"""Cache for oauth credentials."""

import json
import os

import google.oauth2.credentials

_DEFAULT_DIR = os.path.join(os.path.expanduser('~'), '.config', 'launchflow')
_DEFAULT_FILE = 'launchflow_google_creds.json'
_CREDS_PATH = os.path.join(_DEFAULT_DIR, _DEFAULT_FILE)


class DefCredsCache:

    def save(self, creds):
        os.makedirs(_DEFAULT_DIR, exist_ok=True)
        credentials_json = {
            "access_token": creds.token,
            "refresh_token": creds.refresh_token,
            "id_token": creds.id_token,
            "scopes": creds.scopes,
        }
        with open(_CREDS_PATH, 'w') as f:
            json.dump(credentials_json, f)

    def load(self):
        with open(_CREDS_PATH, 'r') as f:
            credentials_json = json.load(f)
            creds = google.oauth2.credentials.Credentials(
                token=credentials_json['access_token'],
                refresh_token=credentials_json['refresh_token'],
                id_token=credentials_json['id_token'],
                scopes=credentials_json['scopes'])
        if creds.expired:
            raise ValueError(
                'Credentials have expired. Please re-run: `launchflow auth`')
        return creds


CREDS_CACHE = DefCredsCache()


def get_user_creds():
    creds = CREDS_CACHE.load()
    if creds is None:
        raise ValueError(
            'failed to load credentials. Please run: `launch auth` to '
            'reauthanticate.')
    return creds


def save_user_creds(creds):
    CREDS_CACHE.save(creds)
