import os
import shutil

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class HomepageCopier(BasePlugin):
    config_scheme = (
        ("src", config_options.Type(str, default="README.md")),
        ("dest", config_options.Type(str, default="docs/index.md")),
    )

    def clean_up(self):
        if os.path.exists(self.config["dest"]):
            os.remove(self.config["dest"])

    def on_config(self, config):
        self.clean_up()
        shutil.copy(self.config["src"], self.config["dest"])
        return config

    def on_post_build(self, config):
        self.clean_up()

    def on_build_error(self, error):
        self.clean_up()
