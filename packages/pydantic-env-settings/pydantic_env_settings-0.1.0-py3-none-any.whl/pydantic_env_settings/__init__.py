"""Wrapper around BaseSettings.

Sets the usage of the .env file as default.

Modifies the error description while parsing .env file:
    - marks it's a settings validation error
    - renames the field names by adding the env_prefix and uppercaseing it
    - gives hint about .env file

>>> class MySettings(EnvSettings):
...     filename: str
...     verbose: bool
...     class Config:
...         env_prefix = 'MY_'
>>> settings = MySettings()
Traceback (most recent call last):
...
pydantic_env_settings.SettingsError: 2 validation errors for MySettings
MY_FILENAME
  field required (type=value_error.missing)
MY_VERBOSE
  field required (type=value_error.missing)
<BLANKLINE>
Hint! Verify your environment setting or the '.env' file.
"""

from typing import Any, Union, Optional
from pathlib import Path
from pydantic import ValidationError
from pydantic.env_settings import BaseSettings, env_file_sentinel


class SettingsError(Exception):
    def __str__(self) -> str:
        return "{}\n\nHint! Verify your environment setting or the '{}' file.".format(*self.args)


class EnvSettings(BaseSettings):
    def __init__(
        __pydantic_self__,
        _env_file: Union[Path, str, None] = env_file_sentinel,
        _env_file_encoding: Optional[str] = None,
        _secrets_dir: Union[Path, str, None] = None,
        **values: Any
    ) -> None:
        try:
            super().__init__(_env_file, _env_file_encoding, _secrets_dir, **values)
        except ValidationError as err:
            cfg = err.model.__config__
            env_file = _env_file if _env_file != env_file_sentinel else cfg.env_file
            for e in err.raw_errors:
                e._loc = tuple(str.upper(cfg.env_prefix + x) for x in e.loc_tuple())
            raise SettingsError(err, env_file) from None

    class Config:
        env_file = ".env"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
