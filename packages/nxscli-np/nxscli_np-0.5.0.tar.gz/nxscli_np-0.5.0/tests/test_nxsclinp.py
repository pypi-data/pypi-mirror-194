import nxscli_np
import nxscli_np.ext_commands
import nxscli_np.ext_plugins


def test_nxsclinp():
    assert nxscli_np.__version__

    assert isinstance(nxscli_np.ext_plugins.plugins_list, list)
    assert isinstance(nxscli_np.ext_commands.commands_list, list)
