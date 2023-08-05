"""Numpy extension plugins."""

from nxscli.iplugin import DPluginDescription

from nxscli_np.plugins.npmem import PluginNpmem
from nxscli_np.plugins.npsave import PluginNpsave

plugins_list: list[DPluginDescription] = [
    DPluginDescription("npsave", PluginNpsave),
    DPluginDescription("npmem", PluginNpmem),
]
