import os


DEFAULT_HELLO_NAME = os.environ.get(
    "DEFAULT_HELLO_NAME",
    default="world"
)

DEFAULT_VERSION_FILENAME = os.environ.get(
    "DEFAULT_VERSION_FILENAME",
    default="VERSION"
)
