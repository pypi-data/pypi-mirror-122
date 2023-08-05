import base64
import json
import simplejson
import yaml
import logging
import string
import re
import uuid
import datetime
import pytz
import dateutil
import time
import signal
from threading import Event
from dateutil.parser import parse as dateparser
from collections import namedtuple

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from mjooln.environment import *
from mjooln.exception import *


class Crypt:
    """ Wrapper for best practice key generation and AES 128 encryption

    From `Fernet Docs <https://cryptography.io/en/latest/fernet/>`_:
    HMAC using SHA256 for authentication, and PKCS7 padding.
    Uses AES in CBC mode with a 128-bit key for encryption, and PKCS7 padding.
    """

    # TODO: Do QA on cryptographic strength

    @classmethod
    def generate_key(cls):
        """ Generates URL-safe base64-encoded random key with length 44 """
        return Fernet.generate_key()

    @classmethod
    def salt(cls):
        """ Generates URL-safe base64-encoded random string with length 24

        :return: bytes
        """

        # Used 18 instead of standard 16 since encode otherwise leaves
        # two trailing equal signs (==) in the resulting string
        return base64.urlsafe_b64encode(os.urandom(18))

    @classmethod
    def key_from_password(cls,
                          salt: bytes,
                          password: str):
        """ Generates URL-safe base64-encoded random string with length 44

        :type salt: bytes
        :type password: str
        :return: bytes
        """

        password = password.encode()  # Convert to type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    @classmethod
    def encrypt(cls,
                data: bytes,
                key: bytes):
        """ Encrypts input data with the given key

        :type data: bytes
        :type key: bytes
        :return: bytes
        """
        if key is None:
            raise CryptError(f'Encryption key missing, cannot encrypt')
        fernet = Fernet(key)
        return fernet.encrypt(data)

    @classmethod
    def decrypt(cls,
                data: bytes,
                key: bytes):
        """ Decrypts input data with the given key

        :type data: bytes
        :type key: bytes
        :return: bytes
        """
        if key is None:
            raise CryptError(f'Encryption key missing, cannot encrypt')
        fernet = Fernet(key)
        try:
            return fernet.decrypt(data)
        except InvalidToken as it:
            raise CryptError(f'Invalid token. Probably due to '
                             f'invalid password/key. Actual message: {it}')


class Glass:

    @classmethod
    def glass(cls, *args, **kwargs):
        """
        If input is a class instance, return instance. If not, call
        constructor with same input arguments
        """
        if args and len(args) == 1 and not kwargs and isinstance(args[0], cls):
            return args[0]
        else:
            return cls(*args, **kwargs)


class Math:
    """ Utility math methods

    """

    @classmethod
    def human_size(cls, size_bytes: int):
        """ Convert bytes to a human readable format

        :type size_bytes: int
        :return: Tuple of size as a float and unit as a string
        :rtype: (float, str)
        """
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        size = size_bytes
        power_labels = {0: '', 1: 'k', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return size, power_labels[n] + 'B'

    @classmethod
    def bytes_to_human(cls,
                       size_bytes: int,
                       min_precision=5):
        """
        Convert size in bytes to human readable string

        :param size_bytes: Bytes
        :param min_precision: Minimum precision in number of digits
        :return:
        """
        value, unit = cls.human_size(size_bytes=size_bytes)
        len_int = len(str(int(value)))
        if len_int >= min_precision or unit == 'B':
            len_dec = 0
        else:
            len_dec = min_precision - len_int
        return f'{value:.{len_dec}f} {unit}'


class Text:
    """ String utility functions
    """
    _CAMEL_TO_SNAKE = r'(?<!^)(?=[A-Z])'
    _SNAKE_TO_CAMEL = r'(.+?)_([a-z])'
    _RE_CAMEL_TO_SNAKE = re.compile(_CAMEL_TO_SNAKE)
    _RE_SNAKE_TO_CAMEL = re.compile(_SNAKE_TO_CAMEL)

    @classmethod
    def camel_to_snake(cls, camel: str):
        """
        Convert camel to snake::

            Text.camel_to_snake('ThisIsCamel')
                this_is_camel
        """
        return cls._RE_CAMEL_TO_SNAKE.sub('_', camel).lower()

    @classmethod
    def snake_to_camel(cls, snake: str):
        """
        Convert snake to camel::

            Text.snake_to_camel('this_is_snake')
                ThisIsSnake
        """
        # TODO: Implement regex instead
        return ''.join(x[0].upper() + x[1:] for x in
                       snake.split('_'))


class Seed:
    """
    Convenience methods for unique string representation of an object

    Object can be created with the method ``from_seed()``, but the method
    must be overridden in child class. ``find`` methods use the class variable
    ``REGEX``, which must also be overridden in child class

    If the seed has a fixed length, this can be specified in the class
    variable ``LENGTH``, and will speed up identification (or will it...)
    """

    #: Regex identifying seed must be overridden in child class
    REGEX = None

    #: If seed has a fixed length, override in child class
    LENGTH = None

    @classmethod
    def _search(cls, str_: str):
        if not cls.REGEX:
            raise BadSeed(f'_REGEX must be overridden in child class')
        return re.compile(cls.REGEX).search(str_)

    @classmethod
    def _exact_match(cls, str_: str):
        if not cls.REGEX:
            raise BadSeed(f'_REGEX must be overridden in child class')
        _regex_exact = rf'^{cls.REGEX}$'
        return re.compile(_regex_exact).match(str_)

    @classmethod
    def verify_seed(cls, str_: str):
        """
        Check if string is seed

        :raise BadSeed: If string is not seed
        :param str_: Seed to verify
        """
        if not cls.is_seed(str_):
            raise BadSeed(f'Sting is not seed: {str_}')

    @classmethod
    def is_seed(cls, str_: str):
        """
        Checks if input string is an exact match for seed

        :param str_: Input string
        :return: True if input string is seed, False if not
        """
        if cls.LENGTH and len(str_) != cls.LENGTH:
            return False
        return cls._exact_match(str_) is not None

    @classmethod
    def seed_in(cls, str_: str):
        """ Check if input string contains one or more seeds

        :param str_: String to check
        :type str_: str
        :return: True if input string contains one or more seeds, false if not
        """
        if cls._search(str_):
            return True
        else:
            return False

    @classmethod
    def find_seed(cls, str_: str):
        """
        Looks for and returns exactly one object from text

        Uses ``from_seed()`` to instantiate object from seed and will fail if
        there are none or multiple seeds.
        Use find_all() to return a list of identities in text, including
        an empty list if there are none

        :raise BadSeed: If none or multiple seeds are found in string
        :param str_: String to search for seed
        :type str_: str
        :return: Seed object
        """
        res = re.findall(cls.REGEX, str_)
        if len(res) == 1:
            return cls.from_seed(res[0])
        elif not res:
            raise BadSeed(
                f'No {cls.__name__} found in this text: \'{str_}\'; '
                f'Consider using find_seeds(), which will '
                f'return empty list if none are found.')
        else:
            raise BadSeed(
                f'Found {len(res)} instances of {cls.__name__} in this '
                f'text: \'{str_}\'; '
                f'Use find_all() to return a list of all instances'
            )

    @classmethod
    def find_seeds(cls,
                   str_: str):
        """ Finds and returns all seeds in text

        :type str_: str
        :return: List of objects
        """
        ids = re.findall(cls.REGEX, str_)
        return [cls.from_seed(x) for x in ids]

    @classmethod
    def from_seed(cls, str_: str):
        """
        Must be overridden in child class.

        Will create an object from seed

        :param str_: Seed
        :return: Instance of child class
        """
        raise BadSeed(f'Method from_seed() must be overridden '
                      f'in child class \'{cls.__name__}')

    def seed(self):
        """
        Get seed of current object.

        Default is ``str(self)``

        :return: :class:`Seed`
        """
        return str(self)


class Dic:
    """Enables child classes to mirror attributes and dictionaries

    Private variables start with underscore, and are ignored by default.

    .. note:: Meant for inheritance and not direct use, but can be initialized
        with a dictionary and will then serve as a struct, where keys can be
        accessed using dot notation

    Direct use example::

        dic = Dic(a=1, b=2, c='three')
        dic.to_dict()
            {'a': 1, 'b': 2, 'c': 'three'}
        dic.a
            1
        dic.b
            2
        dic.c
            'three'

        dic.c = 'four'
        dic.to_dict()
            {'a': 1, 'b': 2, 'c': 'four'}


    """
    _PRIVATE_STARTSWITH = '_'

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], dict):
                self.add(args[0])
            elif PIXIE:
                raise PixieInPipeline(
                    'Only allowed argument for constructor is '
                    'a dict. Use kwargs, or inheritance for customization')
        elif len(args) > 1 and PIXIE:
            raise PixieInPipeline(
                'Dic cannot be instantiated with multiple args, only '
                'kwargs. Use inheritance for customization')
        self.add(kwargs)

    @classmethod
    def from_dict(cls,
                  di: dict):
        """
        Create a new object from input dictionary
        """
        return cls(**di)

    def to_vars(self,
                ignore_private: bool = True):
        di = vars(self).copy()
        if ignore_private:
            pop_keys = [x for x in di if x.startswith(self._PRIVATE_STARTSWITH)]
            for key in pop_keys:
                di.pop(key)

        return di

    def to_dict(self,
                ignore_private: bool = True,
                recursive: bool = False):
        # TODO: Populate to_doc etc with recursive, same way as ignoreprivate
        """ Return dictionary with a copy of attributes

        :param ignore_private: Ignore private attributes flag
        :return: dict
        """
        di = self.to_vars(ignore_private=ignore_private)
        if recursive:
            for key, item in di.items():
                if isinstance(item, Dic):
                    di[key] = item.to_vars(ignore_private=ignore_private)
        return di

    def keys(self, ignore_private=True):
        dic = self.to_dict(ignore_private=ignore_private)
        return [str(x) for x in dic.keys()]

    def __repr__(self):
        di = self.to_vars()
        dicstr = []
        for key, item in di.items():
            dicstr.append(f'{key}={item.__repr__()}')
        dicstr = ', '.join(dicstr)
        return f'{type(self).__name__}({dicstr})'

    def _add_item(self, key, item, ignore_private=True):
        # Add item and ignore private items if ignore_private is set to True
        if not ignore_private or not key.startswith(self._PRIVATE_STARTSWITH):
            self.__setattr__(key, item)

    def _add_dict(self,
                  dic: dict,
                  ignore_private: bool = True):
        for key, item in dic.items():
            self._add_item(key, item, ignore_private=ignore_private)

    def add(self,
            dic: dict,
            ignore_private: bool = True):
        """ Add dictionary to class as attributes

        :param dic: Dictionary to add
        :param ignore_private: Ignore private attributes flag
        :return: None
        """
        self._add_dict(dic, ignore_private=ignore_private)

    # TODO: Consider always requiring equal
    def add_only_existing(self, dic, ignore_private=True):
        """ Add dictionary keys and items as attributes if they already exist
        as attributes

        :param dic: Dictionary to add
        :param ignore_private: Ignore private attributes flag
        :return: None
        """
        dic_to_add = {}
        for key in dic:
            if hasattr(self, key):
                dic_to_add[key] = dic[key]
        self._add_dict(dic_to_add, ignore_private=ignore_private)

    # TODO: Consider decprecation
    def force_equal(self, dic, ignore_private=True):
        """ Add all dictionary keys and items as attributes in object, and
        delete existing attributes that are not keys in the input dictionary

        :param dic: Dictionary to add
        :param ignore_private: Ignore private attributes flag
        :return: None
        """
        self._add_dict(dic, ignore_private=ignore_private)
        for key in self.to_dict(ignore_private=ignore_private):
            if key not in dic:
                self.__delattr__(key)

    def print(self,
              ignore_private=True,
              indent=4 * ' ',
              width=80,
              flatten=False,
              separator=WORD_SEPARATOR):
        """
        Pretty print object attributes in terminal

        :param ignore_private: Ignore private variables flag
        :param indent: Spacing for sub dictionaries
        :param width: Target width of printout
        :param flatten: Print as joined keys
        :param separator: Key separator when flattening
        """
        text = f'--{indent}[[ {type(self).__name__} ]]{indent}'
        text += (width - len(text)) * '-'
        print(text)
        if not flatten:
            dic = self.to_dict(ignore_private=ignore_private)
        else:
            dic = self.to_flat(sep=separator)
        self._print(dic, level=0)
        print(width * '-')

    def _print(self, dic, level=0, indent=4 * ' '):
        for key, item in dic.items():
            if isinstance(item, dict):
                print(level * indent + f'{key}: [dict]')
                self._print(item, level=level + 1)
            elif isinstance(item, Dic) and not isinstance(item, Seed):
                item = item.to_dict()
                print(level * indent + f'{key}: [{type(item).__name__}]')
                self._print(item, level=level + 1)
            else:
                print(level * indent + f'{key}: '
                                       f'[{type(item).__name__}] {item} ')

    def print_flat(self,
                   ignore_private=True,
                   separator=WORD_SEPARATOR):
        self.print(ignore_private=ignore_private,
                   separator=separator, flatten=True)

    # TODO: Move to flag in to_dict etc., and unflatten in from_dict etc
    # TODO: Replace sep with Key sep.
    # TODO: Require var names not to have double underscores
    # TODO: Figure out how to handle __vars__, what is the difference with _vars

    def to_flat(self,
                sep=WORD_SEPARATOR,
                ignore_private=True):
        """
        Flatten dictionary to top elements only by combining keys of
         sub dictionaries with the given separator

        :param sep: Separator to use, default is double underscore (__)
        :type sep: str
        :param ignore_private: Flags whether to ignore private attributes,
            identified by starting with underscore
        :return: Flattened dictionary
        :rtype: dict
        """
        di = self.to_dict(ignore_private=ignore_private)
        return self.flatten(di, sep=sep)

    @classmethod
    def from_flat(cls,
                  di_flat: dict,
                  sep=WORD_SEPARATOR):
        return cls.from_dict(cls.unflatten(di_flat,
                                           sep=sep))

    @classmethod
    def _flatten(cls, di: dict, parent_key='', sep=WORD_SEPARATOR):
        items = []
        for key, item in di.items():
            if parent_key:
                new_key = parent_key + sep + key
            else:
                new_key = key
            if isinstance(item, dict):
                items.extend(cls._flatten(item, new_key, sep=sep).items())
            else:
                items.append((new_key, item))
        return dict(items)

    @classmethod
    def flatten(cls, di: dict, sep=WORD_SEPARATOR):
        """
        Flattens input dictionary with given separator
        :param di: Input dictionary
        :param sep: Separator (default is \'__\')
        :return: Flattened dictionary
        :rtype: dict
        """
        return cls._flatten(di, sep=sep)

    @classmethod
    def unflatten(cls, di_flat: dict, sep=WORD_SEPARATOR):
        """
        Unflattens input dictionary using the input separator to split into
        sub dictionaries
        :param di_flat: Input dictionary
        :param sep: Separator (default is \'__\')
        :return: Dictionary
        :rtype: dict
        """
        di = dict()
        for flat_key, item in di_flat.items():
            keys = flat_key.split(sep)
            di_tmp = di
            for key in keys[:-1]:
                if key not in di_tmp:
                    di_tmp[key] = dict()
                di_tmp = di_tmp[key]
            di_tmp[keys[-1]] = item
        return di


class JSON:
    """Dict to/from JSON string, with optional human readable"""

    @classmethod
    def dumps(cls, di, human=True, sort_keys=False, indent=4 * ' '):
        """Convert from dict to JSON string

        :param di: Input dictionary
        :type di: dict
        :param human: Human readable flag
        :param sort_keys: Sort key flag (human readable only)
        :param indent: Indent to use (human readable only)
        :return: JSON string
        :rtype: str
        """
        if human:
            return simplejson.dumps(di, sort_keys=sort_keys, indent=indent)
        else:
            return json.dumps(di)

    @classmethod
    def loads(cls, json_string):
        """ Parse JSON string to dictionary

        :param json_string: JSON string
        :type json_string: str
        :return: Dictionary
        :rtype: dict
        """
        return simplejson.loads(json_string)

    @classmethod
    def to_yaml(cls, json_string):
        di = cls.loads(json_string)
        return YAML.dumps(di)


class YAML:

    @classmethod
    def dumps(cls, di: dict):
        """
        Convert dictionary to YAML string

        :param di: Input dictionary
        :type di: dict
        :return: YAML string
        :rtype: str
        """
        return yaml.safe_dump(di)

    @classmethod
    def loads(cls, yaml_str):
        """
        Convert YAML string to dictionary

        :param yaml_str: Input YAML string
        :type yaml_str: str
        :return: Dictionary
        :rtype: dict
        """
        return yaml.safe_load(yaml_str)

    @classmethod
    def to_json(cls, yaml_str, human=False):
        di = cls.loads(yaml_str)
        return JSON.dumps(di, human=human)


# TODO: Add zulu/key/identity as builtin? Alternatively optional with environment variable
class Doc(Dic):
    """
    Enables child classes to mirror attributes, dictionaries, JSON and
    YAML

    .. note:: ``to_doc`` and ``from_doc`` are meant to be overridden in
        child class if attributes are not serializable. Both methods are
        used by JSON and YAML conversions
    """

    @classmethod
    def from_doc(cls, doc: dict):
        """
        Convert input dictionary to correct types and return object

        .. note:: Override in child class to handle custom types

        :param doc: Dictionary with serializable items only
        :return: New Doc object instantiated with input dictionary
        :rtype: Doc
        """
        return cls.from_dict(doc)

    @classmethod
    def from_json(cls,
                  json_string: str):
        """
        Create :class:`Doc` from input JSON string
        :param json_string: JSON string
        :return: Doc
        """
        doc = JSON.loads(json_string=json_string)
        return cls.from_doc(doc)

    @classmethod
    def from_yaml(cls,
                  yaml_string: str):
        """
        Create :class:`Doc` from input YAML string
        :param yaml_string: YAML string
        :return: Doc
        """
        doc = YAML.loads(yaml_string)
        return cls.from_doc(doc)

    def add_yaml(self,
                 yaml_string: str,
                 ignore_private=True):
        """
        Convert input YAML string to dictionary and add to current object

        :param yaml_string: YAML string
        :return: Doc
        """
        dic = YAML.loads(yaml_string)
        self.add(dic, ignore_private=ignore_private)

    def add_json(self,
                 json_string: str,
                 ignore_private=True):
        """
        Convert input JSON string to dictionary and add to current object

        :param json_string: JSON string
        :return: Doc
        """
        dic = JSON.loads(json_string)
        self.add(dic, ignore_private=ignore_private)

    def to_doc(self):
        """
        Converts class attributes to dictionary of serializable attributes

        ..note:: Override in child class to handle custom types

        :param ignore_private: Ignore private flag
        :return: Dictionary of serialized objects
        """
        doc = self.to_dict(ignore_private=True)
        return doc

    def to_json(self, human: bool = False):
        """
        Convert object to JSON string
        :param human: Use human readable format
        :return: JSON string
        :rtype: str
        """
        doc = self.to_doc()
        return JSON.dumps(doc, human=human)

    def to_yaml(self):
        """
        Convert object to YAML string
        :return: YAML string
        :rtype: str
        """
        doc = self.to_doc()
        return YAML.dumps(doc)


class Tic:
    """
    Time counter

    Example::

        tic = Tic()

        (wait a bit)

        tic.toc()
            2.5361578464508057

        tic.toc('Elapsed time')
            'Elapsed time: 17.219 seconds'
    """

    def __init__(self):
        self.start_time = time.time()

    def elapsed_time(self):
        return time.time() - self.start_time

    def toc(self, text=''):
        if text:
            return f'{text}: {self.elapsed_time():.3f} seconds'
        else:
            return self.elapsed_time()

    def tac(self, min_sleep_s=1.0):
        remaining_time = min_sleep_s - self.elapsed_time()
        if remaining_time > 0:
            time.sleep(remaining_time)


class Word(Seed, Glass):
    """
    Defines a short string with limitations

    - Minimum length is set in Environment with default 1
    - Empty word is ``n_o_n_e``
    - Allowed characters are

        - Lower case ascii ``a-z``
        - Digits ``0-9``
        - Underscore ``_``

    - Underscore and digits can not be the first character
    - Underscore can not be the last character
    - Can not contain double underscore since it acts as separator for words
      in :class:`.Key`

    Sample words::

        'simple'
        'with_longer_name'
        'digit1'
        'longer_digit2'

    """
    logger = logging.getLogger(__name__)

    REGEX = r'(?!.*__.*)[a-z0-9][a-z_0-9]*[a-z0-9]'

    #: Allowed characters
    ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits + '_'

    #: Allowed first characters
    ALLOWED_STARTSWITH = string.ascii_lowercase + string.digits

    #: Allowed last characters
    ALLOWED_ENDSWITH = string.ascii_lowercase + string.digits

    NONE = 'n_o_n_e'

    @classmethod
    def is_seed(cls, str_: str):
        if len(str_) == 1:
            if MINIMUM_WORD_LENGTH > 1:
                return False
            else:
                return str_ in cls.ALLOWED_STARTSWITH
        else:
            return super().is_seed(str_)

    @classmethod
    def none(cls):
        """
        Return Word repesentation of ``None``

        :return: ``n_o_n_e``
        :rtype: Word
        """
        return cls(cls.NONE)

    @classmethod
    def from_int(cls, number):
        return cls(str(number))

    @classmethod
    def from_ints(cls, numbers):
        numstr = '_'.join([str(x) for x in numbers])
        return cls(numstr)

    @classmethod
    def check(cls, word: str):
        """
        Check that string is a valid word

        :param word: String to check
        :type word: str
        :return: True if ``word`` is valid word, False if not
        :rtype: bool
        """
        if len(word) < MINIMUM_WORD_LENGTH:
            raise BadWord(
                f'Element too short. Element \'{word}\' has '
                f'length {len(word)}, while minimum length '
                f'is {MINIMUM_WORD_LENGTH}')
        if not word[0] in cls.ALLOWED_STARTSWITH:
            raise BadWord(f'Invalid startswith. Word \'{word}\' '
                          f'cannot start with \'{word[0]}\'. '
                          f'Allowed startswith characters are: '
                          f'{cls.ALLOWED_STARTSWITH}')
        if not word[-1] in cls.ALLOWED_ENDSWITH:
            raise BadWord(f'Invalid endswith. Word \'{word}\' '
                          f'cannot end with \'{word[-1]}\'. '
                          f'Allowed endswith characters are: '
                          f'{cls.ALLOWED_ENDSWITH}')
        invalid_characters = [x for x in word if x not in
                              cls.ALLOWED_CHARACTERS]
        if len(invalid_characters) > 0:
            raise BadWord(
                f'Invalid character(s). Word \'{word}\' cannot '
                f'contain any of {invalid_characters}. '
                f'Allowed characters are: '
                f'{cls.ALLOWED_CHARACTERS}')
        if WORD_SEPARATOR in word:
            raise BadWord(
                f'Word contains word separator, which is '
                f'reserved for separating words in a Key.'
                f'Word \'{word}\' cannot contain '
                f'\'{CLASS_SEPARATOR}\'')

    @classmethod
    def elf(cls, word):
        """ Attempts to interpret input as a valid word

        .. warning: Elves are fickle

        :raises AngryElf: If input cannot be interpreted as Word
        :param word: Input word string or word class
        :type word: str or Word
        :rtype: Word
        """
        if isinstance(word, Word):
            return word
        elif cls.is_seed(word):
            return cls(word)
        else:
            _original = word
            if WORD_SEPARATOR in word:
                raise AngryElf(f'This looks more like a Key: \'{_original}\'; '
                               f'Try the Key.elf() not me. In case you '
                               f'didn\'t notice I\'m the Word.elf()')

            # Test camel to snake
            if ' ' not in word and '_' not in word:
                word = Text.camel_to_snake(word)
                if cls.is_seed(word):
                    return cls(word)
                word = _original

            word = word.replace('_', ' ')
            word = word.strip()
            word = word.replace(' ', '_')
            while '__' in word:
                word = word.replace('__', '_')
            word = Text.camel_to_snake(word)
            while '__' in word:
                word = word.replace('__', '_')
            if cls.is_seed(word):
                return cls(word)
            raise AngryElf(f'Cannot for the bleeding world figure out '
                           f'how to make an Element from this sorry '
                           f'excuse of a string: {_original}')

    def __init__(self, word: str):
        if PIXIE:
            try:
                self.check(word)
            except BadWord as ie:
                raise PixieInPipeline(f'Invalid word: {ie}') from ie
        else:
            if not self.is_seed(word):
                raise BadWord(f'Invalid word: {word}')
        self.__word = word

    def __str__(self):
        return self.__word

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __gt__(self, other):
        return str(self) > str(other)

    def __le__(self, other):
        return str(self) <= str(other)

    def __ge__(self, other):
        return str(self) >= str(other)

    def __hash__(self):
        return hash(self.__word)

    def __repr__(self):
        return f'Word(\'{self.__word}\')'

    @staticmethod
    def _int(element):
        try:
            return int(element)
        except ValueError:
            return None

    @classmethod
    def _is_int(cls, element):
        return cls._int(element) is not None

    def is_none(self):
        """
        Check if word is ``n_o_n_e``, i.e. word representation of ``None``

        :rtype: bool
        """
        return self.__word == self.NONE

    def is_int(self):
        """
        Check if word is an integer

        :rtype: bool
        """
        ints = self._ints()
        return len(ints) == 1 and ints[0] is not None

    def _elements(self):
        return self.__word.split('_')

    def _ints(self):
        return [self._int(x) for x in self._elements()]

    def index(self):
        """
        Get index of word

        :raises BadWord: If word is an integer and thus cannot have an index
        :return: 0 if word has no index, otherwise returns index
        :rtype: int
        """
        elements = self._elements()
        if len(elements) == 1:
            if self._is_int(elements[0]):
                raise BadWord(f'Word is an integer, cannot get index: {self}')
            return 0
        else:
            idx = elements[-1]
            if self._is_int(idx):
                return self._int(idx)
            else:
                return 0

    @classmethod
    def _is_numeric(cls, ints):
        return all(ints)

    def is_numeric(self):
        """
        Check if word is numeric, i.e. can be converted to integer

        :rtype: bool
        """
        return self._is_numeric(self._ints())

    def to_int(self):
        """
        Convert word to integer

        :raise NotAnInteger: If word is not an integer
        :rtype: int
        """
        ints = self._ints()
        if len(ints) == 1 and ints[0] is not None:
            return ints[0]
        else:
            raise NotAnInteger(f'Word is not an integer: {self}')

    def to_ints(self):
        """
        Convert word to list of integers

        :rtype: int
        """
        return self._ints()

    def increment(self):
        """
        Create a new word with index incremented

        Example::

            word = Word('my_word_2')
            word.increment()
                Word('my_word_3')

        :rtype: Word
        """
        elements = self._elements()
        if len(elements) == 1:
            if self._is_int(elements[0]):
                raise BadWord(f'Word is an integer and '
                              f'cannot be incremented: {self}')
            elements = elements + ['1']
        else:
            idx = self._int(elements[-1])
            if idx is None:
                elements += ['1']
            else:
                elements[-1] = str(idx + 1)
        return Word('_'.join(elements))


class Identity(Seed, Glass):
    """ UUID string generator with convenience functions

    Inherits str, and is therefore an immutable string, with a fixed format
    as illustrated below.

    Examples::

        Identity()
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

        Identity.is_in('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            True

        Identity.find_one('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

    """

    REGEX = r'[0-9A-F]{8}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{4}' \
            r'\_[0-9A-F]{12}'

    REGEX_CLASSIC = r'[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}' \
                    r'\-[0-9a-f]{12}'
    REGEX_COMPACT = r'[0-9a-f]{32}'
    LENGTH = 36

    @classmethod
    def from_seed(cls, seed: str):
        """
        Create Identity from seed string

        :rtype: Identity
        """
        return cls(seed)

    @classmethod
    def is_classic(cls, classic: str):
        """
        Check if string is uuid on classic format

        :rtype: bool
        """
        if len(classic) != 36:
            return False
        _regex_exact = rf'^{cls.REGEX_CLASSIC}$'
        return re.compile(_regex_exact).match(classic) is not None

    @classmethod
    def from_classic(cls, classic: str):
        """
        Create Identity from classic format uuid

        :rtype: Identity
        """
        classic = classic.replace('-', '_').upper()
        return cls(classic)

    @classmethod
    def is_compact(cls, compact: str):
        """
        Check if string is compact format uuid

        :rtype: bool
        """
        if len(compact) != 32:
            return False
        _regex_exact = rf'^{cls.REGEX_COMPACT}$'
        return re.compile(_regex_exact).match(compact) is not None

    @classmethod
    def from_compact(cls, compact: str):
        """
        Create identity from compact format uuid

        :rtype: Identity
        """
        compact = '_'.join([
            compact[:8],
            compact[8:12],
            compact[12:16],
            compact[16:20],
            compact[20:]
        ]).upper()
        return cls(compact)

    @classmethod
    def elf(cls, input):
        """
        Try to create an identity based on input

        :raises AngryElf: If an identity cannot be created
        :rtype: Identity
        """
        if isinstance(input, Identity):
            return input
        elif isinstance(input, str):
            if cls.is_seed(input):
                return cls(input)
            elif cls.is_classic(input):
                return cls.from_classic(input)
            elif cls.is_compact(input):
                return cls.from_compact(input)
            elif cls.is_classic(input.lower()):
                return cls.from_classic(input.lower())
            elif cls.is_compact(input.lower()):
                return cls.from_compact(input.lower())

            # Try to find one or more identities in string
            ids = cls.find_seeds(input)
            if len(ids) > 0:
                # If found, return the first
                return ids[0]
        raise IdentityError(
            f'This useless excuse for a string has no soul, '
            f'and hence no identity: \'{input}\''
        )

    def __init__(self,
                 identity: str = None):
        if not identity:
            identity = str(uuid.uuid4()).replace('-', '_').upper()
        elif not self.is_seed(identity):
            raise IdentityError(f'String is not valid identity: {identity}')
        self.__identity = identity

    def __str__(self):
        return self.__identity

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __gt__(self, other):
        return str(self) > str(other)

    def __le__(self, other):
        return str(self) <= str(other)

    def __ge__(self, other):
        return str(self) >= str(other)

    def __hash__(self):
        return hash(self.__identity)

    def __repr__(self):
        return f'Identity(\'{self.__identity}\')'

    def classic(self):
        """
        Return uuid string on classic format::

            Identity().classic()
                '18a9e538-3b5e-4442-b2b9-f728fbe8f240'

        :rtype: str
        """
        return self.__identity.replace('_', '-').lower()

    def compact(self):
        """
        Return uuid string on compact format::

            Identity().compact()
                '18a9e5383b5e4442b2b9f728fbe8f240'

        :rtype: str
        """
        return self.__identity.replace('_', '').lower()


class Key(Seed, Glass):
    """
    Defines key string with limitations:

    - Minimum length is 2
    - Allowed characters are:

        - Lower case ascii (a-z)
        - Digits (0-9)
        - Underscore (``_``)
        - Double underscore (``__``)

    - Underscore and digits can not be the first character
    - Underscore can not be the last character
    - The double underscore act as separator for :class:`.Word`
      in the key
    - Triple underscore is reserved for separating keys from other keys or
      seeds, such as in class :class:`.Atom`

    Sample keys::

        'simple'
        'with_longer_name'
        'digit1'
        'longer_digit2'
        'word_one__word_two__word_three'
        'word1__word2__word3'
        'word_1__word_2__word_3'

    """

    #: Allowed characters
    ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits + '_'

    #: Allowed first characters
    ALLOWED_STARTSWITH = string.ascii_lowercase

    #: Allowed last characters
    ALLOWED_ENDSWITH = string.ascii_lowercase + string.digits

    #: Regular expression for verifying and finding keys
    REGEX = rf'(?!.*{CLASS_SEPARATOR}.*)[a-z][a-z_0-9]*[a-z0-9]'

    def __init__(self,
                 key: str):
        if PIXIE:
            try:
                self.verify_key(key)
            except BadWord as ie:
                raise PixieInPipeline('Invalid word in key') from ie
            except InvalidKey as ik:
                raise PixieInPipeline('Invalid key') from ik
        if not self.is_seed(key):
            raise InvalidKey(f'Invalid key: {key}')
        self.__key = key

    def __str__(self):
        return self.__key

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __gt__(self, other):
        return str(self) > str(other)

    def __le__(self, other):
        return str(self) <= str(other)

    def __ge__(self, other):
        return str(self) >= str(other)

    def __hash__(self):
        return hash(self.__key)

    def __repr__(self):
        return f'Key(\'{self.__key}\')'

    def __iter__(self):
        for word in self.words():
            yield word

    @classmethod
    def verify_key(cls, key: str):
        """
        Verify that string is a valid key

        :param key: String to check
        :return: True if string is valid key, False if not
        """
        if not len(key) >= MINIMUM_WORD_LENGTH:
            raise InvalidKey(f'Key too short. Key \'{key}\' has length '
                             f'{len(key)}, while minimum length is '
                             f'{MINIMUM_WORD_LENGTH}')
        if CLASS_SEPARATOR in key:
            raise InvalidKey(f'Key contains word reserved as class '
                             f'separator. '
                             f'Key \'{key}\' cannot contain '
                             f'\'{CLASS_SEPARATOR}\'')
        if not key[0] in cls.ALLOWED_STARTSWITH:
            raise InvalidKey(f'Invalid startswith. Key \'{key}\' '
                             f'cannot start with \'{key[0]}\'. '
                             f'Allowed startswith characters are: '
                             f'{cls.ALLOWED_STARTSWITH}')

        words = key.split(WORD_SEPARATOR)
        for word in words:
            Word.check(word)

    @classmethod
    def from_words(cls, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                return cls(arg)
            elif isinstance(arg, tuple) or isinstance(arg, list):
                args = arg

        args = [str(x) for x in args]
        return cls(WORD_SEPARATOR.join(args))

    def words(self):
        """
        Return list of words in key (separated by double underscore)

        Example::

            key = Key('some_key__with_two__no_three_elements')
            key.words()
                ['some_key', 'with_two', 'three_elements']
            key.words()[0]
                Word('some_key)

        :returns: [:class:`.Word`]
        """
        return [Word(x) for x in self.__key.split(WORD_SEPARATOR)]

    def with_separator(self,
                       separator: str):
        """ Replace separator

        Example::

            key = Key('some__key_that_could_be__path')
            key.with_separator('/')
                'some/key_that_could_be/path'

        :param separator: Separator of choice
        :type separator: str
        :return: str
        """
        return separator.join([str(x) for x in self.words()])

    @classmethod
    def elf(cls, key):
        """ Attempts to create a valid key based on the input

        .. warning:: Elves are fickle

        :raise AngryElf: If a valid key cannot be created
        :param key: Input key string or key class
        :type key: str or Key
        :return: Key
        """
        if isinstance(key, Key):
            return key
        elif Key.is_seed(key):
            return cls(key)
        else:
            _original_class = None
            if not isinstance(key, str):
                _original_class = type(key).__name__
                key = str(key)

            _original = key
            if Key.is_seed(key):
                return cls(key)
            key = key.strip()
            if Key.is_seed(key):
                return cls(key)
            key = key.replace(' ', '_')
            if Key.is_seed(key):
                return cls(key)
            key = key.lower()
            if Key.is_seed(key):
                return cls(key)
            if _original_class:
                raise InvalidKey(f'Creating '
                                 f'a key from \'{_original_class}\' is, as '
                                 f'you should have known, not meant to be. '
                                 f'Resulting string was: {_original}')
            raise InvalidKey(f'I tried but no way I can make a key out of '
                             f'this excuse of a string: {_original}')


class Zulu(datetime.datetime, Seed, Glass):
    # TODO: Round to millisecond etc. And floor. Check Arrow how its done

    """
    Timezone aware datetime objects in UTC

    Create using constructor::

        Zulu() or Zulu.now()
            Zulu(2020, 5, 21, 20, 5, 31, 930343)

        Zulu(2020, 5, 12)
            Zulu(2020, 5, 12)

        Zulu(2020, 5, 21, 20, 5, 31)
            Zulu(2020, 5, 21, 20, 5, 31)

    :meth:`Seed.seed` is inherited from :class:`Seed` and returns a string
    on the format ``<date>T<time>u<microseconds>Z``, and is \'designed\'
    to be file name and double click friendly, as well as easily recognizable
    within some string when using regular expressions.
    Printing a Zulu object returns seed, and Zulu can be created using
    :meth:`from_seed`::

        z = Zulu(2020, 5, 12)
        print(z)
            20200512T000000u000000Z

        z.seed()
            '20200512T000000u000000Z'

        str(z)
            '20200512T000000u000000Z'

        Zulu.from_seed('20200512T000000u000000Z')
            Zulu(2020, 5, 12)

    For an `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_
    formatted string, use custom function::

        z = Zulu('20200521T202041u590718Z')
        z.iso()
            '2020-05-21T20:20:41.590718+00:00'

    Similarly, Zulu can be created from ISO string::

        Zulu.from_iso('2020-05-21T20:20:41.590718+00:00')
            Zulu(2020, 5, 21, 20, 20, 41, 590718)


    Inputs or constructors may vary, but Zulu objects are *always* UTC. Hence
    the name Zulu.

    Constructor also takes regular datetime objects, provided they have
    timezone info::

        dt = datetime.datetime(2020, 5, 23, tzinfo=pytz.utc)
        Zulu(dt)
            Zulu(2020, 5, 23, 0, 0, tzinfo=<UTC>)

        dt = datetime.datetime(2020, 5, 23, tzinfo=dateutil.tz.tzlocal())
        Zulu(dt)
            Zulu(2020, 5, 22, 22, 0, tzinfo=<UTC>)

    Zulu has element access like datetime, in addition to string convenience
    attributes::

        z = Zulu()
        print(z)
            20200522T190137u055918Z
        z.month
            5
        z.str.month
            '05'
        z.str.date
            '20200522'
        z.str.time
            '190137'

    Zulu has a method :meth:`delta` for timedelta, as well as :meth:`add`
    for adding timedeltas directly to generate a new Zulu::

        Zulu.delta(hours=1)
            datetime.timedelta(seconds=3600)

        z = Zulu(2020, 1, 1)
        z.add(days=2)
            Zulu(2020, 1, 3)

    For more flexible ways to create a Zulu object, see :meth:`Zulu.elf`

    """

    _ZuluStr = namedtuple('ZuluStr', [
        'year',
        'month',
        'day',
        'hour',
        'minute',
        'second',
        'microsecond',
        'date',
        'time',
        'seed',
    ])

    _FORMAT = '%Y%m%dT%H%M%Su%fZ'
    REGEX = r'\d{8}T\d{6}u\d{6}Z'
    LENGTH = 23

    ISO_REGEX_STRING = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-' \
                       r'(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):' \
                       r'([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-]' \
                       r'(?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    ISO_REGEX = re.compile(ISO_REGEX_STRING)

    ############################################################################
    # String methods
    ############################################################################

    @classmethod
    def is_iso(cls, st: str):
        """
        Check if input string is
        `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_

        Check is done using regex :data:`Zulu.ISO_REGEX`

        :param st: Maybe an ISO formatted string
        :return: True if input string is iso, False if not
        :rtype: bool
        """
        try:
            if cls.ISO_REGEX.match(st) is not None:
                return True
        except:
            pass
        return False

    ############################################################################
    # Timezone methods
    ############################################################################

    @classmethod
    def all_timezones(cls):
        """
        Returns a list of all allowed timezone names

        Timezone \'local\' will return a datetime object with local timezone,
        but is not included in this list

        Wrapper for :meth:`pytz.all_timezones`

        :return: List of timezones
        :rtype: list
        """
        return pytz.all_timezones

    @classmethod
    def _to_utc(cls, ts):
        return ts.astimezone(pytz.utc)

    @classmethod
    def _tz_from_name(cls, tz='utc'):
        if tz == 'local':
            tz = dateutil.tz.tzlocal()
        else:
            try:
                tz = pytz.timezone(tz)
            except pytz.exceptions.UnknownTimeZoneError as ue:
                raise ZuluError(f'Unknown timezone: \'{tz}\'. '
                                f'Use Zulu.all_timezones() for a list '
                                f'of actual timezones')
        return tz

    ############################################################################
    # Create methods
    ############################################################################

    @classmethod
    def now(cls,
            tz=None):
        """
        Overrides ``datetime.datetime.now()``. Equivalent to ``Zulu()``

        :raise ZuluError: If parameter ``tz`` has a value. Even if value is UTC
        :param tz: Do not use. Zulu is always UTC
        :return: Zulu
        """
        if tz:
            raise ZuluError(f'Zulu.now() does not allow input time zone info. '
                            f'Zulu is always UTC. Hence the name')
        return cls()

    @classmethod
    def _from_unaware(cls, ts, tz=None):
        if not tz:
            raise ZuluError('No timezone info. Set timezone to use '
                            'with \'tz=<timezone string>\'. \'local\' will '
                            'use local timezone info. Use '
                            'Zulu.all_timezones() for a list of actual '
                            'timezones')
        return ts.replace(tzinfo=cls._tz_from_name(tz))

    @classmethod
    def _elf(cls, ts, tz=None):
        # Takes a datetime.datetime object and adds the input tzinfo if
        # none is present
        if not ts.tzinfo:
            ts = cls._from_unaware(ts, tz=tz)
        return ts

    @classmethod
    def from_unaware(cls, ts, tz='utc'):
        """ Create Zulu from timezone unaware datetime

        :param ts: Unaware time stamp
        :type ts: datetime.datetime
        :param tz: Time zone, with 'utc' as default.
            'local' will use local time zone
        :rtype: Zulu
        """
        if ts.tzinfo:
            raise ZuluError(f'Input datetime already has '
                            f'time zone info: {ts}. '
                            f'Use constructor or Zulu.elf()')
        else:
            ts = cls._from_unaware(ts, tz=tz)
        return cls(ts)

    @classmethod
    def from_unaware_local(cls, ts):
        """
        Create Zulu from timezone unaware local timestamp

        :param ts: Timezone unaware datetime
        :type ts: datetime.datetime
        :rtype: Zulu
        """
        return cls.from_unaware(ts, tz='local')

    @classmethod
    def from_unaware_utc(cls, ts):
        """
        Create Zulu from timezone unaware UTC timestamp

        :param ts: Timezone unaware datetime
        :type ts: datetime.datetime
        :rtype: Zulu
        """
        return cls.from_unaware(ts, tz='utc')

    @classmethod
    def _parse_iso(cls,
                   iso: str):
        ts = dateparser(iso)
        if ts.tzinfo and str(ts.tzinfo) == 'tzutc()':
            ts = ts.astimezone(pytz.utc)
        return ts

    @classmethod
    def from_iso(cls,
                 str_: str,
                 tz=None):
        """
        Create Zulu object from ISO 8601 string

        :param iso: ISO 8601 string
        :param tz: Timezone string to use if missing in ts_str
        :return: Zulu
        :rtype: Zulu
        """
        ts = cls._parse_iso(str_)
        if tz and not ts.tzinfo:
            ts = cls._from_unaware(ts, tz)
        elif ts.tzinfo and tz:
            raise ZuluError(f'Timezone info found in ISO string as well as '
                            f'input timezone argument (tz). Keep tz=None, '
                            f'or use Zulu.elf()')
        elif not tz and not ts.tzinfo:
            raise ZuluError('No timezone info in neither ISO string '
                            'nor tz argument')
        return cls(ts)

    @classmethod
    def _parse(cls,
               ts_str: str,
               pattern: str):
        return datetime.datetime.strptime(ts_str, pattern)

    @classmethod
    def parse(cls,
              ts_str: str,
              pattern: str,
              tz=None):
        """Parse time stamp string with the given pattern

        :param ts_str: Timestamp string
        :type ts_str: str
        :param pattern: Follows standard
            `python strftime reference <https://strftime.org/>`_
        :param tz: Timezone to use if timestamp does not have timezone info
        :return: Zulu
        """
        ts = cls._parse(ts_str, pattern)
        if not ts.tzinfo:
            ts = cls._from_unaware(ts, tz=tz)
        elif tz:
            raise ZuluError('Cannot have an input timezone argument when '
                            'input string already has timezone information')
        return cls(ts)

    @classmethod
    def from_seed(cls, seed: str):
        """
        Create Zulu object from seed string

        :param seed: Seed string
        :rtype: Zulu
        """
        if not cls.is_seed(seed):
            raise ZuluError(f'String is not Zulu seed: {seed}')
        ts = cls._parse(seed, cls._FORMAT)
        ts = cls._from_unaware(ts, tz='utc')
        return cls(ts)

    @classmethod
    def _from_epoch(cls, epoch):
        ts = datetime.datetime.utcfromtimestamp(epoch)
        return ts.replace(tzinfo=pytz.UTC)

    @classmethod
    def from_epoch(cls, epoch):
        """
        Create Zulu object from UNIX Epoch

        :param epoch: Unix epoch
        :type epoch: float
        :return: Zulu instance
        :rtype: Zulu
        """
        ts = cls._from_epoch(epoch)
        return cls(ts)

    @classmethod
    def _fill_args(cls, args):
        if len(args) < 8:
            # From date
            args = list(args)
            args += (8 - len(args)) * [0]
            if args[1] == 0:
                args[1] = 1
            if args[2] == 0:
                args[2] = 1
            args = tuple(args)

        if args[-1] not in [None, 0, pytz.utc]:
            raise ZuluError(f'Zulu can only be UTC. '
                            f'Invalid timezone: {args[-1]}')

        args = list(args)
        args[-1] = pytz.utc
        return tuple(args)

    @classmethod
    def elf(cls, *args, tz='local'):
        """
        General input Zulu constructor

        Takes the same inputs as constructor, and also allows Zulu
        objects to pass through. If timeozone is missing it will assume the input
        timezone ``tz``, which is set to local as default

        It takes both seed strings and iso strings::

            Zulu.elf('20201112T213732u993446Z')
                Zulu(2020, 11, 12, 21, 37, 32, 993446)

            Zulu.elf('2020-11-12T21:37:32.993446+00:00')
                Zulu(2020, 11, 12, 21, 37, 32, 993446)

        It takes UNIX epoch::

            e = Zulu(2020, 1, 1).epoch()
            e
                1577836800.0
            Zulu.elf(e)
                Zulu(2020, 1, 1)

        It will guess the missing values if input integers are not a full date
        and/or time::

            Zulu.elf(2020)
                Zulu(2020, 1, 1)

            Zulu.elf(2020, 2)
                Zulu(2020, 2, 1)

            Zulu.elf(2020,1,1,10)
                Zulu(2020, 1, 1, 10, 0, 0)

        .. warning:: Elves are fickle

        :raise AngryElf: If an instance cannot be created from the given input
        :param args: Input arguments
        :param tz: Time zone to assume if missing. 'local' will use local
            time zone. Use :meth:`all_timezones` for a list of actual
            timezones. Default is 'local'
        :return: Best guess Zulu object
        :rtype: Zulu
        """
        ts = None
        if len(args) == 0:
            return cls()
        elif len(args) > 1:
            args = cls._fill_args(args)
            ts = datetime.datetime(*args)
            if not ts.tzinfo:
                ts = cls._from_unaware(ts, tz)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, Zulu):
                return arg
            elif isinstance(arg, datetime.datetime):
                # Add timzone if missing
                ts = cls._elf(arg, tz=tz)
                return cls(ts)
            elif isinstance(arg, float):
                return cls.from_epoch(arg)
            elif isinstance(arg, int):
                # Instantiate as start of year
                return cls(arg, 1, 1)
            elif isinstance(arg, str):
                if cls.is_seed(arg):
                    return cls.from_seed(arg)
                elif cls.is_iso(arg):
                    ts = cls._parse_iso(arg)
                    # Add timzone if missing
                    ts = cls._elf(ts, tz=tz)
                else:
                    raise ZuluError(f'String is neither zulu, nor ISO: {arg}. '
                                    f'Use Zulu.parse() and enter the format '
                                    f'yourself')
            else:
                raise ZuluError(f'Found no way to interpret input '
                                f'argument as Zulu: {arg} [{type(arg)}]')
        return cls(ts)

    @classmethod
    def range(cls,
              start=None,
              n=10,
              delta=datetime.timedelta(hours=1)):
        """Generate a list of Zulu of fixed intervals

        .. note:: Mainly for dev purposes. There are far better
            ways of creating a range of timestamps, such as using pandas.

        :param start: Start time Zulu, default is *now*
        :type start: Zulu
        :param n: Number of timestamps in range, with default 10
        :type n: int
        :param delta: Time delta between items, with default one hour
        :type delta: datetime.timedelta
        :rtype: [Zulu]
        """
        if not start:
            start = cls()
        return [Zulu.elf(start + x * delta) for x in range(n)]

    def __new__(cls, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            ts = datetime.datetime.utcnow()
            ts = ts.replace(tzinfo=pytz.UTC)
        elif len(args) == 1 and len(kwargs) == 0:
            arg = args[0]
            if isinstance(arg, str):
                raise ZuluError('Cannot instantiate Zulu with a string. Use '
                                'Zulu.from_iso(), Zulu.from_seed(), '
                                'Zulu.from_string() or Zulu.parse()')
            elif isinstance(arg, float):
                raise ZuluError(f'Cannot create Zulu object from a float: '
                                f'{arg}; If float is unix epoch, '
                                f'use Zulu.from_epoch()')
            elif isinstance(arg, Zulu):
                raise ZuluError(f'Input argument is already Zulu: {arg}. '
                                f'Use Zulu.glass() to allow passthrough')
            elif isinstance(arg, datetime.datetime):
                ts = arg
                if not ts.tzinfo:
                    raise ZuluError('Cannot create Zulu from datetime if '
                                    'datetime object does not have timezone '
                                    'info. Use Zulu.from_unaware()')
                ts = ts.astimezone(pytz.UTC)
            else:
                raise ZuluError(f'Unable to interpret input argument: '
                                f'{arg} [{type(arg).__name__}]')
        else:
            # Handle input as regular datetime input (year, month, day etc)
            try:
                ts = datetime.datetime(*args)
            except TypeError as te:
                raise ZuluError from te
            # Add timezone info if missing (assume utc, of course)
            if not ts.tzinfo:
                ts = ts.replace(tzinfo=pytz.UTC)

        # Create actual object
        args = tuple([ts.year, ts.month, ts.day,
                      ts.hour, ts.minute, ts.second,
                      ts.microsecond, ts.tzinfo])
        self = super(Zulu, cls).__new__(cls, *args)
        seed = self.strftime(self._FORMAT)
        self.str = self._ZuluStr(
            year=seed[:4],
            month=seed[4:6],
            day=seed[6:8],
            hour=seed[9:11],
            minute=seed[11:13],
            second=seed[13:15],
            microsecond=seed[16:22],
            date=seed[:8],
            time=seed[9:15],
            seed=seed,
        )
        return self

    def __str__(self):
        return self.str.seed

    def __repr__(self):
        times = [self.hour, self.minute, self.second]
        has_micro = self.microsecond > 0
        has_time = sum(times) > 0
        nums = [self.year, self.month, self.day]
        if has_time or has_micro:
            nums += times
        if has_micro:
            nums += [self.microsecond]
        numstr = ', '.join([str(x) for x in nums])
        return f'Zulu({numstr})'

    def epoch(self):
        """
        Get UNIX epoch (seconds since January 1st 1970)

        Wrapper for :meth:`datetime.datetime.timestamp`

        :return: Seconds since January 1st 1970
        :rtype: float
        """
        return self.timestamp()

    @classmethod
    def from_str(cls, st: str):
        """
        Converts seed or iso string to Zulu

        :param st: Seed or iso string
        :rtype: Zulu
        """
        if cls.is_seed(st):
            return cls.from_seed(st)
        elif cls.is_iso(st):
            return cls.from_iso(st)
        else:
            raise ZuluError(f'Unknown string format (neither seed nor iso): '
                            f'{st}; '
                            f'Use Zulu.parse() to specify format pattern and '
                            f'timezone')

    def iso(self, full=False):
        # TODO: Implement full flag
        """Create `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ string

        Example::

            z = Zulu(2020, 5, 21)
            z.iso()
                '2020-05-21T00:00:00+00:00'

            z.iso(full=True)
                '2020-05-21T00:00:00.000000+00:00'

        :param full: If True, pad isostring to full length when microsecond is
            zero, so that all strings returned will have same length (has
            proved an issue with a certain document database tool, which
            was not able to parse varying iso string length without help)
        :type full: bool
        :return: str
        """
        iso = self.isoformat()
        if full:
            if len(iso) == 25:
                iso = iso.replace('+', '.000000+')
        return iso

    def format(self, pattern):
        """
        Format Zulu to string with the given pattern

        Wrapper for :meth:`datetime.datetime.strftime`

        :param pattern: Follows standard
            `Python strftime reference <https://strftime.org/>`_
        :return: str
        """
        return self.strftime(pattern)

    def to_unaware(self):
        """
        Get timezone unaware datetime object in UTC

        :return: Timezone unaware datetime
        :rtype: datetime.datetime
        """
        return datetime.datetime.utcfromtimestamp(self.epoch())

    def to_tz(self, tz='local'):
        """ Create regular datetime with input timezone

        For a list of timezones use :meth:`.Zulu.all_timezones()`.
        'local' is also allowed, although not included in the list

        :param tz: Time zone to use. 'local' will return the local time zone.
            Default is 'local'
        :rtype: datetime.datetime
        """
        ts_utc = datetime.datetime.utcfromtimestamp(self.epoch())
        ts_utc = ts_utc.replace(tzinfo=pytz.UTC)
        return ts_utc.astimezone(self._tz_from_name(tz))

    def to_local(self):
        """ Create regular datetime with local timezone

        :rtype: datetime.datetime
        """
        return self.to_tz(tz='local')

    @classmethod
    def delta(cls,
              days=0,
              hours=0,
              minutes=0,
              seconds=0,
              microseconds=0,
              weeks=0):

        """Wrapper for :meth:`datetime.timedelta`

        :param days: Number of days
        :param hours: Number of hours
        :param minutes: Number of minutes
        :param seconds: Number of seconds
        :param microseconds: Number of microseconds
        :param weeks: Number of weeks
        :return: datetime.timedelta
        """
        return datetime.timedelta(days=days,
                                  hours=hours,
                                  minutes=minutes,
                                  seconds=seconds,
                                  microseconds=microseconds,
                                  weeks=weeks)

    def add(self,
            days=0,
            hours=0,
            minutes=0,
            seconds=0,
            microseconds=0,
            weeks=0):
        """
        Adds the input to current Zulu object and returns a new one

        :param days: Number of days
        :param hours: Number of hours
        :param minutes: Number of minutes
        :param seconds: Number of seconds
        :param microseconds: Number of microseconds
        :param weeks: Number of weeks

        :return: Current object plus added delta
        :rtype: Zulu
        """
        delta = self.delta(days=days,
                           hours=hours,
                           minutes=minutes,
                           seconds=seconds,
                           microseconds=microseconds,
                           weeks=weeks)
        return self + delta


class Atom(Doc, Seed, Glass):
    """
    Triplet identifier intended for objects and data sets alike

    Format: ``<zulu>___<key>___<identity>``

    :class:`.Zulu` represents t0 or creation time

    :class:`.Key` defines grouping of the contents

    :class:`.Identity` is a unique identifier for the contents

    Constructor initializes a valid atom, and will raise an ``AtomError``
    if a valid atom cannot be created based on input parameters.

    The constructor must as minimum have :class:`.Key` as input, although
    string version (seed) of key is allowed::

        atom = Atom('zaphod__ship_33__inventory')
        atom.key()
            'zaphod__ship_33__inventory'
        atom.zulu()
            Zulu(2020, 5, 22, 13, 13, 18, 179169, tzinfo=<UTC>)
        atom.identity()
            '060AFBD5_D865_4974_8E37_FDD5C55E7CD8'

    Output methods::

        atom
            Atom('zaphod__ship_33__inventory', zulu=Zulu(2020, 5, 22, 13, 13, 18, 179169), identity=Identity('060AFBD5_D865_4974_8E37_FDD5C55E7CD8'))

        str(atom)
            '20200522T131318u179169Z___zaphod__ship_33__inventory___060AFBD5_D865_4974_8E37_FDD5C55E7CD8'

        atom.seed()
            '20200522T131318u179169Z___zaphod__ship_33__inventory___060AFBD5_D865_4974_8E37_FDD5C55E7CD8'

        atom.to_dict()
            {
                'zulu': Zulu(2020, 5, 22, 13, 13, 18, 179169),
                'key': Key('zaphod__ship_33__inventory'),
                'identity': Identity('060AFBD5_D865_4974_8E37_FDD5C55E7CD8')
            }

    Atom inherits :class:`.Doc` and therefore has a ``to_doc()`` method::

        atom.to_doc()
            {
                'zulu': '2020-05-22T13:13:18.179169+00:00',
                'key': 'zaphod__ship_33__inventory',
                'identity': '060AFBD5_D865_4974_8E37_FDD5C55E7CD8'
            }

    The ``to_doc()`` is used for output to the equivalent ``to_json()`` and
    ``to_yaml()``, with equivalent methods for creating an instance from
    ``dict``, doc or a JSON or YAML file.

    When storing an atom as part of another dictionary,
    the most compact method would however be ``seed``, unless readability
    is of importance.

    """

    REGEX = r'\d{8}T\d{6}u\d{6}Z\_\_\_[a-z][a-z_0-9]*[a-z0-9]\_\_\_' \
            r'[0-9A-F]{8}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{12}'

    @classmethod
    def from_seed(cls,
                  seed: str):
        """ Creates an Atom from a seed string

        :param seed: A valid atom seed string
        :rtype: Atom
        """
        if not cls.is_seed(seed):
            raise AtomError(f'Invalid atom seed: {seed}')
        zulu, key, identity = seed.split(CLASS_SEPARATOR)
        return cls(key=Key(key),
                   zulu=Zulu.from_seed(zulu),
                   identity=Identity(identity))

    @classmethod
    def elf(cls, *args, **kwargs):
        """ Attempts to create an atom based on the input arguments

        .. warning:: Elves are fickle

        :raise AngryElf: If input arguments cannot be converted to Atom
        :rtype: Atom
        """
        if len(args) == 1 and not kwargs:
            arg = args[0]
            if isinstance(arg, Atom):
                return arg
            if isinstance(arg, Key):
                return cls(arg)
            elif isinstance(arg, str):
                if Key.is_seed(arg):
                    return cls(arg)
                elif cls.is_seed(arg):
                    return cls.from_seed(arg)
                else:
                    raise AtomError(f'This input string is nowhere near '
                                    f'what I need to create an Atom: {arg}')
            elif Key.is_seed(arg):
                return cls(arg)
            else:
                raise AtomError(f'How the fuck am I supposed to create an atom '
                                f'based on this ridiculous excuse for an '
                                f'input: {arg} [{type(arg)}]')
        elif len(args) == 0:
            if 'key' not in kwargs:
                raise AtomError(f'At the very least, give me a key to work '
                                f'on. You know, key as thoroughly described '
                                f'in class Key')
            key = Key.elf(kwargs['key'])
            identity = None
            zulu = None
            if 'identity' in kwargs:
                identity = Identity.elf(kwargs['identity'])
            if 'zulu' in kwargs:
                zulu = Zulu.elf(kwargs['zulu'])
            return cls(key,
                       zulu=zulu,
                       identity=identity)
        raise AtomError(f'This is rubbish. Cannot make any sense of this '
                        f'mindless junk of input: '
                        f'args={args}; kwargs={kwargs}')

    @classmethod
    def from_dict(cls,
                  di: dict):
        """
        Create :class:`Atom` from input dictionary

        :param di: Input dictionary
        :rtype: Atom
        """
        return cls(key=di['key'],
                   zulu=di['zulu'],
                   identity=di['identity'])

    def __init__(self,
                 key,
                 zulu: Zulu = None,
                 identity: Identity = None):
        """ Atom constructor

        :param key: Valid Key
        :param zulu: Valid Zulu or None
        :param identity: Valid Identity or None
        :raise AtomError: If key is missing or any arguments are invalid
        :rtype: Atom
        """
        super(Atom, self).__init__()
        if isinstance(key, str):
            if Key.is_seed(key):
                key = Key(key)
            elif Atom.is_seed(key):
                raise AtomError(f'Cannot instantiate Atom with seed. '
                                f'Use Atom.from_seed()')
            else:
                raise AtomError(f'Invalid key: {key} [{type(key).__name__}]')

        if not isinstance(key, Key):
            raise AtomError(f'Invalid key: [{type(key)}] {key}')

        if not zulu:
            zulu = Zulu()
        if not identity:
            identity = Identity()

        self.__zulu = zulu
        self.__key = key
        self.__identity = identity

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return CLASS_SEPARATOR.join([str(self.__zulu),
                                     str(self.__key),
                                     str(self.__identity)])

    def __repr__(self):
        return f'Atom(\'{self.__key}\', ' \
               f'zulu={self.__zulu.__repr__()}, ' \
               f'identity={self.__identity.__repr__()})'

    def __hash__(self):
        return hash((self.__zulu, self.__key, self.__identity))

    def __lt__(self, other):
        return (self.__zulu, self.__key, self.__identity) < \
               (other.__zulu, other.__key, other.__identity)

    def __gt__(self, other):
        return (self.__zulu, self.__key, self.__identity) > \
               (other.__zulu, other.__key, other.__identity)

    def key(self):
        """
        Get Atom Key

        :rtype: Key
        """
        return self.__key

    def zulu(self):
        """
        Get Atom Zulu

        :rtype: Zulu
        """
        return self.__zulu

    def identity(self):
        """
        Get Atom Identity

        :rtype: Identity
        """
        return self.__identity

    def to_dict(self,
                ignore_private: bool = True,
                recursive: bool = False):
        """ Get Atom dict

        Example from class documentantion::

            atom.to_dict()
                {
                    'zulu': Zulu(2020, 5, 22, 13, 13, 18, 179169),
                    'key': Key('zaphod__ship_33__inventory'),
                    'identity': Identity('060AFBD5_D865_4974_8E37_FDD5C55E7CD8')
                }

        :param ignore_private: Ignore private attributes (not relevant)
        :param recursive: Recursive dicts (not relevant)
        :rtype: dict

        """
        return {
            'zulu': self.__zulu,
            'key': self.__key,
            'identity': self.__identity,
        }

    def to_doc(self,
               ignore_private: bool = True):
        """ Get Atom as a serializable dictionary

        Example from class documentantion::

            atom.to_doc()
                {
                    'zulu': '2020-05-22T13:13:18.179169+00:00',
                    'key': 'zaphod__ship_33__inventory',
                    'identity': '060AFBD5_D865_4974_8E37_FDD5C55E7CD8'
                }

        :param ignore_private: Ignore private attributes (not relevant)
        :param recursive: Recursive dicts (not relevant)
        :rtype: dict

        """
        return {
            'zulu': self.__zulu.iso(),
            'key': self.__key.seed(),
            'identity': self.__identity.seed(),
        }

    @classmethod
    def from_doc(cls, doc: dict):
        """
        Create Atom from serializable dictionary

        :param doc: Dictionary with serialized objects
        :rtype: Atom
        """
        return cls(
            zulu=Zulu.from_iso(doc['zulu']),
            key=Key(doc['key']),
            identity=Identity(doc['identity']),
        )

    def with_sep(self,
                 sep: str):
        """ Atom seed string with custom separator

        Example::

            atom.with_sep('/')
                '20200522T131318u179169Z/zaphod__ship_33__inventory/060AFBD5_D865_4974_8E37_FDD5C55E7CD8'

        :param sep: Custom separator
        :rtype: str
        """
        return sep.join(str(self).split(CLASS_SEPARATOR))

    @classmethod
    def element_count(cls,
                      elements: int = None):
        """
        Count number of elements represented by element input

        For examples, see:

            :meth:`.Atom.key_elements()`
            :meth:`.Atom.date_elements()`
            :meth:`.Atom.time_elements()`

        :param elements: Element parameter
        :rtype: int
        """
        if elements is None or elements < 0:
            return 1
        else:
            return elements

    @classmethod
    def _elements(cls, parts, level, sep=''):
        if level == 0:
            return []
        elif level > 0:
            return parts[:level]
        else:
            return [sep.join(parts[:-level])]

    def key_elements(self, elements=None):
        """
        Get selected key elements

        Intented usage is creating sub folders for files with atom naming

        Examples::

            atom.key_elements(None)
                ['zaphod__ship_33__inventory']
            atom.element_count(None)
                1

            atom.key_elements(0)
                []
            atom.element_count(0)
                0

            atom.key_elements(2)
                ['zaphod', 'ship_33']
            atom.element_count(2)
                2

            atom.key_elements(-2)
                ['zaphod__ship_33']
            atom.element_count(-2)
                1

        :param elements: Elements
        :return: Elements
        :rtype: list
        """
        if elements is None:
            return [str(self.__key)]
        return self._elements(self.__key.words(), elements,
                              sep=WORD_SEPARATOR)

    def date_elements(self, elements=3):
        """
         Get selected date elements

         Intented usage is creating sub folders for files with atom naming

         Examples::

             atom.date_elements(None)
                 ['20200522']
             atom.element_count(None)
                 1

             atom.date_elements(0)
                 []
             atom.element_count(0)
                 0

             atom.date_elements(2)
                 ['2020', '05']
             atom.element_count(2)
                 2

             atom.date_elements(-2)
                 ['202005']
             atom.element_count(-2)
                 1

         :param elements: Elements
         :return: Elements
         :rtype: list
         """

        if elements is None:
            return [self.__zulu.str.date]
        return self._elements([self.__zulu.str.year,
                               self.__zulu.str.month,
                               self.__zulu.str.day], elements)

    def time_elements(self, elements=0):
        """
         Get selected time elements

         Intented usage is creating sub folders for files with atom naming

         Examples::

             atom.time_elements(None)
                 ['131318']
             atom.element_count(None)
                 1

             atom.time_elements(0)
                 []
             atom.element_count(0)
                 0

             atom.time_elements(2)
                 ['13', '13']
             atom.element_count(2)
                 2

             atom.time_elements(-2)
                 ['1313']
             atom.element_count(-2)
                 1

         :param elements: Elements
         :return: Elements
         :rtype: list
         """
        if elements is None:
            return [self.__zulu.str.time]
        return self._elements([self.__zulu.str.hour,
                               self.__zulu.str.minute,
                               self.__zulu.str.second], elements)


class Waiter:
    """
    Convenience class for waiting or sleeping
    """

    @classmethod
    def sleep(cls, seconds):
        """
        Simple sleep

        :param seconds: Seconds to sleep
        """
        time.sleep(seconds)

    def __init__(self, keyboard_interrupt=True):
        self._come = Event()
        if keyboard_interrupt:
            for sig in ('SIGTERM', 'SIGHUP', 'SIGINT'):
                signal.signal(getattr(signal, sig),
                              self._keyboard_interrupt)

    def wait(self, seconds):
        """
        Sleeps for the given time, can be aborted with :meth:`come` and
        exits gracefully with keyboard interrupt

        :param seconds: Seconds to wait
        :type seconds: float
        :return: True if interrupted, False if not
        :rtype: bool
        """
        self._come.clear()
        self._come.wait(seconds)
        return self._come.is_set()

    def _keyboard_interrupt(self, signo, _frame):
        self._come.set()

    def come(self):
        """
        Abort :meth:`wait`
        """
        self._come.set()
