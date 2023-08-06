import shutil
from getpass import getpass
from pathlib import Path
from configparser import ConfigParser

from .crypt import salt_and_hash


DEFAULT_CFG_FILE = Path.home() / ".config" / "radicale" / "config"


def init_password_store():
    check_config()

    password = getpass()
    confirm = getpass("Re-enter password to confirm: ")

    if password != confirm:
        raise ValueError("Password does not match. Try again.")

    secret = salt_and_hash(password)
    save_config(secret)


def get_config():
    config = ConfigParser()
    assert DEFAULT_CFG_FILE.exists(), f"Config file {DEFAULT_CFG_FILE} not found!"
    config.read(DEFAULT_CFG_FILE)
    return config


def check_config():
    config = get_config()
    assert not config.has_section("auth"), (
        f"An authentication method already exists in {DEFAULT_CFG_FILE}!"
    )


def save_config(secret):
    r"""Append the authentication secret to config

    .. code-block::conf

        [auth]
        type = radicale_auth_sh
        secret = $argon2id$v=19$m=102400,t=2,p=8$tSm+JOWigOgPZx/g44K5fQ$WDyus6py50bVFIPkjA28lQ

    """
    config = get_config()
    for sect in config.sections():
        config.remove_section(sect)

    config.add_section("auth")
    config.set(section="auth", option="type", value="radicale_auth_sh")
    config.set(section="auth", option="secret", value=secret)

    shutil.copy2(DEFAULT_CFG_FILE, DEFAULT_CFG_FILE.with_suffix(".old"))

    # Append auth section
    with DEFAULT_CFG_FILE.open("a") as fp:
        config.write(fp)

    print(f"Password salted and stored in {DEFAULT_CFG_FILE}")
