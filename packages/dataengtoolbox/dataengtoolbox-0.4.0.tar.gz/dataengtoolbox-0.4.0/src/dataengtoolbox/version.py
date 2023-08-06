import os

from dataengtoolbox.settings import DEFAULT_VERSION_FILENAME


version_filepath = os.path.join(
    os.path.dirname(__file__),
    DEFAULT_VERSION_FILENAME,
)

with open(version_filepath, "r") as version_file_handler:
    version = version_file_handler.read().strip()
