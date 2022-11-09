import unittest
from subprocess import Popen, PIPE, run
from unittest.mock import patch, Mock, call, mock_open

from pycli import execute_command, add_imports, main


class TestPycli(unittest.TestCase):
    def test_execute_command(self):
        self.assertEqual('aaabbb', execute_command('x = "bbb"; line + x', 'aaa'))

    def test_add_imports(self):
        self.assertEqual('import sys; sys.argv', add_imports('sys.argv'))

    def test_add_imports_with_dot(self):
        self.assertEqual('import os.path; os.path.join("tmp", "test")', add_imports('os.path.join("tmp", "test")'))

    @patch('pycli.print')
    @patch('pycli.sys', Mock(stdin=['line one', 'line_two']))
    def test_main_no_file(self, print_mock: Mock):
        main(['line.split()[0]'])
        self.assertListEqual([call('line'), call('line_two')], print_mock.call_args_list)

    @patch('pycli.print')
    @patch('pycli.open', mock_open(read_data='line one\nline_two'))
    def test_main_with_file(self, print_mock: Mock):
        main(['line.split()[0]', 'file'])
        self.assertListEqual([call('line'), call('line_two')], print_mock.call_args_list)

    def test_e2e(self):
        p = run(['python3 pycli.py "files = os.listdir(); list(filter(files, lambda x: line in x))"'],
                capture_output=True, text=True, input='pycli\ntest')
        self.assertEqual("['pycli.py']\n['tests.py']", p.stdout)


if __name__ == '__main__':
    unittest.main()
