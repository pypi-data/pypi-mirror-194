import click
import os
import json


class ConfigTools:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def load_configs(self):
        """load configs from file."""
        with open(f"{os.path.join(os.path.dirname(__file__),'..','config','config.json')}", "r") as file:
            data = json.loads(file.read())
        return data

    def check(self, key):
        data = self.load_configs()
        if key in data:
            return True
        return False

    def set(self, key, value):
        data = self.load_configs()
        data[key] = value
        with open(f"{os.path.join(os.path.dirname(__file__),'..','config','config.json')}", "w") as file:
            json.dump(data, file, indent=4)

    def get(self, key):
        if self.check(key):
            data = self.load_configs()
            return data[key]

        return f"{key} is not exist"

    def list(self):
        data = self.load_configs()
        for key in data:
            click.echo(f"{key}={data[key]}")

    def is_loggedin(self):
        data = self.load_configs()
        return data["IS_LOGGEDIN"]


configtools = ConfigTools()
