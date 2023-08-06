import unittest
from openstack_cli.commands import gift, logout, login
from click.testing import CliRunner
from openstack_cli.utils.config_tools import configtools
import requests
from tabulate import tabulate



class TestGifts(unittest.TestCase):

    def setUp(self):
        runner = CliRunner()
        runner.invoke(logout.cli)
        # configtools.list()
        assert configtools.get("IS_LOGGEDIN") == False

        result = runner.invoke(login.cli, input="admin\nadminadmin")
        # configtools.list()
        assert configtools.get("IS_LOGGEDIN") == True

    def test_gift_ls_a(self):
        runner = CliRunner()
        result = runner.invoke(gift.cli, ["ls", "-a"])

        res = requests.get("https://api.openstack.sh/api/templates/")
        res = res.json()
        # print(result.output)
        # print(res)
        lst = [[f"{x['slug']}:{x['id']}", x['description'],
                f"{x['price']}$", x['updated']] for x in res["results"]]
        headers = ["template", "description", "prices", "updated"]

        lst = sorted(lst, key=lambda l: l[0], reverse=False)
        lst = tabulate(lst, headers=headers, tablefmt="heavy_outline")
        assert result.output[:-1] == lst

    def test_gift_ls(self):
        runner = CliRunner()
        result = runner.invoke(gift.cli, ["ls"])

        cookies = {
            "access": configtools.get("ACCESS"),
            "refresh": configtools.get("REFRESH"),
            "username": configtools.get("USERNAME")
        }
        res = requests.get(
            "https://api.openstack.sh/api/users/templates/", cookies=cookies)
        res = res.json()
        lst = [[f"{x['slug']}:{x['id']}", x['description'],
                f"{x['price']}$", x['updated']] for x in res["results"]]
        headers = ["template", "description", "prices", "updated"]

        lst = sorted(lst, key=lambda l: l[0], reverse=False)
        lst = tabulate(lst, headers=headers, tablefmt="heavy_outline")

        assert result.output[:-1] == lst
