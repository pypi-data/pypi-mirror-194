import requests
import json
import argparse
import os
import logging

# NOTE: returns a list of pod names.
# TODO: consider sending back the entire yaml? Maybe someone wants that? No status update here.
# TODO: make this error handling not shit.
def get_pod_ids(model_id, version_id):
    try:
        homeDir = os.path.expanduser( '~' )
        f = open(f"{homeDir}/pyqai.config")
        configObj = json.load(f)
        api_token = configObj["api_token"]
        account_id = configObj["account_id"]
    except Exception as e:
        logging.error(e, exc_info=True)
        print("ERROR. Unable to verify credentials; re-run pyqai-init to reset user credentials.")
        return 

    get_pods_json = {"model_id":model_id,"version_id":version_id,"account_id":account_id,"api_token":api_token}
    get_pods = requests.post('https://get-pods-fgkue36c2q-uc.a.run.app', json = get_pods_json, headers={'Authorization':api_token})

    try:
        get_pods_response = json.loads(get_pods.text)
        get_pods_content = get_pods_response['response']
        return get_pods_content
    except Exception as e:
        logging.error(e, exc_info=True)
        print(f"ERROR. Unable to get pod names with exception: {e}")
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-id", help="The id of your deployed model", required=True)
    parser.add_argument("--version-id", help="The version id of your deployed model", required=True)
    args = parser.parse_args()

    print(get_pod_ids(args.model_id, args.version_id))