from flask import Blueprint

from api.client import SumoLogicCloudSIEMClient
from api.utils import get_credentials, jsonify_data

health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    key = get_credentials()
    client = SumoLogicCloudSIEMClient(key)
    _ = client.health()
    return jsonify_data({'status': 'ok'})
