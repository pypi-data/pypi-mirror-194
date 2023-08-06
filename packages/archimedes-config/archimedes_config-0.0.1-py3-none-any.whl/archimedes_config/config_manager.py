"""
Class declaration for secret manager
"""
import logging
from typing import Any, Dict, Union

import toml
from cryptography.fernet import Fernet


class ConfigManager:
    """
    Manages Secrets
    """

    def __init__(
        self, path: str = None, default_key=None, decrypt_on_load: bool = False
    ) -> None:
        """Init for secret handler

        Arguments:
            path (str|path): Path to the config file
            default_key (str): Default secret key to use for encryption / decryption
            decrypt_on_load (bool): Decrypt the config on load
        """
        self._secrets = None  # Loaded secrets
        self.secrets_loaded_from = (
            None  # Path secrets loaded from. Used as default saving location.
        )
        self._default_key = None  # Default key

        # Records changes in Secret.
        # Used to warn if secrets have not been saved.
        self._secret_changed = False

        self._is_secret_encrypted = None  # Encryption state of secrets
        self.secret_loaded = False  # Has secrets been loaded

        # if path, set load the config
        if path:
            self.load(path=path)

        # if default key is set, set the key
        if default_key:
            self.set_default_key(default_key)

        if decrypt_on_load:
            self.decrypt_secrets()

    def __repr__(self) -> str:
        """
        Shows state of secrets
        Encrypted secrets will not be print encrypted

        :return:
        """
        print_data = {}
        for group, keys in self.secret.items():
            print_data[group] = {}
            for key, data in keys.items():
                print_data[group][key] = {}
                for field, value in data.items():
                    print_data[group][key][field] = (
                        "***ENCRYPTED***"
                        if (
                            field == "value"
                            and data.get("is_encrypted", False)
                            and not self.is_secret_encrypted
                        )
                        else value
                    )
        print_data = self.format_toml(print_data)
        return print_data

    def __del__(self) -> None:
        if self._secret_changed:
            logging.warning("WARNING: Changes to secret has not been discarded.")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__del__()

    @property
    def secret_changed(self) -> bool:
        """Checks if any values in secret has been changed"""
        return self._secret_changed

    @property
    def is_secret_encrypted(self) -> bool:
        """Checks the state of encryption if secret"""
        return self._is_secret_encrypted

    @property
    def default_key(self) -> str:
        """Returns remote key in AZ key vault"""
        if not self._default_key:
            raise ValueError("Default key has not been set.")
        return self._default_key

    @property
    def secret(self) -> Dict:
        """Returns secret"""
        if self._secrets:
            return self._secrets
        raise ValueError("Secret has not been loaded.")

    def set_default_key(self, key):
        """Sets a default key"""

        if self._default_key:
            raise ValueError("Default key has already been set.")
        self._default_key = key

    def format_toml(self, toml_data: Dict = None):
        """
        Formats input toml into pretty format
        :param toml_data: Dict representation of toml
        :return:
        """
        if toml_data is None:
            toml_data = self.secret
        formatted_toml = []
        for group, keys in toml_data.items():
            formatted_toml.append(f"[{group}]")
            for key, value in keys.items():
                formatted_toml.append(f"\t[{group}.{key}]")

                is_encrypted = value.get("is_encrypted", False)
                is_encrypted = "true" if is_encrypted else "false"
                formatted_toml.append(f"\tis_encrypted = {is_encrypted}")

                value = value["value"]
                if isinstance(value, str):
                    value = f'"{value}"'
                elif isinstance(value, bool):
                    value = "true" if value else "false"
                formatted_toml.append(f"\tvalue = {value}\n")

        return "\n".join(formatted_toml)

    def get(self, group: str, item: str, *, default_return=KeyError) -> Any:
        """
        Returns value for the key
        :param group: Name of group the key belongs to
        :param item: Name of key to extract
        :param default_return: Returns this value if key does not exist in secret
        :return:
        """
        try:
            key_meta = self.secret[group][item]
        except KeyError as err:
            if default_return == KeyError:
                raise err
            return default_return
        if key_meta.get("is_encrypted", False) and self.is_secret_encrypted:
            raise ValueError("Secret has not been decrypted.")
        return self.secret[group][item]["value"]

    def _encrypt_value(self, is_encrypted: bool, value: Any, key: str = None):
        """
        Encrypts a single value
        :param is_encrypted: If true, encrypts
        :param value: value to encrypt
        :param key:
        :return:
        """
        key = key if key else self.default_key
        if is_encrypted:
            value = Fernet(key).encrypt(value.encode()).decode()
        if value is None:
            value = ""
        return value

    def _decrypt_value(self, is_encrypted: bool, value, key: str = None):
        """
        Decrypts a value
        :param is_encrypted: If true decrypts
        :param value: Valur to decrypt
        :return:
        """
        key = key if key else self.default_key
        if is_encrypted:
            value = Fernet(key).decrypt(value).decode()
        if value == "":
            value = None
        return value

    def save(self, path: str = None, allow_saving_decrypted: bool = False) -> None:
        """
        Save secret into a toml file
        :param path:
            Path to save the secrets to
            Defaults to the path the secrets were loaded from
        :param allow_saving_decrypted:
            If true, allows saving decrypted secrets
        :return:
        """
        if not self.is_secret_encrypted:
            if not allow_saving_decrypted:
                raise ValueError(
                    "Saving decrypted secrets is not allowed."
                    "Set `allow_saving_decrypted` to True to save decrypted secrets."
                )
        if path is None:
            if not self.secrets_loaded_from:
                raise ValueError("Both default path and specific path not set.")
            path = self.secrets_loaded_from
        data = self.secret.copy()
        data["CONFIGURATIONS"]["_IS_CONFIG_ENCRYPTED"][
            "value"
        ] = self.is_secret_encrypted

        formatted_toml = self.format_toml()
        with open(path, "w", encoding="utf8") as file:
            file.write(formatted_toml)
        self._secret_changed = False

    def new_secret(self):
        """
        Initializes a new unencrypted secret
        """
        if self._secrets:
            raise ValueError("Secrets has already been loaded.")
        self._secrets = {"CONFIGURATIONS": {"_IS_CONFIG_ENCRYPTED": {"VALUE": False}}}
        self._is_secret_encrypted = False
        self.secret_loaded = True
        self._secret_changed = True

    def load(self, path="config.toml"):
        """
        Loads an environment toml file
        :param path: path to the toml file to read secrets from
        :return:
        """
        if self.secret_loaded:
            raise ValueError("Secret has already been loaded.")
        self.secret_loaded = True
        self.secrets_loaded_from = path
        self._secret_changed = False
        config = toml.load(path)
        for _, keys in config.items():
            for field, content in keys.items():
                if "value" in content:
                    continue
                raise ValueError(
                    f"Invalid toml file. "
                    f"Header {field} doesnt have `value` or `is_encrypted` field."
                )

        self._is_secret_encrypted = config["CONFIGURATIONS"]["_IS_CONFIG_ENCRYPTED"][
            "value"
        ]
        self._secrets = config

    def list_groups(self):
        """Returns groups"""
        return list(self.secret.keys())

    def list_secrets(self, group: str):
        """Returns list of keys in secret"""
        return list(self.secret[group].keys())

    def create_new_key(
        self,
        secret_save_path: str,
        key_save_path: str,
    ):
        """
        Encrypts an existing toml with a new key

        :param secret_save_path: Path to store new config
        :param key_save_path: Path to store new key
        :return:
        """
        new_key = Fernet.generate_key()
        secret_encryption_state = self.is_secret_encrypted
        if secret_encryption_state:
            self.decrypt_secrets()
        new_config = self.encrypt_secrets(key=new_key.decode(), inplace=False)
        if secret_encryption_state:  # revert secret state to previous
            self.encrypt_secrets()

        new_config = self.format_toml(new_config)
        with open(secret_save_path, "w", encoding="utf8") as file:
            file.write(new_config)
        with open(key_save_path, "w", encoding="utf8") as file:
            file.write(new_key.decode())

    def encrypt_secrets(self, key: str = None, inplace=True) -> Union[Dict, None]:
        """
        Encrypts all the secrets
        :param key:
            Key to use for encryption
            Defaults to key set in registry
        :param inplace:
            If true, modifies in memory and returns none
            If false, returns modified data
        :return:
        """

        new_encrypted_config = self.secret.copy()
        for group, keys in self.secret.items():
            for secret_key, value in keys.items():
                value = self._encrypt_value(
                    value.get("is_encrypted", False), value["value"], key
                )
                new_encrypted_config[group][secret_key]["value"] = value
        if not inplace:
            return new_encrypted_config
        self._secrets = new_encrypted_config
        self._is_secret_encrypted = True
        return None

    def decrypt_secrets(
        self,
        bypass_key: str = None,
    ):
        """
        Decrypts an env file
        :param bypass_key: If provided, ignores the key in azure registry
        :return:
        """
        if not self.is_secret_encrypted:
            raise ValueError("Keys have already been decrypted.")
        enc_key = bypass_key if bypass_key else self.default_key

        decoded_config = self.secret.copy()
        for group, keys in self.secret.items():
            for key, value in keys.items():
                decoded_config[group][key]["value"] = self._decrypt_value(
                    value.get("is_encrypted", False), value["value"], enc_key
                )
        self._secrets = decoded_config
        self._is_secret_encrypted = False
        self._secret_changed = True

    def add_new_secret(  # pylint:disable=too-many-arguments
        self,
        group_name: str,
        key_name: str,
        unencrypted_values: Any,
        is_encrypted: bool,
        create_group_if_not_exist: bool = False,
        allow_updating: bool = False,
    ):
        """
        Adds a new secret

        :param group_name: Group Name that secret belongs to
        :param key_name: Name for secret
        :param unencrypted_values: Value to store
        :param is_encrypted: If true, encrypts the value
        :param create_group_if_not_exist: If false, if group name does not exist raises exception
        :param allow_updating: If false, attempting to update existing key will raise an issue
        :return:
        """
        if "." in group_name:
            raise ValueError("Group name cannot have dot `.`")
        if "." in key_name:
            raise ValueError("Key name cannot have dot `.`")

        if group_name not in self.secret:
            if not create_group_if_not_exist:
                raise ValueError(
                    f"Group `{group_name}` doesnt exists."
                    f"Creation of group is not allowed."
                )
            self.secret[group_name] = {}

        if not allow_updating:
            if key_name in self.secret:
                raise ValueError(
                    f"{key_name} already exists in config." f" Updating is not allowed."
                )

        if is_encrypted:
            value = self._encrypt_value(True, unencrypted_values)
        else:
            value = unencrypted_values

        self._secrets[group_name][key_name] = {
            "value": value,
            "is_encrypted": is_encrypted,
        }

        self._is_secret_encrypted = True
        self._secret_changed = True
