import os


def get_root_password():
    """Get the value of the ROOT_PASSWORD environment variable.
    
    Returns:
        str: The value of the ROOT_PASSWORD environment variable.
    """
    return os.environ.get("ROOT_PASSWORD")
