import toml


def get_config() -> dict:
    return toml.load("config.toml")
