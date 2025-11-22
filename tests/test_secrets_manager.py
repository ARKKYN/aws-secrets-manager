import unittest
from unittest.mock import MagicMock, patch, mock_open, call
import os
import tempfile
from botocore.exceptions import ClientError
from secrets_manager.secrets_manager import SecretsManager

class TestSecretsManager(unittest.TestCase):

    def setUp(self):
        self.environment = "dev"
        self.service_name = "myservice"
        with patch("boto3.client") as mock_boto:
            self.secrets_manager = SecretsManager(self.environment, self.service_name)
            self.mock_client = self.secrets_manager.client

    def test_init(self):
        self.assertEqual(self.secrets_manager.environment, "DEV")
        self.assertEqual(self.secrets_manager.service_name, "MYSERVICE")
        self.assertEqual(self.secrets_manager.prefix, "/DEV/MYSERVICE/")

    def test_validate_inputs_valid(self):
        self.secrets_manager.validate_inputs()

    def test_validate_inputs_empty(self):
        self.secrets_manager.environment = ""
        with self.assertRaises(ValueError):
            self.secrets_manager.validate_inputs()

    def test_validate_inputs_slash(self):
        self.secrets_manager.environment = "dev/"
        with self.assertRaises(ValueError):
            self.secrets_manager.validate_inputs()

    def test_list_secrets(self):
        paginator = MagicMock()
        self.mock_client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [
            {"SecretList": [{"Name": "/DEV/MYSERVICE/SECRET1"}, {"Name": "/OTHER/SECRET"}]}
        ]
        
        secrets = self.secrets_manager.list_secrets()
        self.assertEqual(secrets, ["/DEV/MYSERVICE/SECRET1"])

    def test_list_secrets_error(self):
        self.mock_client.get_paginator.side_effect = ClientError({"Error": {"Code": "AccessDenied"}}, "list_secrets")
        with self.assertRaises(Exception):
            self.secrets_manager.list_secrets()

    def test_get_secret_value(self):
        self.mock_client.get_secret_value.return_value = {"SecretString": "value"}
        value = self.secrets_manager.get_secret_value("secret")
        self.assertEqual(value, "value")

    def test_get_secret_value_not_found(self):
        self.mock_client.get_secret_value.side_effect = ClientError({"Error": {"Code": "ResourceNotFoundException"}}, "get_secret_value")
        value = self.secrets_manager.get_secret_value("secret")
        self.assertIsNone(value)

    def test_get_secret_value_error(self):
        self.mock_client.get_secret_value.side_effect = ClientError({"Error": {"Code": "OtherError"}}, "get_secret_value")
        with self.assertRaises(Exception):
            self.secrets_manager.get_secret_value("secret")

    @patch("secrets_manager.secrets_manager.SecretsManager.list_secrets")
    @patch("secrets_manager.secrets_manager.SecretsManager.get_secret_value")
    def test_create_temp_env_file(self, mock_get_value, mock_list):
        mock_list.return_value = ["/DEV/MYSERVICE/KEY1"]
        mock_get_value.return_value = "VALUE1"
        
        file_path = self.secrets_manager.create_temp_env_file()
        self.assertTrue(os.path.exists(file_path))
        
        with open(file_path, "r") as f:
            content = f.read()
        
        self.assertIn("KEY1=VALUE1", content)
        os.remove(file_path)

    @patch("builtins.input", return_value="n")
    @patch("secrets_manager.secrets_manager.SecretsManager.list_secrets")
    def test_create_temp_env_file_no_secrets_no_create(self, mock_list, mock_input):
        mock_list.return_value = []
        with self.assertRaises(Exception):
            self.secrets_manager.create_temp_env_file()

    @patch("subprocess.run")
    def test_open_editor(self, mock_run):
        self.secrets_manager.open_editor("path")
        mock_run.assert_called_with(["vim", "path"], check=True)

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="KEY1=NEW_VALUE\nKEY2=VALUE2")
    @patch("secrets_manager.secrets_manager.SecretsManager.list_secrets")
    def test_update_secrets_from_file(self, mock_list, mock_file, mock_exists):
        mock_list.return_value = ["/DEV/MYSERVICE/KEY1", "/DEV/MYSERVICE/KEY3"]
        
        self.secrets_manager.update_secrets_from_file("dummy_path")
        
        # Check update
        self.mock_client.update_secret.assert_called_with(SecretId="/DEV/MYSERVICE/KEY1", SecretString="NEW_VALUE")
        
        # Check create
        self.mock_client.create_secret.assert_called_with(Name="/DEV/MYSERVICE/KEY2", SecretString="VALUE2")
        
        # Check delete
        self.mock_client.delete_secret.assert_called_with(SecretId="/DEV/MYSERVICE/KEY3", ForceDeleteWithoutRecovery=True)

if __name__ == "__main__":
    unittest.main()
