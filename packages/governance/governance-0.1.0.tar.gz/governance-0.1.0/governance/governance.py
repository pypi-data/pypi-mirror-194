# governance/governance.py
import json
import requests

import requests
import json

class Results:
    def __init__(self):
        self.api_key = None
        self.server_url = None
        self.agent_id = None
        self.agent_token = None
        self.project_id = None
        self.stage_id = None

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_server_url(self, server_url):
        self.server_url = server_url

    def set_agent_id(self, agent_id):
        self.agent_id = agent_id

    def set_agent_token(self, token):
        self.agent_token = token

    def set_project_id(self, project_id):
        self.project_id = project_id

    def set_stage_id(self, stage_id):
        self.stage_id = stage_id

    def submit(self, data, **kwargs):
        url = self.server_url + "result/"
        headers = {"Content-Type": "application/json", "agent_id": self.agent_id, "token": self.agent_token}
        payload = {}
        if self.api_key is not None:
            payload["api_key"] = self.api_key
        payload['project_id'] = self.project_id
        payload['stage_id'] = self.stage_id
        payload['json'] = data
        payload = json.dumps(payload)
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            print("Submission successful")
        else:
            print("Error submitting data: {}".format(response.content))

def governance():
    return Results()