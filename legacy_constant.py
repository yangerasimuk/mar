class Constant:
    META_FILE_SUFFIX = ".mar.txt"
    MAR_DIRECTORY_NAME = "./.mar"
    MAR_IGNORE_FILE_NAME = ".marignore"
    MAR_IGNORE_DIRECTORY_NAMES = [".git", ".mar", "Trash", "#recycle", ".DS_Store", "@eaDir", "@tmp", ".TemporaryItems"]
    TAGS_PATH_FILE_NAME = "./.mar/tags.path.mar.txt"

    # Поменять на MAR_DIRECTORY_NAME
    INDEX_DIRECTORY_NAME = "./.mar"
    INDEX_FILE_NAME = "./.mar/index.mar.txt"
    SYSTEM_FILE_PREFIX = "."
    CURRENT_DIRECTORY_NAME = "."
    PARENT_DIRECTORY_NAME = ".."
    SYSTEM_DIRECTORY_PREFIX = "."
    PYTHON_DIRECTORY_PREFIX = "_"
    SYSTEM_FILES = [".DS_Store", ".localized"]

    # Messages
    MESSAGE_NO_ADS_FILES = "No files with streams (NTFS ADS)"

    # KVO tags
    TAG_KEY_SYSTEM_UUID = "uuid"
    TAG_KEY_SYSTEM_SOURCE_CREATED_DATETIME = "source_created"
    TAG_KEY_SYSTEM_META_MODIFIED_DATETIME = "meta_modified"
    FINDER_PRINT_TAG_HIDDEN_KEYS = [TAG_KEY_SYSTEM_UUID, TAG_KEY_SYSTEM_SOURCE_CREATED_DATETIME, TAG_KEY_SYSTEM_META_MODIFIED_DATETIME]

    # Date
    TAG_VALUE_SYSTEM_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
