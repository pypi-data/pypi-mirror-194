import os
import urllib.request
import requests
from typing import Optional, Dict, Collection
from urllib.parse import urljoin


__DEFAULT_VAULT_URL = "https://sm-vault.dev.spratingsvpc.com"
__DEFAULT_SHELF_ID = "rdsvelocity"
__DEFAULT_ENVIRONMENT = "dev"


class NoQuotedCommasSession(requests.Session):
    """
    Taken from https://stackoverflow.com/questions/23496750/how-to-prevent-python-requests-from-percent-encoding-my-urls/23497912

    The vault api allows multiple keys to be passed in a comma separated list (single parameter).
    However, the URL standard says that comma is a reserved token and so it becomes percent encoded, messing up the value that vault receives.
    This overrides that behavior to allow commas to be sent as-is.

    It could cause issues if there is a comma somewhere else in the request, but if we are only using this to hit vault I don't see where that issue would arise.
    """
    def send(self, *a, **kw):
        # a[0] is prepared request
        a[0].url = a[0].url.replace(urllib.request.quote(","), ",")
        return requests.Session.send(self, *a, **kw)


def get_secrets(key_names: Collection[str],
                vault_url: str = __DEFAULT_VAULT_URL,
                shelf_id: str = __DEFAULT_SHELF_ID,
                environment: str = __DEFAULT_ENVIRONMENT,
                fail_on_missing: bool = True) -> Dict[str, str]:
    """
    Gets the secrets from the vault for the given key names.
    If one or more keys do not exist in the vault and fail_on_missing is True (the default) a KeyError will be thrown.
    Otherwise, a dict is returned where the keys are the key names and the values are the secrets from vault.
    If fail_on_missing is False and any key was not found in vault, an empty dict is returned (it is all or nothing).

    :param key_names: an iterable with the keys of the secrets to retrieve
    :param vault_url: the base Vault URL
    :param shelf_id: the shelf id to use
    :param environment: the environment the shelf is in
    :param fail_on_missing: if False return None when the key is not found else raise a KeyError if this is True
    :return: a dict containing the keys mapped to their secret
    :raises KeyError: if any key is not found and fail_on_missing=True
    :raises requests.exceptions.HTTPError: if there is a Vault error (e.g. given shelf or env is invalid)
    """
    if len(key_names) < 1:
        return {}

    if os.environ.get('SPR_APP_SECRET_HC_VAULT_TOKEN') is None:
        raise KeyError("Unable to get SPR_APP_SECRET_HC_VAULT_TOKEN value from environment. Make sure the variable is exported")

    service_url = urljoin(vault_url, '/'.join([shelf_id, environment]))

    headers = {'spr-sm-token': os.environ.get('SPR_APP_SECRET_HC_VAULT_TOKEN')}
    s = NoQuotedCommasSession()
    resp = s.get(service_url,
                 params={'secret-keys': ','.join(key_names)},
                 headers=headers)

    if resp.status_code != 200:
        resp.raise_for_status()

    json = resp.json()
    if json['status']['code'] == '0':
        values = {key_name: json['data'][key_name] for key_name in key_names}
        return values
    else:
        if fail_on_missing:
            raise KeyError(f'Error: {json["status"]["message"]}')
        else:
            return {}


def get_secret(key_name: str,
               vault_url: str = __DEFAULT_VAULT_URL,
               shelf_id: str = __DEFAULT_SHELF_ID,
               environment: str = __DEFAULT_ENVIRONMENT,
               fail_on_missing: bool = True) -> Optional[str]:
    """
    Gets a secret from the vault of the given key name.  If fail_on_missing is True (the default)
    a KeyError will be thrown.  If it is set to False then the function will return None.

    :param key_name: the key of the secret to retrieve
    :param vault_url: the base Vault URL
    :param shelf_id: the shelf id to use
    :param environment: the environment the shelf is in
    :param fail_on_missing: if False return None when the key is not found else raise a KeyError if this is True
    :return: the secret value or None if not found and fail_on_missing=False
    :raises KeyError: if the key is not found and fail_on_missing=True
    :raises requests.exceptions.HTTPError: if there is a Vault error (e.g. given shelf or env is invalid)
    """

    values = get_secrets(
        key_names=[key_name],
        vault_url=vault_url,
        shelf_id=shelf_id,
        environment=environment,
        fail_on_missing=fail_on_missing
    )
    if values:
        return values[key_name]
    else:
        return None
