import json
import os
import warnings

from distutils.util import strtobool
from dotenv import load_dotenv


class Config:
    DEFAULTS = dict(
        DEBUG=True,
        NEO4J_URI="bolt://localhost:7687",
        NEO4J_USER="neo4j",
        NEO4J_PASSWORD="neo4j",
        NEO4J_DEFAULT_DATABASE="neo4j",
        NEO4J_ENCRYPTED_CONNECTION=False,
    )

    def __init__(self, **kwargs):
        for k, v in self.DEFAULTS.items():
            if k in kwargs:
                v = kwargs[k]
            setattr(self, k, v)

    def _set_value(self, key, value):
        default_value = self.DEFAULTS[key]
        if value is not None and isinstance(default_value, bool) and not isinstance(value, bool):
            try:
                value = strtobool(value)
            except ValueError:
                value = None
        setattr(self, key, value)

    def feed_from_json_file(self, f):
        data = json.load(f)
        for k, v in data.items():
            if k in self.DEFAULTS:
                self._set_value(k, v)
            else:
                warnings.warn(f"Key '{k}' is not a valid configuration key, will be ignored", UserWarning)

    def feed_from_json_file_path(self, json_file_path):
        with open(json_file_path, "r") as f:
            self.feed_from_json_file(f)

    def feed_from_env_file(self, env_file=".env", override=True, set_null=False):
        load_dotenv(dotenv_path=env_file, override=override)
        self.feed_from_env(set_null=set_null)

    def feed_from_env(self, set_null=False):
        for k in self.DEFAULTS:
            v = os.getenv(k, None)
            if v or set_null:
                self._set_value(k, v)

    def __str__(self):
        return "\n".join(f"{k}={getattr(self, k, None)}" for k in self.DEFAULTS)


gconf = Config()
