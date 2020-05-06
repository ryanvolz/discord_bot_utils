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
"""Utilities for Discord bot commands."""
import functools


async def acknowledge_command(ctx):
    """Add a thumbs up reaction to acknowledge a command."""
    emoji = "👍"
    await ctx.message.add_reaction(emoji)


def delete_command_message(delay=10, only_on_success=False):
    """Return command decorator that deletes the command message."""

    def decorator(command):
        @functools.wraps(command)
        async def wrapper(self, ctx, *args, **kwargs):
            ret = await command(self, ctx, *args, **kwargs)
            if not only_on_success or ret:
                await ctx.message.delete(delay=delay)
            return ret

        return wrapper

    return decorator
