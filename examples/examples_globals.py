import json
import os


def get_temp_dir() -> str:
    return os.path.join(os.path.dirname(os.getcwd()), "Temp")


def _make_temp_dir() -> None:
    """Create a temporary directory for storing files."""
    os.makedirs(get_temp_dir(), exist_ok=True)


def _get_shared_data_file() -> str:
    return os.path.join(get_temp_dir(), "pysherlock_examples_shared_data.json")


def store_sherlock_tutorial_path(ansys_install_path: str) -> None:
    """Store the Sherlock tutorial path in a shared data file."""
    _make_temp_dir()
    data = {"sherlock_tutorial_path": os.path.join(ansys_install_path, "sherlock", "tutorial")}
    with open(_get_shared_data_file(), "w") as file:
        json.dump(data, file)


def get_sherlock_tutorial_path() -> str:
    """Retrieve the Sherlock tutorial path from the shared data file."""
    with open(_get_shared_data_file(), "r") as file:
        data = json.load(file)
    return data.get("sherlock_tutorial_path", "Not set")
