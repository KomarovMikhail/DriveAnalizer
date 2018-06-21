from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class DriveAnalyzer:
    def __init__(self):
        self._scopes = 'https://www.googleapis.com/auth/drive.metadata.readonly'
        self._client_secret_file = 'client_secret.json'
        self._name = 'DriveAnalyzer'

    def _get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'drive-analyzer.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self._client_secret_file, self._scopes)
            flow.user_agent = self._name
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:
                # for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def get_files(self):
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)

        about = service.about().get(fields='user').execute()

        if about.get('user') is None:
            raise ValueError('Got invalid about requests result')

        user_email = about['user']['emailAddress']
        query = "'" + user_email + "' in owners"

        results = service.files().list(
            q=query,
            pageSize=1000,
            fields="nextPageToken, files(name, size, fileExtension)"
        ).execute()

        items = results.get('files', [])

        if not items:
            return None

        res = {}
        for item in items:
            if item.get('fileExtension') is not None and item.get('size') is not None:
                if res.get(item['fileExtension']) is None:
                    res[item['fileExtension']] = {
                        'objects': [{
                            'name': item['name'],
                            'size': int(item['size']) / 1024,
                        }],
                        'totalSize': int(item['size']) / 1024
                    }
                else:
                    res[item['fileExtension']]['objects'].append({
                        'name': item['name'],
                        'size': int(item['size']) / 1024
                    })
                    res[item['fileExtension']]['totalSize'] += int(item['size']) / 1024
        return res
