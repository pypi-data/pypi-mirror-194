import unittest
from openstack_cli.commands import login, logout
from click.testing import CliRunner
from openstack_cli.utils.config_tools import configtools



class TestLogoutLogin(unittest.TestCase):
    
    def test_login_logout(self):
        runner = CliRunner()
        runner.invoke(logout.cli)
        assert configtools.get("IS_LOGGEDIN") == False

        result = runner.invoke(login.cli,input="admin\nadminadmin")
        assert configtools.get("IS_LOGGEDIN") == True
