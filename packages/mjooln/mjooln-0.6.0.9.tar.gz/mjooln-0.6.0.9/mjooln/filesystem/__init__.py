import psutil
import socket
from sys import platform
import shutil
import glob
import gzip
import zipfile
import hashlib
from pathlib import Path as Path_, PurePath

from mjooln.core import *


# TODO: Add the lack of speed in documentation. Not meant to be used
# for large folders (thats the whole point)
class Path(Glass):
    """ Absolute paths as an instance with convenience functions

    Intended use via subclasses :class:`.Folder` and :class:`.File`

    No relative paths are allowed. Paths not starting with a valid
    mountpoint will be based in current folder

    All backslashes are replaced with :data:`FOLDER_SEPARATOR`
    """
    logger = logging.getLogger(__name__)

    FOLDER_SEPARATOR = '/'
    PATH_CHARACTER_LIMIT = 256

    LINUX = 'linux'
    WINDOWS = 'windows'
    OSX = 'osx'
    PLATFORM = {
        'linux': LINUX,
        'linux2': LINUX,
        'darwin': OSX,
        'win32': WINDOWS,
    }

    @classmethod
    def platform(cls):
        """
        Get platform name alias

            - :data:`WINDOWS`
            - :data:`LINUX`
            - :data:`OSX`

        Example on a linux platform::

            Path.platform()
                'linux'

            Path.platform() == Path.LINUX
                True

        :raises PathError: If platform is unknown
        :return: Platform name alias
        :rtype: str
        """
        if platform in cls.PLATFORM:
            return cls.PLATFORM[platform]
        else:
            raise PathError(f'Unknown platform {platform}. '
                            f'Known platforms are: {cls.PLATFORM.keys()}')

    @classmethod
    def host(cls):
        """ Get host name

        Wrapper for ``socket.gethostname()``

        :return: Host name
        :rtype: str
        """
        return socket.gethostname()

    @classmethod
    def _join(cls, *args):
        return os.path.join(*args)

    @classmethod
    def join(cls, *args):
        """ Join strings to path

        Wrapper for ``os.path.join()``

        Relative paths will include current folder::

            Path.current()
                '/Users/zaphod/dev'
            Path.join('code', 'donald')
                '/Users/zaphod/dev/code/donald'

        :return: Joined path as absolute path
        :rtype: Path
        """
        return cls(cls._join(*args))

    @classmethod
    def mountpoints(cls):
        # TODO: Add limit on levels or something to only get relevant partitions
        """ List valid mountpoints/partitions or drives

        Finds mountpoints/partitions on linux/osx, and drives (C:, D:) on
        windows.

        .. note:: Network drives on windows will not be found by this method,
            unless they have been mapped

        :return: Valid mountpoints or drives
        :rtype: list
        """
        mps = [Folder(x.mountpoint.replace('\\', cls.FOLDER_SEPARATOR))
               for x in psutil.disk_partitions(all=True)
               if os.path.isdir(x.mountpoint)]
        # Remove duplicates (got double instance of root in a terraform vm)
        return list(set(mps))

    @classmethod
    def has_valid_mountpoint(cls, path_str):
        """ Flags if the path starts with a valid mountpoint

        .. note:: If platform is Windows, and path starts with double slash,
            it is interpreted as a network drive and therefore as having
            valid mountpoint

        :return: True if path has valid mountpoint, False if not
        :rtype: bool
        """
        if cls.platform() == cls.WINDOWS and cls.is_network_drive(path_str):
            return True
        return len([x for x in cls.mountpoints()
                    if path_str.startswith(x)]) > 0

    @classmethod
    def listdir(cls, path_str):
        """
        List folder content as plain strings with relative path names

        Wrapper for ``os.listdir()``

        Other list and walk methods in :class:`Folder` will instantiate
        :class:`File` or :class:`Folder` objects. They are thus a bit slower

        :param path_str: String with path to folder
        :return: List of relative path strings
        """
        return os.listdir(path_str)

    @classmethod
    def validate(cls, path_str):
        """
        Check if path is longer than :data:`PATH_CHARACTER_LIMIT`, which
        on Windows may cause problems

        :param path_str: Path to check
        :type path_str: str
        :raises PathError: If path is too long
        """
        if len(path_str) > cls.PATH_CHARACTER_LIMIT:
            raise PathError(f'Path exceeds {cls.PATH_CHARACTER_LIMIT} '
                            f'characters, which may cause problems on '
                            f'some platforms')
        # TODO: Add check on characters in path

    def __init__(self, path: str):
        if PIXIE and not isinstance(path, str):
            raise PixieInPipeline(f'Input to Path constructor '
                                  f'must be of type str')
        if not os.path.isabs(path):
            path = path.replace('\\', self.FOLDER_SEPARATOR)
            path = os.path.abspath(path)
        path = path.replace('\\', self.FOLDER_SEPARATOR)
        if PIXIE:
            try:
                self.validate(path)
            except PathError as pe:
                raise PixieInPipeline(f'Invalid path: {path}') from pe
        self.__path = path

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return self.__path

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __le__(self, other):
        return str(self) <= str(other)

    def __ge__(self, other):
        return str(self) >= str(other)

    # Make pandas (and other libraries) recognize Path class as pathlike
    def __fspath__(self):
        return str(self)

    def __repr__(self):
        return f'Path(\'{self.__path}\')'

    def _rename(self, new_path: str):
        self.__path = new_path

    def as_file(self):
        """
        Create :class:`File` with same path

        :rtype: File
        """
        return File(self.__path)

    def as_folder(self):
        """
        Create :class:`Folder` with same path

        :rtype: Folder
        """
        return Folder(self.__path)

    def as_path(self):
        """
        Get as ``pathlib.Path`` object

        :return: path
        :rtype: pathlib.Path
        """
        return Path_(str(self))

    def as_pure_path(self):
        """
        Get as ``pathlib.PurePath`` object

        :return: path
        :rtype: pathlib.PurePath
        """
        return PurePath(str(self))

    def name(self):
        """ Get name of folder or file

        Example::

            p = Path('/Users/zaphod')
            p
                '/Users/zaphod
            p.name()
                'zaphod'

            p2 = Path(p, 'dev', 'code', 'donald')
            p2
                '/Users/zaphod/dev/code/donald'
            p2.name()
                'donald'

            p3 = Path(p, 'dev', 'code', 'donald', 'content.txt')
            p3
                '/Users/zaphod/dev/code/donald/content.txt'
            p3.name()
                'content.txt'

        :return: Folder or file name
        :rtype: str
        """
        return os.path.basename(str(self))

    def volume(self):
        """ Return path volume

        Volume is a collective term for mountpoint, drive and network drive

        :raises PathError: If volume cannot be determined
        :return: Volume of path
        :rtype: Folder
        """
        try:
            return self.network_drive()
        except PathError:
            pass
        mountpoints = self.mountpoints()
        candidates = [x for x in mountpoints if str(self).startswith(str(x))]
        if len(candidates) > 1:
            candidates = [x for x in candidates
                          if not x == self.FOLDER_SEPARATOR]
        if len(candidates) == 1:
            return Folder.glass(candidates[0])
        else:
            # Find the longest matching candidate (should be the one)
            lens = [(len(x), x) for x in candidates]
            lens.sort(reverse=True)
            # Check that the two longest don't have same length
            # (this should not happen, since that would mean there were
            # two identical mountpoints)
            if lens[0][0] > lens[1][0]:
                return lens[0][1]
            else:
                raise PathError(
                    f'Could not determine volume for path: {self}; '
                    f'Based on candidates: {candidates};'
                    f'Avaliable mountpoints: {mountpoints}')

    def exists(self):
        """ Check if path exists

        Wrapper for ``os.path.exists()``

        :return: True if path exists, False otherwise
        :rtype: bool
        """
        return os.path.exists(self)

    def raise_if_not_exists(self):
        """ Raises an exception if path does not exist

        :raises PathError: If path does not exist
        """
        if not self.exists():
            raise PathError(f'Path does not exist: {self}')

    def is_volume(self):
        """
        Check if path is a volume

        Volume is a collective term for mountpoint, drive and network drive

        :raises PathError: If path does not exist
        :return: True if path is a volume, False if not
        :rtype: bool
        """
        if self.exists():
            return self.is_network_drive() or self in self.mountpoints()
        else:
            raise PathError(f'Cannot see if non existent path '
                            f'is a volume or not: {self}')

    def on_network_drive(self):
        """
        Check if path is on a network drive

        .. warning:: Only checks if the path starts with double slash, and may
            be somewhat unreliable. Make sure to test if it seems to work

        :return: True if path is on network drive, False if not
        :rtype: bool
        """
        return str(self).startswith('//')

    def network_drive(self):
        """
        Returns the first part of the path following the double slash

        Example::

            p = Path('//netwdrive/extensions/parts')
            p.network_drive()
                Folder('//netwdrive')

        :raises PathError: If path is not on a network drive
            (see :meth:`on_network_drive()`)
        :return: Network drive part of the path
        :rtype: Folder
        """
        if self.on_network_drive():
            return Folder('//' + self.parts()[0])
        else:
            raise PathError(f'Path is not on a network drive: {self}')

    def is_network_drive(self):
        """
        Check if path is a network drive following the same rules as
        in :meth:`on_network_drive()`

        .. note:: If on Windows, a mapped network drive will not be
            interpreted as a network drive, since the path starts with a
            drive letter

        :return: True if path is network drive, False if not
        :rtype: bool
        """
        try:
            return self.network_drive() == self
        except PathError:
            return False

    def is_folder(self):
        """
        Check if path is a folder

        :raises PathError: If path does not exist
        :return: True if path is a folder, False if not
        :rtype: bool
        """
        if self.exists():
            return os.path.isdir(self)
        else:
            raise PathError(f'Cannot determine if non existent path '
                            f'is a folder or not: {self}')

    def is_file(self):
        """ Check if path is a file

        :raises PathError: If path does not exist
        :return: True if path is a file, False if not
        :rtype: bool
        """
        if self.exists():
            return os.path.isfile(self)
        else:
            raise PathError(f'Cannot determine if non existent path '
                            f'is a file or not: {self}')

    def size(self):
        """ Return file or folder size

        .. note:: If Path is a folder, ``size()`` will return a small number,
            representing the size of the folder object, not its contents.
            For finding actual disk usage of a folder, use
            :meth:`.Folder.disk_usage()`

        :raises PathError: If path does not exist
        :returns: File or folder size
        :rtype: int
        """
        if self.exists():
            return os.stat(self).st_size
        else:
            raise PathError(f'Cannot determine size of '
                            f'non existent path: {self}')

    def created(self):
        """
        Get created timestamp from operating system

        Wrapper for ``os.stat(<path>).st_ctime``

        .. note:: Created timestamp tends to be unreliable, especially
            when files have been moved around

        :return: Timestamp created (perhaps)
        :rtype: Zulu
        """
        return Zulu.from_epoch(os.stat(self).st_ctime)

    def modified(self):
        """
        Get modified timestamp from operating system

        Wrapper for ``os.stat(<path>).st_mtime``

        .. note:: Modified timestamp tends to be unreliable, especially
            when files have been moved around

        :returns: Timestamp modified (perhaps)
        :rtype: Zulu
        """
        return Zulu.from_epoch(os.stat(self).st_mtime)

    def parts(self):
        """
        Get list of parts in path

        Example::

            p = Path('/home/zaphod/dev/code')
            p.parts()
                ['home', 'zaphod', 'dev', 'code']

        :returns: String parts of path
        :rtype: list
        """
        parts = str(self).split(self.FOLDER_SEPARATOR)
        # Remove empty first part (if path starts with /)
        if parts[0] == '':
            parts = parts[1:]
        # Once more in case this is a network drive
        if parts[0] == '':
            parts = parts[1:]
        return parts


class Folder(Path):

    @classmethod
    def home(cls):
        """ Get path to user home folder

        Wrapper for ``os.path.expanduser()``

        :return: Home folder path
        :rtype: Folder
        """
        return Folder(os.path.expanduser('~'))

    @classmethod
    def current(cls):
        """ Get current folder path

        Wrapper for ``os.getcwd()``

        :return: Path to current folder
        :rtype: Folder
        """
        return cls(os.getcwd())

    def __init__(self, path, *args, **kwargs):
        super(Folder, self).__init__(path)
        if PIXIE:
            if self.exists():
                if self.is_file():
                    raise PixieInPipeline(f'Path is a file, '
                                          f'not a folder: {self}')

    def __repr__(self):
        return f'Folder(\'{self}\')'

    def create(self, error_if_exists=True):
        """ Create new folder, including non existent parent folders

        :raises FolderError: If folder already exists,
            *and* ``error_if_exists=True``
        :param error_if_exists: Error flag. If True, method will raise an
            error if the folder already exists
        :type error_if_exists: bool
        :returns: True if it was created, False if not
        :rtype: bool
        """
        if not self.exists():
            os.makedirs(self)
            return True
        else:
            if error_if_exists:
                raise FolderError(f'Folder already exists: {self}')
            return False

    def touch(self):
        """
        Create folder if it does not exist, ignore otherwise
        """
        self.create(error_if_exists=False)

    def untouch(self):
        """
        Remove folder if it exists, ignore otherwise

        :raises OSError: If folder exists but is not empty
        """
        self.remove(error_if_not_exists=False)

    def parent(self):
        """ Get parent folder

        :return: Parent folder
        :rtype: Folder
        """
        return Folder(os.path.dirname(str(self)))

    def append(self, *args):
        """ Append strings or list of strings to current folder

        Example::

            fo = Folder.home()
            print(fo)
                '/Users/zaphod'

            fo.append('dev', 'code', 'donald')
                '/Users/zaphod/dev/code/donald'

            parts = ['dev', 'code', 'donald']
            fo.append(parts)
                '/Users/zaphod/dev/code/donald'

        :param args: Strings or list of strings
        :return: Appended folder as separate object
        :rtype: Folder
        """
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, list):
                return Folder.join(str(self), '/'.join(arg))
            else:
                return Folder.join(str(self), arg)
        else:
            return Folder.join(str(self), *args)

    def file(self, name: str):
        """
        Create file path in this folder

        :param name: File name
        :type name: str
        :return: File path in this folder
        :rtype: File
        """
        if PIXIE:
            if os.path.abspath(name) == name:
                raise PixieInPipeline(f'File name is already full path: {name}')
        return File.join(str(self), name)

    def is_empty(self):
        """ Check if folder is empty

        :raise FolderError: If folder does not exist
        :return: True if empty, False if not
        :rtype: bool
        """
        if self.exists():
            return len(list(self.list())) == 0
        else:
            raise FolderError(f'Cannot check if non existent folder '
                              f'is empty: {self}')

    # TODO: Add test for empty, with missing name
    def empty(self, name: str):
        """
        Recursively deletes all files and subfolders

        Name of folder is required to verify deleting content

        .. warning:: Be careful. Will delete  all content recursively

        :param name: Folder name as given by :meth:`.Folder.name()`.
            Required to verify deleting all contents
        :type name: str
        :raises FolderError: If folder does not exist, or if ``name`` is not
            an exact match with folder name
        """
        if self.name() != name:
            raise FolderError(f'Text of folder required to verify '
                              f'deletion: name={self.name()}')
        if self.exists():
            for name in os.listdir(self):
                path = os.path.join(self, name)
                if os.path.isfile(path) or os.path.islink(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
        else:
            raise FolderError(f'Cannot empty a non existent folder: {self}')

    def remove(self,
               error_if_not_exists: bool = True):
        """
        Remove folder

        :raises OSError: If folder exists but is not empty
        :raises FolderError: If folder does not exist and
            ``error_if_not_exists=True``
        :param error_if_not_exists: If True, method will raise an
            error if the folder already exists
        :type error_if_not_exists: bool
        """
        if self.exists():
            os.rmdir(str(self))
        else:
            if error_if_not_exists:
                raise FolderError(f'Cannot remove a non existent '
                                  f'folder: {self}')

    def remove_empty_folders(self):
        """
        Recursively remove empty subfolders
        """
        fo_str = str(self)
        for root, folders, files in os.walk(fo_str):
            if root != fo_str and not folders and not files:
                os.rmdir(root)

    def list(self,
             pattern: str = '*',
             recursive: bool = False):
        """
        List folder contents

        Example patterns:

            - ``'*'`` (default) Returns all files and folders except hidden
            - ``'.*`` Returns all hidden files and folders
            - ``'*.txt'`` Return all files ending with 'txt'

        .. note:: For large amounts of files and folders, use the generator
            returned by :meth:`.Folder.walk()` and handle them individually

        :raises FolderError: If folder does not exist
        :param pattern: Pattern to search for
        :param recursive: If True search will include all subfolders and files
        :return: List of :class:`.File` and/or :class:`Folder`
        :rtype: list
        """
        if not self.exists():
            raise FolderError(f'Cannot list non existent folder: {self}')

        if recursive:
            paths = glob.glob(str(self.append('**', pattern)),
                              recursive=True)
        elif pattern is None:
            paths = os.listdir(str(self))
        else:
            paths = glob.glob(str(self.append(pattern)))
        for i, path in enumerate(paths):
            try:
                if os.path.isfile(path):
                    paths[i] = File(path)
                elif os.path.isdir(path):
                    paths[i] = Folder(path)
            except FileError or PathError or FolderError:
                # TODO: Handle links and other exceptions
                pass
        return paths

    def list_files(self,
                   pattern='*',
                   recursive=False):
        """
        List all files in this folder matching ``pattern``

        Uses :meth:`.Folder.list()` and then filters out all :class:`.File`
        objects and returns the result

        .. note:: For large amounts of files, use the generator
            returned by :meth:`.Folder.files()` and handle them individually

        :raises FolderError: If folder does not exist
        :param pattern: Pattern to search for
        :param recursive: If True search will include all subfolders and files
        :return: List of :class:`.File` objects
        :rtype: list
        """
        paths = self.list(pattern=pattern,
                          recursive=recursive)
        return [x for x in paths if isinstance(x, File)]

    def list_folders(self,
                     pattern='*',
                     recursive=False):
        """
        List all folders in this folder matching ``pattern``

        Uses :meth:`.Folder.list()` and then filters out all :class:`.Folder`
        objects and returns the result

        .. note:: For large amounts of folders, use the generator
            returned by :meth:`.Folder.folders()` and handle them individually

        :raises FolderError: If folder does not exist
        :param pattern: Pattern to search for
        :param recursive: If True search will include all subfolders and files
        :return: List of :class:`.Folder` objects
        :rtype: list
        """
        paths = self.list(pattern=pattern,
                          recursive=recursive)
        return [x for x in paths if isinstance(x, Folder)]

    def walk(self,
             include_files: bool = True,
             include_folders: bool = True):
        """
        Generator listing all files and folders in this folder recursively

        :return: Generator object returning :class:`File` or :class:`Folder`
            for each iteration
        :rtype: generator
        """
        for root, fos, fis in os.walk(str(self)):
            if include_folders:
                for fo in (Folder.join(root, x) for x in fos):
                    if fo.exists():
                        yield fo
            if include_files:
                for fi in (File.join(root, x) for x in fis):
                    if fi.exists():
                        yield fi

    def files(self):
        """
        Generator listing all files in this folder recursively

        Print all files larger than 1 kB in home folder and all subfolders::

            fo = Folder.home()
            for fi in fo.files():
                if fi.size() > 1000:
                    print(fi)

        :return: Generator object returning :class:`File` for each iteration
        :rtype: generator
        """
        return self.walk(include_files=True,
                         include_folders=False)

    def folders(self):
        """
        Generator listing all folders in this folder recursively

        :return: Generator object returning :class:`Folder` for each iteration
        :rtype: generator
        """
        return self.walk(include_files=False,
                         include_folders=True)

    def count(self,
              include_files: bool = True,
              include_folders: bool = True):
        """
        Count number of files and/or folders recursively

        .. note:: Links will also be included

        :param include_files: Include files in count
        :type include_files: bool
        :param include_folders: Include folders in count
        :type include_folders: bool
        :return: Number of files and/or folders in folder
        :rtype: int
        """
        count = 0
        for root, fos, fis in os.walk(str(self)):
            if include_folders:
                count += len(fos)
            if include_files:
                count += len(fis)
        return count

    def count_files(self):
        """
        Count number of files recursively

        .. note:: Links will also be included

        :return: Number of files in folder
        :rtype: int
        """
        return self.count(include_files=True, include_folders=False)

    def count_folders(self):
        """
        Count number of folders recursively

        .. note:: Links will also be included

        :return: Number of folders in folder
        :rtype: int
        """
        return self.count(include_files=False, include_folders=True)

    def disk_usage(self,
                   include_folders: bool = False,
                   include_files: bool = True):
        """
        Recursively determines disk usage of all contents in folder

        :param include_folders: If True, all folder sizes will be included in
            total, but this is only the folder object and hence a small number.
            Default is therefore False
        :param include_files: If True, all file sizes are included in total.
            Default is obviously True
        :raises FolderError: If folder does not exist
        :return: Disk usage of folder content
        :rtype: int
        """
        if not self.exists():
            raise FolderError(f'Cannot determine disk usage of '
                              f'non existent folder: {self}')
        size = 0
        for root, fos, fis in os.walk(str(self)):
            if include_folders:
                for fo in fos:
                    try:
                        size += os.stat(os.path.join(root, fo)).st_size
                    except FileNotFoundError:
                        pass
            if include_files:
                for fi in fis:
                    try:
                        size += os.stat(os.path.join(root, fi)).st_size
                    except FileNotFoundError:
                        pass
        return size

    def print(self,
              count: bool = False,
              disk_usage: bool = False):
        """
        Print folder content

        :param count: Include count for each subfolder
        :type count: bool
        :param disk_usage: Include disk usage for each subfolder, and size
            for each file
        :type disk_usage: bool
        """
        paths = self.list()
        for path in paths:
            if not path.exists():
                print(f'{path.name()} [link or deleted]')
            else:
                if path.is_folder():
                    print(f'{path.name()} [Folder]')
                    if count or disk_usage:
                        fo = Folder(str(path))
                        if count:
                            nfo = fo.count_folders()
                            print(f'\tSubfolder count: {nfo}')
                            nfi = fo.count_files()
                            print(f'\tFile count: {nfi}')
                        if disk_usage:
                            du = fo.disk_usage()
                            dustr = Math.bytes_to_human(du)
                            print(f'\tDisk usage: {dustr}')
                elif path.is_file():
                    print(f'{path.name()} [File]')
                    if disk_usage:
                        fi = File(str(path))
                        size = Math.bytes_to_human(fi.size())
                        print(f'\tSize: {size}')
                else:
                    print(f'{path.name()} [unknown]')

    # def print(self,
    #           indent: int = 2,
    #           include_files: bool = True,
    #           include_folders: bool = True):
    #     """
    #     :param indent:
    #     :param include_files:
    #     :param include_folders:
    #     :return:
    #     """
    #     # TODO: Redo with sequential walkthrough, and max_depth
    #     fo_str = str(self)
    #     for path in self.walk(include_files=include_files,
    #                           include_folders=include_folders):
    #         level = str(path).replace(fo_str, '').count('/')
    #         path_indent = ' ' * indent * level
    #         path_tag = ''
    #         if path.is_folder():
    #             path_tag = '/'
    #         print(f'{path_indent}{path.name()}{path_tag}')


# class FileElements(Doc):
#     __pixie = Config.PIXIE_IN_PIPELINE
#
#
#
#     COMPRESSED_ENDSWITH = EXTENSION_SEPARATOR + COMPRESSED_EXTENSION
#     ENCRYPTED_ENDSWITH = EXTENSION_SEPARATOR + ENCRYPTED_EXTENSION
#     COMPRESSED_AND_ENCRYPTED_ENDSWITH = \
#         EXTENSION_SEPARATOR + COMPRESSED_EXTENSION + ENCRYPTED_ENDSWITH
#
#     def __init__(self,
#                  stub: str,
#                  extension: str,
#                  is_hidden: bool = False,
#                  is_compressed: bool = False,
#                  is_encrypted: bool = False):
#         """
#         Create file name from stub and attributes
#
#         :param stub: File stub, barring extensions and hidden startswith
#         :param extension: File extension
#         :param is_hidden: True tags file name as hidden
#         :param is_compressed: True tags file name as compressed, adding the
#             necessary extra extension
#         :param is_encrypted:
#         :return:
#         """
#         super().__init__()
#         if self.__pixie:
#             if stub.startswith(self.HIDDEN_STARTSWITH):
#                 raise FileError(f'Stub cannot start with the hidden flag. '
#                                 f'Keep stub clean, and set is_hidden=True')
#             if self.EXTENSION_SEPARATOR in stub:
#                 raise FileError(f'Cannot add stub with extension '
#                                 f'separator in it: {stub}. '
#                                 f'Need a clean string for this')
#             if self.EXTENSION_SEPARATOR in extension:
#                 raise FileError(f'Cannot add extension with extension '
#                                 f'separator in it: {extension}. '
#                                 f'Need a clean string for this')
#         self.stub = stub
#         self.extension = extension
#         self.is_hidden = is_hidden
#         self.is_compressed = is_compressed
#         self.is_encrypted = is_encrypted
#         if self.__pixie:
#             if self.EXTENSION_SEPARATOR in extension:
#                 raise PixieInPipeline(f'There should not be a separator in '
#                                       f'an extension: {extension}')
#
#         self.__name = None

# def __str__(self):
#     if not self.__name:
#         names = [self.stub, self.extension]
#         if self.is_compressed:
#             names += [self.COMPRESSED_EXTENSION]
#         if self.is_encrypted:
#             names += [self.ENCRYPTED_EXTENSION]
#         name = self.EXTENSION_SEPARATOR.join(names)
#         if self.is_hidden:
#             name = self.HIDDEN_STARTSWITH + name
#         self.__name = name
#     return self.__name

# def parts(self):
#     parts = [self.stub,
#              self.extension]
#     if self.is_compressed:
#         parts += self.COMPRESSED_EXTENSION
#     if self.is_encrypted:
#         parts += self.ENCRYPTED_EXTENSION
#     return parts
#
#
#     return dict(stub=stub,
#                 extension=extension,
#                 extensions=extensions,
#                 is_hidden=is_hidden,
#                 is_compressed=is_compressed,
#                 is_encrypted=is_encrypted)

# def from_name(self, name):
#     di = self.name_to_dict(name):
#     if not di['extensions']:
#
# def __repr__(self):
#     kwargs = [f'\'{self.stub}\'',
#               f'\'{self.extension}\'']
#     if self.is_hidden:
#         kwargs += f'is_hidden={self.is_hidden}'
#     if self.is_compressed:
#         kwargs += f'is_compressed={self.is_compressed}'
#     if self.is_encrypted:
#         kwargs += f'is_encrypted={self.is_encrypted}'
#     kwargs = ', '.join(kwargs)
#     return f'FileElements({kwargs})'


class File(Path):
    """
    Convenience class for file handling

    Create a file path in current folder::

        fi = File('my_file.txt')
        fi
            File('/home/zaphod/current/my_file.txt')

    Create a file path in home folder::

        fi = File.home('my_file.txt')
        fi
            File('/home/zaphod/my_file.txt')

    Create a file path in some folder::

        fo = Folder.home().append('some/folder')
        fo
            Folder('/home/zaphod/some/folder')
        fi = fo.file('my_file.txt')
        fi
            File('/home/zaphod/some/folder/my_file.txt')

    Create and read a file::

        fi = File('my_file.txt')
        fi.write('Hello world')
        fi.read()
            'Hello world'
        fi.size()
            11

    Compress and encrypt::

        fi.compress()
        fi.name()
            'my_file.txt.gz'
        fi.read()
            'Hello world'

        crypt_key = Crypt.generate_key()
        crypt_key
            b'aLQYOIxZOLllYThEKoXTH_eqTQGEnXm9CUl2glq3a2M='
        fi.encrypt(crypt_key)
        fi.name()
            'my_file.txt.gz.aes'
        fi.read(crypt_key=crypt_key)
            'Hello world'

    Create an encrypted file, and write to it::

        ff = File('my_special_file.txt.aes')
        ff.write('Hello there', password='123')
        ff.read(password='123')
            'Hello there'

        f = open(ff)
        f.read()
            'gAAAAABe0BYqPPYfzha3AKNyQCorg4TT8DcJ4XxtYhMs7ksx22GiVC03WcrMTnvJLjTLNYCz_N6OCmSVwk29Q9hoQ-UkN0Sbbg=='
        f.close()

    .. note:: Using the ``password`` parameter, builds an encryption key by
        combining it with the builtin (i.e. hard coded) class salt.
        For proper security, generate your
        own salt with :meth:`.Crypt.salt()`. Store this salt appropriately,
        then use :meth:`.Crypt.key_from_password()` to generate a crypt_key

    .. warning:: \'123\' is not a real password

    """
    _salt = b'O89ogfFYLGUts3BM1dat4vcQ'

    logger = logging.getLogger(__name__)

    #: Files with this extension will compress text before writing to file
    #: and decompress after reading
    COMPRESSED_EXTENSION = COMPRESSED_EXTENSION

    #: Files with this extension will encrypt before writing to file, and
    #: decrypt after reading. The read/write methods therefore require a
    #: crypt_key
    ENCRYPTED_EXTENSION = ENCRYPTED_EXTENSION

    JSON_EXTENSION = 'json'
    YAML_EXTENSION = 'yaml'

    # #: Extensions reserved for compression and encryption
    # RESERVED_EXTENSIONS = [COMPRESSED_EXTENSION,
    #                        ENCRYPTED_EXTENSION]

    #: File names starting with this character will be tagged as hidden
    HIDDEN_STARTSWITH = '.'

    #: Extension separator. Period
    EXTENSION_SEPARATOR = '.'

    # TODO: Add binary flag based on extension (all other than text is binary..)
    # TODO: Facilitate child classes with custom read/write needs

    @classmethod
    def make(cls,
             folder,
             stub: str,
             extension: str,
             is_hidden: bool = False,
             is_compressed: bool = False,
             is_encrypted: bool = False):
        """
        Create a file path following proper file name structure

        :param folder: Containing folder
        :type folder: Folder
        :param stub: File stub
        :type stub: str
        :param extension: File extension added after file stub
        :type extension: str
        :param is_hidden: Whether file is hidden or not. True will add
             :data:`HIDDEN_STARTSWITH` to beginning of filename
        :type is_hidden: bool
        :param is_compressed: True will add the :data:`COMPRESSED_EXTENSION`
            after the regular extension
        :type is_compressed: bool
        :param is_encrypted: True will add the :data:`ENCRYPTED_EXTENSION`
            after the regular extension and possible compressed extension
        :type is_encrypted: bool
        :rtype: File
        """
        folder = Folder.glass(folder)
        names = [stub, extension]
        if is_compressed:
            names += [cls.COMPRESSED_EXTENSION]
        if is_encrypted:
            names += [cls.ENCRYPTED_EXTENSION]
        name = cls.EXTENSION_SEPARATOR.join(names)
        if is_hidden:
            name = cls.HIDDEN_STARTSWITH + name

        return cls.join(folder, name)

    @classmethod
    def home(cls,
             file_name: str):
        """
        Create a file path in home folder

        :param file_name: File name
        :type file_name: str
        :rtype: File
        """
        return cls.join(Folder.home(), file_name)

    @classmethod
    def _crypt_key(cls,
                   crypt_key: bytes = None,
                   password: str = None):
        if crypt_key and password:
            raise FileError('Use either crypt_key or password.')
        elif not crypt_key and not password:
            raise FileError('crypt_key or password missing')
        if crypt_key:
            return crypt_key
        else:
            return Crypt.key_from_password(cls._salt, password)

    def __init__(self, path: str, *args, **kwargs):
        super(File, self).__init__(path)
        if PIXIE:
            if self.exists():
                if self.is_volume():
                    raise PixieInPipeline(f'Path is volume, not file: {path}')
                elif self.is_folder():
                    raise PixieInPipeline(f'Path is existing folder, '
                                          f'not file: {path}')
        # Lazy parsing of file name to avoid unnecessary processing
        self.__name_is_parsed = False
        self.__parts = None
        self.__stub = None
        self.__extension = None
        self.__extensions = None
        self.__hidden = None
        self.__compressed = None
        self.__encrypted = None

    def __repr__(self):
        return f'File(\'{self}\')'

    def _rename(self, new_path: str):
        super()._rename(new_path)
        self.__name_is_parsed = False

    def _parse_name(self):
        if not self.__name_is_parsed:
            name = self.name()
            self.__hidden = name.startswith(self.HIDDEN_STARTSWITH)
            if self.__hidden:
                name = name[1:]
            parts = name.split(self.EXTENSION_SEPARATOR)
            while not parts[0]:
                parts = parts[1:]
            self.__parts = parts.copy()
            self.__stub = parts[0]
            parts = parts[1:]
            self.__extension = None
            self.__extensions = parts
            self.__compressed = False
            self.__encrypted = False
            if parts and parts[-1] == self.ENCRYPTED_EXTENSION:
                self.__encrypted = True
                parts = parts[:-1]

            if parts and parts[-1] == self.COMPRESSED_EXTENSION:
                self.__compressed = True
                parts = parts[:-1]

            if len(parts) == 1:
                self.__extension = self.__extensions[0]
            self.__name_is_parsed = True

    def parts(self):
        """
        Get file parts, i.e. those separated by period

        :return: list
        """
        self._parse_name()
        return self.__parts

    def touch(self):
        """
        Create empty file if it does not exist already
        """
        self.folder().touch()
        Path_(self).touch()

    def untouch(self, ignore_if_not_empty=False):
        """
        Delete file if it exists, and is empty

        :param ignore_if_not_empty: If True, no exception is raised if file
            is not empty and thus cannot be deleted with untouch
        :return:
        """
        if self.exists():
            if self.size() == 0:
                self.delete()
            else:
                if not ignore_if_not_empty:
                    raise FileError(f'Cannot untouch file '
                                    f'that is not empty: {self}; '
                                    f'Use delete() to delete a non-empty file')

    def extensions(self):
        """
        Get file extensions as a list of strings

        :return: List of file extensions
        :rtype: list
        """
        self._parse_name()
        return self.__extensions

    def is_hidden(self):
        """
        Check if file is hidden, i.e. starts with :data:`HIDDEN_STARTSWITH`

        :return: True if hidden, False if not
        :rtype: bool
        """
        self._parse_name()
        return self.__hidden

    def is_compressed(self):
        """
        Check if file is compressed, i.e. has :data:`COMPRESSED_EXTENSION`

        :return: True if compressed, False if not
        :rtype: bool
        """
        self._parse_name()
        return self.__compressed

    def is_encrypted(self):
        """
        Check if file is encrypted, i.e. has :data:`ENCRYPTED_EXTENSION`

        :return: True if encrypted, False if not
        :rtype: bool
        """
        self._parse_name()
        return self.__encrypted

    def stub(self):
        """
        Get file stub, i.e. the part of the file name bar extensions and
        :data:`HIDDEN_STARTSWITH`

        Example::

            fi = File('.hidden_with_extensions.json.gz')
            fi.stub()
                'hidden_with_extensions'

        :return: File stub
        :rtype: str
        """
        self._parse_name()
        return self.__stub

    def extension(self):
        """
        Get file extension, i.e. the extension which is not reserved.
        A file is only supposed to have one extension that does not indicate
        either compression or encryption.

        :raise FileError: If file has more than one extension barring
            :data:`COMPRESSED_EXTENSION` and :data:`ENCRYPTED_EXTENSION`
        :return: File extension
        :rtype: str
        """
        self._parse_name()
        return self.__extension

    def md5_checksum(self):
        """
        Get MD5 Checksum for the file

        :raise FileError: If file does not exist
        :return: MD5 Checksum
        :rtype: str
        """
        if not self.exists():
            raise FileError(f'Cannot make checksum '
                            f'if file does not exist: {self}')
        md5 = hashlib.md5()
        with open(self, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()

    def new(self, name):
        """
        Create a new file path in same folder as current file

        :param name: New file name
        :rtype: File
        """
        return self.folder().file(name)

    def delete(self,
               missing_ok: bool = False):
        """
        Delete file

        :raise FileError: If file is missing, and ``missing_ok=False``
        :param missing_ok: Indicate if an exception should be raised if the
            file is missing. If True, an exception will not be raised
        :type missing_ok: bool
        """
        if self.exists():
            self.logger.debug(f'Delete file: {self}')
            os.unlink(self)
        elif not missing_ok:
            raise FileError(f'Tried to delete file '
                            f'that doesn\'t exist: {self}')

    def delete_if_exists(self):
        """
        Delete file if exists
        """
        self.delete(missing_ok=True)

    def write(self, data, mode='w',
              crypt_key: bytes = None,
              password: str = None,
              **kwargs):
        """
        Write data to file

        For encryption, use either ``crypt_key`` or ``password``. None or both
        will raise an exception. Encryption requires the file name to end with
        :data:`ENCRYPTED_EXTENSION`

        :raise FileError: If using ``crypt_key`` or ``password``, and the
            file does not have encrypted extension
        :param data: Data to write
        :type data: str or bytes
        :param mode: Write mode
        :type mode: str
        :param crypt_key: Encryption key
        :type crypt_key: bytes
        :param password: Password (will use class salt)
        :type password: str
        """
        if PIXIE and (
                crypt_key or password) and not self.is_encrypted():
            raise PixieInPipeline(f'File does not have crypt extension '
                                  f'({self.ENCRYPTED_EXTENSION}), '
                                  f'but a crypt_key '
                                  f'or password was sent as input to write.')

        if self.is_encrypted():
            crypt_key = self._crypt_key(crypt_key=crypt_key,
                                        password=password)

        self.folder().touch()
        if self.is_compressed():
            if self.is_encrypted():
                self._write_compressed_and_encrypted(data, crypt_key=crypt_key)
            else:
                self._write_compressed(data)
        elif self.is_encrypted():
            self._write_encrypted(data, crypt_key=crypt_key)
        else:
            self._write(data, mode=mode)

    def write_json(self,
                   data: dict,
                   human: bool = False,
                   crypt_key: bytes = None,
                   password: str = None,
                   **kwargs):
        """
        Write dictionary to JSON file

        Extends :meth:`.JSON.dumps()` with :meth:`.File.write()`

        For encryption, use either ``crypt_key`` or ``password``. None or both
        will raise an exception. Encryption requires the file name to end with
        :data:`ENCRYPTED_EXTENSION`

        :raise FileError: If using ``crypt_key`` or ``password``, and the
            file does not have encrypted extension
        :param data: Data to write
        :type data: str or bytes
        :param human: If True, write JSON as human readable
        :type human: bool
        :param crypt_key: Encryption key
        :type crypt_key: bytes
        :param password: Password (will use class salt)
        :type password: str
        """
        data = JSON.dumps(data, human=human)
        self.write(data, mode='w', crypt_key=crypt_key, password=password)

    def write_yaml(self,
                   data: dict,
                   crypt_key: bytes = None,
                   password: str = None,
                   **kwargs):
        """
        Write dictionary to YAML file

        Extends :meth:`.YAML.dumps()` with :meth:`.File.write()`

        For encryption, use either ``crypt_key`` or ``password``. None or both
        will raise an exception. Encryption requires the file name to end with
        :data:`ENCRYPTED_EXTENSION`

        :raise FileError: If using ``crypt_key`` or ``password``, and the
            file does not have encrypted extension
        :param data: Data to write
        :type data: str or bytes
        :param crypt_key: Encryption key
        :type crypt_key: bytes
        :param password: Password (will use class salt)
        :type password: str
        """
        data = YAML.dumps(data)
        self.write(data, mode='w', crypt_key=crypt_key, password=password)

    def _write(self, data, mode='w'):
        with open(self, mode=mode) as f:
            f.write(data)

    def _write_compressed(self, content):
        if not isinstance(content, bytes):
            content = content.encode()
        with gzip.open(self, mode='wb') as f:
            f.write(content)

    def _write_encrypted(self,
                         content,
                         crypt_key=None):
        if not isinstance(content, bytes):
            content = content.encode()
        with open(self, mode='wb') as f:
            f.write(Crypt.encrypt(content, crypt_key))

    def _write_compressed_and_encrypted(self,
                                        content,
                                        crypt_key=None):
        if not isinstance(content, bytes):
            content = content.encode()
        with gzip.open(self, mode='wb') as f:
            f.write(Crypt.encrypt(content, crypt_key))

    def open(self, mode='r'):
        """
        Open file

        Returns a file handle by extending builtin ``open()``

        Intended use::

            fi = File('look_at_me.txt')
            with fi.open() as f:
                print(f.read()) # Do something more elaborate than this

            # This would also work (making this method rather useless)
            with open(fi) as f:
                print(f.read())

            # Better solution for this simple example
            print(fi.read())

        :param mode: File open mode
        :return: File handle
        """
        return open(self, mode=mode)

    def _is_binary(self, mode):
        return 'b' in mode

    def readlines(self, num_lines=1):
        """
        Read lines in file

        Does not work with encrypted files

        Intended use is reading the header of a file

        :param num_lines: Number of lines to read. Default is 1
        :return: First line as a string if ``num_lines=1``, or a list of
            strings for each line
        :rtype: str or list
        """
        if PIXIE and self.is_encrypted():
            raise PixieInPipeline(f'Cannot read lines in encrypted file')
        if self.is_compressed():
            return self._readlines_compressed(num_lines=num_lines)
        else:
            return self._readlines(num_lines=num_lines)

    def read(self, mode='r',
             crypt_key: bytes = None,
             password: str = None,
             *args, **kwargs):
        """
        Read file

        If file is encrypted, use either ``crypt_key`` or ``password``.
        None or both will raise an exception. Encryption requires the file
        name to end with :data:`ENCRYPTED_EXTENSION`

        :raises FileError: If trying to decrypt a file without
            :data:`ENCRYPTED_EXTENSION`
        :param mode: Read mode
        :param crypt_key: Encryption key
        :type crypt_key: bytes
        :param password: Password (will use class salt)
        :type password: str
        :return: Data as string or bytes depending on read mode
        :rtype: str or bytes
        """
        if not self.exists():
            raise FileError(f'Cannot read from file '
                            f'that does not exist: {self}')
        elif PIXIE and (crypt_key or password) and not \
                self.is_encrypted():
            raise PixieInPipeline(f'File does not have crypt extension '
                                  f'({self.ENCRYPTED_EXTENSION}), '
                                  f'but a crypt_key '
                                  f'or password was sent as input to write.')
        if self.is_encrypted():
            crypt_key = self._crypt_key(crypt_key=crypt_key, password=password)

        if self.is_compressed():
            if self.is_encrypted():
                data = self._read_compressed_and_encrypted(crypt_key)
                if 'b' not in mode:
                    data = data.decode()
            else:
                data = self._read_compressed(mode=mode)
                if 'b' not in mode:
                    data = data.decode()
        else:
            if self.is_encrypted():
                data = self._read_encrypted(crypt_key=crypt_key)
                if 'b' not in mode:
                    data = data.decode()
            else:
                data = self._read(mode=mode)

        return data

    def read_json(self,
                  crypt_key: bytes = None,
                  password: str = None,
                  **kwargs):
        """
        Read json file

        Extends :meth:`.File.read()` with :meth:`.JSON.loads()`

        :param crypt_key: Encryption key
        :type crypt_key: bytes
        :param password: Password (will use class salt)
        :type password: str
        :return: Dictionary of JSON content
        :rtype: dict
        """
        data = self.read(mode='r', crypt_key=crypt_key, password=password)
        return JSON.loads(data)

    def read_yaml(self,
                  crypt_key: bytes = None,
                  password: str = None,
                  **kwargs):
        """
        Read json file

        Extends :meth:`.File.read()` with :meth:`.YAML.loads()`

        :param crypt_key: Encryption key
        :type crypt_key: bytes
        :param password: Password (will use class salt)
        :type password: str
        :return: Dictionary of YAML content
        :rtype: dict
        """
        data = self.read(mode='r', crypt_key=crypt_key, password=password)
        return YAML.loads(data)

    def _read(self, mode='r'):
        with open(self, mode=mode) as f:
            return f.read()

    def _readlines(self, num_lines=1):
        with open(self, mode='r') as f:
            content = []
            for n in range(num_lines):
                content.append(f.readline().strip())
            if len(content) == 1:
                content = content[0]
        return content

    def _read_compressed(self,
                         mode='rb'):
        with gzip.open(self, mode=mode) as f:
            return f.read()

    def _readlines_compressed(self, num_lines=1):
        with gzip.open(self, mode='rt') as f:
            content = []
            for n in range(num_lines):
                content.append(f.readline().strip())
            if len(content) == 1:
                content = content[0]
        if not isinstance(content, str):
            if isinstance(content, list):
                for n in range(len(content)):
                    if isinstance(content[n], bytes):
                        content[n] = content[n].decode()
            elif isinstance(content, bytes):
                content = content.decode()

        return content

    def _read_encrypted(self, crypt_key):
        data = self._read(mode='rb')
        decrypted = Crypt.decrypt(data, crypt_key)
        return decrypted

    def _read_compressed_and_encrypted(self, crypt_key):
        with gzip.open(self, mode='rb') as f:
            data = f.read()
        decrypted = Crypt.decrypt(data, crypt_key)
        return decrypted

    # def make_new_name(self,
    #                   stub,
    #                   extension,
    #                   is_hidden=False,
    #                   is_compressed=False,
    #                   is_encrypted=False):
    #     pass

    def rename(self,
               new_name: str):
        """
        Rename file

        :param new_name: New file name, including extension
        :type new_name: str
        :return: A file path with the new file name
        :rtype: File
        """
        new_path = str(self.join(self.folder(), new_name))
        os.rename(self, new_path)
        self._rename(new_path)

    def folder(self):
        """
        Get the folder containing the file

        :return: Folder containing the file
        :rtype: Folder
        """
        return Folder(os.path.dirname(self))

    def move(self,
             new_folder: Folder,
             new_name=None,
             overwrite: bool = False):
        """
        Move file to a new folder, and with an optional new name

        :param new_folder: New folder
        :type new_folder: Folder
        :param new_name: New file name (optional). If missing, the file will
            keep the same name
        :return: Moved file
        :rtype: File
        """
        if not self.exists():
            raise FileError(f'Cannot move non existent file: {self}')
        if PIXIE and not overwrite:
            if self.folder() == new_folder:
                if new_name and new_name == self.name():
                    raise FileError(f'Cannot move a file to '
                                    f'the same name: {self}')
        new_folder.touch()
        if new_name:
            new_file = File.join(new_folder, new_name)
        else:
            new_file = File.join(new_folder, self.name())
        if not overwrite and new_file.exists():
            raise FileError(f'Target file already exists. '
                            f'Use overwrite=True to allow overwrite')
        if self.volume() == new_folder.volume():
            os.rename(self, new_file)
        else:
            shutil.move(self, new_file)
        self._rename(str(new_file))

    def copy(self,
             new_folder,
             new_name: str = None,
             overwrite: bool = False):
        """
        Copy file to a new folder, and optionally give it a new name

        :param overwrite: Set True to overwrite destination file if it exists
        :type overwrite: bool
        :param new_folder: New folder
        :type new_folder: Folder or str
        :param new_name: New file name (optional). If missing, the file will
            keep the same name
        :type new_name: str
        :return: Copied file
        :rtype: File
        """
        new_folder = Folder.glass(new_folder)
        if self.folder() == new_folder:
            raise FileError(f'Cannot copy a file '
                            f'to the same folder: {new_folder}')
        new_folder.touch()
        if new_name:
            new_file = File.join(new_folder, new_name)
        else:
            new_file = File.join(new_folder, self.name())
        if not overwrite and new_file.exists():
            raise FileError(f'Target file exists: {new_file}; '
                            f'Use overwrite=True to allow overwrite')
        shutil.copyfile(self, new_file)
        return new_file

    def compress(self,
                 delete_original: bool = True):
        """
        Compress file

        :param delete_original: If True, original file will be deleted after
            compression (default)
        :type delete_original: bool
        """
        if self.is_compressed():
            raise FileError(f'File already compressed: {self}')
        if self.is_encrypted():
            raise FileError(f'Cannot compress encrypted file: {self}. '
                            f'Decrypt file first')

        self.logger.debug(f'Compress file: {self}')
        old_size = self.size()
        new_file = File(f'{self}.gz')
        if new_file.exists():
            self.logger.warning(f'Overwrite existing gz-file: {new_file}')
        with open(self, 'rb') as f_in:
            with gzip.open(str(new_file), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        if delete_original:
            self.delete()
        new_file.compression_percent = 100 * (old_size - new_file.size()) \
                                       / old_size
        self.logger.debug(f'Compressed with compression '
                          f'{new_file.compression_percent:.2f}')
        self._rename(str(new_file))

    def decompress(self,
                   delete_original: bool = True,
                   replace_if_exists: bool = True):
        """
        Decompress file

        :param delete_original: If True, the original compressed file will be
            deleted after decompression
        :type delete_original: bool
        :param replace_if_exists: If True, the decompressed file will replace
            any already existing file with the same name
        :type replace_if_exists: bool
        """
        if not self.is_compressed():
            raise FileError(f'File is not compressed: {self}')
        if self.is_encrypted():
            raise FileError(f'Cannot decompress encrypted file: {self}. '
                            f'Decrypt file first.')
        self.logger.debug(f'Decompress file: {self}')
        new_file = File(
            str(self).replace('.' + self.COMPRESSED_EXTENSION, ''))
        if new_file.exists():
            if replace_if_exists:
                self.logger.debug(
                    'Overwrite existing file: {}'.format(new_file))
            else:
                raise FileError(f'File already exists: \'{new_file}\'. '
                                f'Use replace_if_exists=True to ignore.')
        with gzip.open(self, 'rb') as f_in:
            with open(new_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        if delete_original:
            self.delete()
        new_file = File.glass(new_file)
        new_file.compression_percent = None
        self._rename(str(new_file))

    def encrypt(self,
                crypt_key: bytes,
                delete_original: bool = True):
        """
        Encrypt file

        :raise FileError: If file is already encrypted or if crypt_key is
            missing
        :param crypt_key: Encryption key
        :type crypt_key: bytes
        :param delete_original: If True, the original unencrypted file will
            be deleted after encryption
        :type delete_original: bool
        """
        if self.is_encrypted():
            raise FileError(f'File is already encrypted: {self}')
        self.logger.debug(f'Encrypt file: {self}')
        encrypted_file = File(f'{self}.{self.ENCRYPTED_EXTENSION}')
        data = self._read(mode='rb')
        encrypted = Crypt.encrypt(data, crypt_key)
        encrypted_file._write(encrypted, mode='wb')
        if delete_original:
            self.delete()
        self._rename(str(encrypted_file))

    def decrypt(self,
                crypt_key: bytes,
                delete_original: bool = True):
        """
        Decrypt file

        :raise FileError: If file is not encrypted or if crypt_key is missing
        :param crypt_key: Encryption key
        :type crypt_key: bool
        :param delete_original: If True, the original encrypted file will
            be deleted after decryption
        :type delete_original: bool
        """
        if not self.is_encrypted():
            raise FileError(f'File is not encrypted: {self}')

        self.logger.debug(f'Decrypt file: {self}')
        decrypted_file = File(str(self).replace('.' +
                                                self.ENCRYPTED_EXTENSION, ''))
        data = self._read(mode='rb')
        decrypted = Crypt.decrypt(data, crypt_key)
        decrypted_file._write(decrypted, mode='wb')
        if delete_original:
            self.delete()
        self._rename(str(decrypted_file))


class Archive:
    """
    Zip file to gz conversion

    """

    # TODO: Add gz to zip
    # TODO: Add handling of multiple files and folders in archive

    @classmethod
    def is_zip(cls,
               file: File):
        """
        Check if input file is zip archive

        :param file: Input file
        :return: True if extension is 'zip', false if not
        :rtype: bool
        """
        extensions = file.extensions()
        return len(extensions) > 0 and extensions[-1] == 'zip'

    @classmethod
    def zip_to_gz(cls,
                  file: File,
                  delete_source_file: bool = True):
        """
        Convert zip file to gzip compressed file

        :param file: Input zip archive
        :param delete_source_file: Delete source file if True
        """

        if not cls.is_zip(file):
            raise ArchiveError(f'File is not zip-file: {file}')

        with zipfile.ZipFile(file, 'r') as zr:
            file_info = zr.filelist
            if len(file_info) > 1:
                raise ArchiveError(f'Multiple files in archive: {file}')
            elif len(file_info) == 0:
                raise ArchiveError(f'No files in archive: {file}')
            file_info = file_info[0]
            file_name = file_info.filename
            if '/' in file_name:
                file_name = file_name.split('/')[-1]
            if '\\' in file_name:
                file_name = file_name.split('\\')[-1]
            gz_file = File.join(file.folder(), file_name + '.gz')
            with zr.open(file_info, 'r') as zf:
                with gzip.open(gz_file, 'w') as gf:
                    shutil.copyfileobj(zf, gf)

        if delete_source_file:
            file.delete()

        return gz_file


HOME = Folder.glass(HOME)
