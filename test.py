import unittest
from unittest.mock import patch
from click.testing import CliRunner
from cpxctl import get


class TestCli(unittest.TestCase):

    @patch('cpxctl.get_details')
    @patch('cpxctl.get_servers')
    def test_get_all(self, mock_get_servers, mock_get_details):
        server = mock_get_servers()
        server.json.return_value = ['10.58.1.72']

        details = mock_get_details()
        details.json.return_value = {'cpu': '1%', 'memory': '2%', 'service': 'RoleService'}

        runner = CliRunner()
        result = runner.invoke(get, ['all'])
        print(result.output)
        assert '10.58.1.72' in result.output
        assert 'RoleService' in result.output
        assert '1%' in result.output
        assert '2%' in result.output

    @patch('cpxctl.get_details')
    @patch('cpxctl.get_servers')
    def test_get_service(self, mock_get_servers, mock_get_details):
        server = mock_get_servers()
        server.json.return_value = ['10.58.1.72']

        details = mock_get_details()
        details.json.return_value = {'cpu': '1%', 'memory': '2%', 'service': 'RoleService'}

        runner = CliRunner()
        result = runner.invoke(get, ['RoleService'])
        print(result.output)
        assert '10.58.1.72' in result.output
        assert 'RoleService' in result.output
        assert '1%' in result.output
        assert '2%' in result.output

    @patch('cpxctl.get_details')
    @patch('cpxctl.get_servers')
    def test_get_service_inexistent(self, mock_get_servers, mock_get_details):
        server = mock_get_servers()
        server.json.return_value = ['10.58.1.72']

        details = mock_get_details()
        details.json.return_value = {'cpu': '1%', 'memory': '2%', 'service': 'RoleService'}

        runner = CliRunner()
        result = runner.invoke(get, ['InexistentService'])
        print(result.output)
        assert '10.58.1.72' not in result.output
        assert 'RoleService' not in result.output

    @patch('cpxctl.get_details')
    @patch('cpxctl.get_servers')
    def test_get_unhealthy_when_cpu_greater_than_90(self, mock_get_servers, mock_get_details):
        server = mock_get_servers()
        server.json.return_value = ['10.58.1.72']

        details = mock_get_details()
        details.json.return_value = {'cpu': '91%', 'memory': '2%', 'service': 'RoleService'}

        runner = CliRunner()
        result = runner.invoke(get, ['RoleService'])
        print(result.output)
        assert "Unhealthy" in result.output

    @patch('cpxctl.get_details')
    @patch('cpxctl.get_servers')
    def test_get_unhealthy_when_memory_greater_than_90(self, mock_get_servers, mock_get_details):
        server = mock_get_servers()
        server.json.return_value = ['10.58.1.72']

        details = mock_get_details()
        details.json.return_value = {'cpu': '31%', 'memory': '92%', 'service': 'RoleService'}

        runner = CliRunner()
        result = runner.invoke(get, ['RoleService'])
        print(result.output)
        assert "Unhealthy" in result.output


if __name__ == '__main__':
    unittest.main()

