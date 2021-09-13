import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']
    USER_AGENT = ('SecureX Threat Response Integrations '
                  '<tr-integrations-support@cisco.com>')
    CTR_DEFAULT_ENTITIES_LIMIT = 100
    CLOUD_SIEM_API_ENDPOINT = 'https://{host}/api/sec/v1'
