#!/usr/bin/env python3
""" Parameterized and patch as deco """

from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ Class for Testing GHO Client """

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, input, mock_dt):
        """ Test that GHO.org returns the correct value """
        test = GithubOrgClient(input)
        test.org()
        mock_dt.assert_called_once_with(f'https://api.github.com/orgs/{input}')

    def test_public_repos_url(self):
        """ Test the result of public repos url is expected one """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_dt:
            payload = {"repos_url": "https://api.github.com/orgs/myorg/repos"}
            mock_dt.return_value = payload
            cl = GithubOrgClient('myorg')
            res = cl._public_repos_url
            self.assertEqual(res, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_json):
        """
            Testing repos list
            Testing mocked property and mocked_get_json
        """
        json_payload = [{"name": "Google"}, {"name": "Pinterest"}]
        mock_json.return_value = json_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock:
            mock.return_value = "Testing"
            tester = GithubOrgClient('test')
            res = tester.public_repos()

            self.assertEqual(res, [j["name"] for j in json_payload])

            mock.assert_called_once()
            mock_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """ Test that GithubOrgClient.has_license returns correct value """
        res = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(res, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration tests for GithubOrgClient """
    @classmethod
    def setUpClass(cls):
        """ Set up the class with mocked requests """
        cfg = {
            'return_value.json.side_effect': [
                cls.org_payload,
                cls.repos_payload,
                cls.org_payload,
                cls.repos_payload
            ]
        }

        cls.get_patcher = patch('requests.get', **cfg)

        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """ Testing public_repos method """
        cl = GithubOrgClient("google")

        self.assertEqual(cl.org, self.org_payload)
        self.assertEqual(cl.repos_payload, self.repos_payload)
        self.assertEqual(cl.public_repos(), self.expected_repos)
        self.assertEqual(cl.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """ Testing public repos method with License """
        cl = GithubOrgClient("google")

        self.assertEqual(cl.public_repos(), self.expected_repos)
        self.assertEqual(cl.public_repos("XLICENSE"), [])
        self.assertEqual(cl.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """ Stops patching """
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()