import os

#: Home folder. Default is '~/.mjooln'
HOME = os.getenv('MJOOLN__HOME', '~/.mjooln').replace('\\', '/')

#: Default values. Override by adding MJOOLN__ first, and put in environment
#: variables
DEFAULT = {
    'PIXIE': 'false',
    'MINIMUM_WORD_LENGTH': 1,
    'WORD_SEPARATOR': '__',
    'CLASS_SEPARATOR': '___',
    'COMPRESSED_EXTENSION': 'gz',
    'ENCRYPTED_EXTENSION': 'aes',
    'ZULU_TO_ISO': 'true',
    'TRUNK__PATH': os.path.join(HOME, 'trunk.yaml').replace('\\', '/'),
    'TRUNK__EXTENSION': 'yaml',
    'TRUNK__AUTO_SCAN': 'true',
    'TRUNK__AUTO_SCAN_FOLDERS': '',
}


def get_env(name):
    public_name = 'MJOOLN__' + name
    return os.getenv(public_name, DEFAULT[name])


#: When flag is set to 'true', the Pixie will slow down your code, but
#: in return be very picky about your mistakes
PIXIE = get_env('PIXIE') == 'true'

#: Minimum word length. Default is 1
MINIMUM_WORD_LENGTH = get_env('MINIMUM_WORD_LENGTH')

#: Word separator. Default is double underscore
WORD_SEPARATOR = get_env('WORD_SEPARATOR')

#: Class separator. Default is triple underscore
CLASS_SEPARATOR = get_env('CLASS_SEPARATOR')

#: Compressed (reserved) extension. Default is '.gz'
COMPRESSED_EXTENSION = get_env('COMPRESSED_EXTENSION')

#: Encrypted (reserved) extension. Default is '.aes'
ENCRYPTED_EXTENSION = get_env('ENCRYPTED_EXTENSION')

#: Flags converting Zulu to iso string when creating doc
ZULU_TO_ISO = get_env('ZULU_TO_ISO') == 'true'
