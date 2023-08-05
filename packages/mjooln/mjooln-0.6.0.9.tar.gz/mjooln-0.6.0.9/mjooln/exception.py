class MjoolnException(Exception):
    """
    Parent for all module specific exceptions
    """
    pass


class PixieInPipeline(MjoolnException):
    """
    Raised by code mistakes if environment variable
    ``MJOOLN__PIXIE_IN_PIPELINE='true'``
    """
    pass


class AngryElf(MjoolnException):
    """
    Raised when ``elf()`` is unable to figure out what you are trying to do.
    It usually does not take well to not being able to do magic
    """
    pass


class CryptError(MjoolnException):
    """
    Rased by :class:`.Crypt`, mainly when password or crypt_key is invalid
    """
    pass


class BadSeed(MjoolnException):
    """
    Raised by :class:`.Seed`
    """
    pass


class DicError(MjoolnException):
    """
    Raised by :class:`.Dic`
    """
    pass


class DocError(MjoolnException):
    """
    Raised by :class:`.Doc`
    """
    pass


class DocumentError(DocError):
    """
    Raised by :class:`.Document`
    """
    pass


class IdentityError(MjoolnException):
    """
    Raised by :class:`.Identity`
    """
    pass


class BadWord(MjoolnException):
    """
    Raised by :class:`.Word`
    """
    pass


class NotAnInteger(BadWord):
    """
    Raised by :class:`.Word` when trying to get an integer from a non-integer
    word
    """
    pass


class InvalidKey(MjoolnException):
    """
    Raised by :class:`.Key`
    """
    pass


class ZuluError(MjoolnException):
    """
    Raised by :class:`.Zulu`
    """
    pass


class AtomError(MjoolnException):
    """
    Raised by :class:`.Atom`
    """
    pass


class PathError(MjoolnException):
    """
    Raised by :class:`.Path`
    """
    pass


class FolderError(MjoolnException):
    """
    Raised by :class:`.Folder`
    """
    pass


class FileError(MjoolnException):
    """
    Raised by :class:`.File`
    """
    pass


class ArchiveError(MjoolnException):
    """
    Raised by :class:`.Archive`
    """
    pass


class StoreError(MjoolnException):
    """
    Raised by :class:`.Store`
    """
    pass