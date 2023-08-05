"""Numpy extension commands."""

from typing import TYPE_CHECKING

from nxscli_np.commands.cmd_npmem import cmd_pnpmem
from nxscli_np.commands.cmd_npsave import cmd_pnpsave

if TYPE_CHECKING:
    import click

commands_list: list["click.Command"] = [cmd_pnpsave, cmd_pnpmem]
