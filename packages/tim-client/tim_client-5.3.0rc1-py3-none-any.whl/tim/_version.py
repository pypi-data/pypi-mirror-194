import json

__version__ = 'v5.3.0rc1'

version_json = '''
{
 "date": "2022-09-01T16:00:00+0200",
 "dirty": false,
 "error": null,
 "full-revisionid": "",
 "version": "v5.3.0rc1"
}
'''


def get_versions():
    return json.loads(version_json)
