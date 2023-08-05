# SPDX-License-Identifier: BSD-2-Clause

from collections       import OrderedDict
from contextlib        import contextmanager
from abc               import ABCMeta, abstractmethod
from typing            import (
	Union, Dict, Any, Literal, Tuple, Generator, List
)
import os
import sys
import subprocess
import tempfile
import zipfile
import hashlib
from pathlib           import Path, PurePosixPath

from ..util.decorators import deprecated

__all__ = (
	'BuildPlan',
	'BuildProducts',
	'LocalBuildProducts',
	'RemoteSSHBuildProducts',
)

class BuildPlan:
	def __init__(self, script: str) -> None:
		'''A build plan.

		Parameters
		----------
		script : str
			The base name (without extension) of the script that will be executed.
		'''
		self.script = script
		self.files  = OrderedDict()

	def add_file(self, filename: str, content: Union[str, bytes]) -> None:
		'''
		Add ``content``, which can be a :class:`str`` or :class:`bytes`, to the build plan
		as ``filename``. The file name can be a relative path with directories separated by
		forward slashes (``/``).
		'''
		assert isinstance(filename, str) and filename not in self.files
		self.files[filename] = content

	def digest(self, size: int = 64) -> bytes:
		'''
		Compute a `digest`, a short byte sequence deterministically and uniquely identifying
		this build plan.
		'''
		hasher = hashlib.blake2b(digest_size = size)
		for filename in sorted(self.files):
			hasher.update(filename.encode('utf-8'))
			content = self.files[filename]
			if isinstance(content, str):
				content = content.encode('utf-8')
			hasher.update(content)
		hasher.update(self.script.encode('utf-8'))
		return hasher.digest()

	def archive(self, file: str) -> None:
		'''
		Archive files from the build plan into ``file``, which can be either a filename, or
		a file-like object. The produced archive is deterministic: exact same files will
		always produce exact same archive.
		'''
		with zipfile.ZipFile(file, 'w') as archive:
			# Write archive members in deterministic order and with deterministic timestamp.
			for filename in sorted(self.files):
				archive.writestr(zipfile.ZipInfo(filename), self.files[filename])

	def execute_local(
		self, root: Union[str, Path] = 'build', *, run_script: bool = True
	) -> 'LocalBuildProducts':
		'''
		Execute build plan using the local strategy. Files from the build plan are placed in
		the build root directory ``root``, and, if ``run_script`` is ``True``, the script
		appropriate for the platform (``{script}.bat`` on Windows, ``{script}.sh`` elsewhere) is
		executed in the build root.

		Returns :class:`LocalBuildProducts`.
		'''

		if isinstance(root, str):
			root = Path(root).resolve()

		root.mkdir(parents = True, exist_ok = True)

		cwd = Path.cwd()
		try:
			os.chdir(root)

			for filename, content in self.files.items():
				filename = Path(filename)
				# Forbid parent directory components completely to avoid the possibility
				# of writing outside the build root.
				if '..' in filename.parts:
					raise RuntimeError(
						f'Unable to write to \'{filename}\'\n'
						'Writing to outside of the build root is forbidden.'
					)

				filename.parent.mkdir(parents = True, exist_ok = True)

				if isinstance(content, str):
					content = content.encode('utf-8')

				with filename.resolve().open('wb') as f:
					f.write(content)

			if run_script:
				if sys.platform.startswith('win32'):
					# Without "call", "cmd /c {}.bat" will return 0.
					# See https://stackoverflow.com/a/30736987 for a detailed explanation of why.
					# Running the script manually from a command prompt is unaffected.
					subprocess.check_call([ 'cmd', '/c', f'call {self.script}.bat' ])
				else:
					subprocess.check_call([ 'sh', f'{self.script}.sh' ])

			return LocalBuildProducts(Path.cwd())

		finally:
			os.chdir(cwd)

	@deprecated('Remote SSH-based builds have been deprecated and will be removed in the next release')
	def execute_remote_ssh(
		self, *, connect_to: Dict[str, Any] = {}, root: str, run_script: bool = True
	) -> 'RemoteSSHBuildProducts':
		'''
		Execute build plan using the remote SSH strategy. Files from the build
		plan are transferred via SFTP to the directory ``root`` on a  remote
		server. If ``run_script`` is ``True``, the ``paramiko`` SSH client will
		then run ``{script}.sh``. ``root`` can either be an absolute or
		relative (to the login directory) path.

		``connect_to`` is a dictionary that holds all input arguments to
		``paramiko``'s ``SSHClient.connect``
		(`documentation <http://docs.paramiko.org/en/stable/api/client.html#paramiko.client.SSHClient.connect>`_).
		At a minimum, the ``hostname`` input argument must be supplied in this
		dictionary as the remote server.

		Returns :class:`RemoteSSHBuildProducts`.
		'''
		from paramiko import SSHClient

		with SSHClient() as client:
			client.load_system_host_keys()
			client.connect(**connect_to)

			with client.open_sftp() as sftp:
				def mkdir_exist_ok(path):
					try:
						sftp.mkdir(str(path))
					except IOError as e:
						# mkdir fails if directory exists. This is fine in torii.build.
						# Reraise errors containing e.errno info.
						if e.errno:
							raise e

				def mkdirs(path):
					# Iteratively create parent directories of a file by iterating over all
					# parents except for the root ("."). Slicing the parents results in
					# TypeError, so skip over the root ("."); this also handles files
					# already in the root directory.
					for parent in reversed(path.parents):
						if parent == PurePosixPath('.'):
							continue
						else:
							mkdir_exist_ok(parent)

				mkdir_exist_ok(root)

				sftp.chdir(root)
				for filename, content in self.files.items():
					filename = PurePosixPath(filename)
					assert '..' not in filename.parts

					mkdirs(filename)

					mode = 't' if isinstance(content, str) else 'b'
					with sftp.file(str(filename), 'w' + mode) as f:
						f.set_pipelined()
						# "b/t" modifier ignored in SFTP.
						if mode == 't':
							f.write(content.encode('utf-8'))
						else:
							f.write(content)

			if run_script:
				transport = client.get_transport()
				channel = transport.open_session()
				channel.set_combine_stderr(True)

				cmd = f'if [ -f ~/.profile ]; then . ~/.profile; fi && cd {root} && sh {self.script}.sh'
				channel.exec_command(cmd)

				# Show the output from the server while products are built.
				buf = channel.recv(1024)
				while buf:
					print(buf.decode('utf-8'), end = '')
					buf = channel.recv(1024)

		return RemoteSSHBuildProducts(connect_to, root)

	def execute(self) -> 'LocalBuildProducts':
		'''
		Execute build plan using the default strategy. Use one of the ``execute_*`` methods
		explicitly to have more control over the strategy.
		'''
		return self.execute_local()


class BuildProducts(metaclass = ABCMeta):
	@abstractmethod
	def get(self, filename: str, mode: Literal['b', 't'] = 'b') -> Union[str, bytes]:
		'''
		Extract ``filename`` from build products, and return it as a :class:`bytes` (if ``mode``
		is ``"b"``) or a :class:`str` (if ``mode`` is ``"t"``).
		'''
		if mode not in ('b', 't'):
			raise ValueError(f'Unsupported file access mode \'{mode}\', must be either \'b\' or \'t\'.')


	@contextmanager
	def extract(self, *filenames: Tuple[str]) -> Generator[
		Union[None, str, List[str]], None, None
	]:
		'''
		Extract ``filenames`` from build products, place them in an OS-specific temporary file
		location, with the extension preserved, and delete them afterwards. This method is used
		as a context manager, e.g.: ::

			with products.extract("bitstream.bin", "programmer.cfg") \
					as bitstream_filename, config_filename:
				subprocess.check_call(["program", "-c", config_filename, bitstream_filename])
		'''
		files = []
		try:
			for filename in filenames:
				# On Windows, a named temporary file (as created by Python) is not accessible to
				# others if it's still open within the Python process, so we close it and delete
				# it manually.
				file = tempfile.NamedTemporaryFile(
					prefix = 'torii_', suffix = '_' + os.path.basename(filename),
					delete = False)
				files.append(file)
				file.write(self.get(filename))
				file.close()

			if len(files) == 0:
				return (yield)
			elif len(files) == 1:
				return (yield files[0].name)
			else:
				return (yield [file.name for file in files])
		finally:
			for file in files:
				os.unlink(file.name)


class LocalBuildProducts(BuildProducts):
	def __init__(self, root: Union[str, Path]) -> None:
		# We provide no guarantees that files will be available on the local filesystem (i.e. in
		# any way other than through `products.get()`) in general, so downstream code must never
		# rely on this, even when we happen to use a local build most of the time.
		if isinstance(root, str):
			self.__root = Path(root)
		else:
			self.__root = root

	def get(self, filename: str, mode: Literal['b', 't'] = 'b') -> Union[str, bytes]:
		super().get(filename, mode)
		with (self.__root / filename).resolve().open(f'r{mode}') as f:
			return f.read()


class RemoteSSHBuildProducts(BuildProducts):

	@deprecated('Remote SSH-based builds have been deprecated and will be removed in the next release')
	def __init__(self, connect_to: Dict[str, Any], root: str) -> None:
		self.__connect_to = connect_to
		self.__root = root

	def get(self, filename: str, mode: Literal['b', 't'] = 'b') -> bytes:
		super().get(filename, mode)

		from paramiko import SSHClient

		with SSHClient() as client:
			client.load_system_host_keys()
			client.connect(**self.__connect_to)

			with client.open_sftp() as sftp:
				sftp.chdir(self.__root)

				with sftp.file(filename, 'r' + mode) as f:
					f.prefetch()
					# "b/t" modifier ignored in SFTP.
					if mode == 't':
						return f.read().decode('utf-8')
					else:
						return f.read()
