# ----------------------------------------------------------------------------
# Copyright (c) 2020 Ryan Volz
# All rights reserved.
#
# Distributed under the terms of the BSD 3-clause license.
#
# The full license is in the LICENSE file, distributed with this software.
#
# SPDX-License-Identifier: BSD-3-Clause
# ----------------------------------------------------------------------------
"""Utilities for persistent settings corresponding to Discord IDs."""
import collections
import os
import pathlib

import ruamel.yaml

__all__ = ("yaml", "DiscordIDSettings")

yaml = ruamel.yaml.YAML(typ="safe")
yaml.default_flow_style = False


def load_persistent_settings(path):
    """Load settings from a yaml file."""
    settings = collections.defaultdict(dict)
    if path.exists():
        with open(path, "r") as f:
            persistent = yaml.load(f)
        if persistent:
            settings.update(persistent)
    return settings


def dump_persistent_settings(path, settings):
    """Write settings to a yaml file."""
    if not path.parent.is_dir():
        os.makedirs(path.parent)
    with open(path, "w+") as f:
        # wrap settings with dict so we write a regular dict and not a defaultdict
        yaml.dump(dict(settings), f)


class DiscordIDSettings(object):
    """Class for managing related settings corresponding to Discord IDs."""

    def __init__(self, name, default_settings=None):
        """Initialize settings object for a given group/file name."""
        if default_settings is None:
            default_settings = {}
        self.name = name
        self.default_settings = default_settings

    def setup(self, bot):
        """Set up persistent settings for the bot."""
        # set up storage for settings and load from persistent file
        if not hasattr(bot, "storage"):
            # define a storage dictionary on the bot if no other extension has yet
            bot.storage = {}
        bot.storage[self.name] = {}
        settings_path = pathlib.Path(".settings", f"{self.name}.yml")
        bot.storage[self.name]["settings_path"] = settings_path
        bot.storage[self.name]["settings"] = load_persistent_settings(settings_path)

    def teardown(self, bot):
        """Tear down persistent settings for the bot."""
        # dump persistent storage to file
        dump_persistent_settings(
            bot.storage[self.name]["settings_path"], bot.storage[self.name]["settings"]
        )

    def get(self, bot, id, key, default=None):
        """Get value corresponding to ID from bot setting storage."""
        id_settings = bot.storage[self.name]["settings"][id]
        try:
            val = id_settings[key]
        except KeyError:
            try:
                val = self.default_settings[key]
            except KeyError:
                val = default
        return val

    def set(self, bot, id, key, val):
        """Set value corresponding to ID to bot setting storage."""
        bot.storage[self.name]["settings"][id][key] = val
