import os


def get_env_strict(key, raise_exception=True):
    try:
        return os.environ[key]
    except KeyError:
        print(f"Environment Variable: '{key}' Not Set ")
        if raise_exception:
            raise KeyError(f"Environment Variable: '{key}' Not Set")


def get_env(key, default_value=None):
    return os.getenv(key, default_value)
