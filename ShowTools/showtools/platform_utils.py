import platform
import os

def get_os():
    return platform.system()

def get_default_install_path():
    if get_os() == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "ShowTools")
    elif get_os() == "Darwin":
        return os.path.join(os.environ["HOME"], "ShowTools")
    else:
        raise RuntimeError("Unsupported OS")