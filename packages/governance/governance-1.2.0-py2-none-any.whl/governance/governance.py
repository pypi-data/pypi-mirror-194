# governance/governance.py
import json
import requests
import pandas as pd
import joblib

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

    def register_artifact(self, type, data, uri, inherit_details_from_stage, name="", description="", permissions="", how_to_use="", task="", business_use_case="", warnings="", version=""):
        fields = ",".join(data.columns.values)
        df_hash = joblib.hash(data)
        payload = {
            "unique_hash": df_hash,
            "uri": uri,
            "fields": fields,
            "inherit_details_from_stage": inherit_details_from_stage,
            "stage_id": self.stage_id
        }

        # Check if we should inherit details from the stage
        if inherit_details_from_stage and self.project_id is not None:
            project_url = self.server_url + "/project/{}".format(self.project_id)
            headers = {"Content-Type": "application/json", "agent_id": self.agent_id, "token": self.agent_token}
            response = requests.get(project_url, headers=headers)
            if response.status_code != 200:
                print("Error retrieving project details: {}".format(response.content))
            else:
                project_data = response.json()
                stages = project_data.get("stages", [])
                for stage in stages:
                    datasets = stage.get("datasets", [])
                    if datasets:
                        dataset = datasets[0]
                        defaults = {
                            "name": dataset.get("name", ""),
                            "version": dataset.get("version", ""),
                            "description": dataset.get("description", ""),
                            "permissions": dataset.get("permissions", ""),
                            "how_to_use": dataset.get("how_to_use", ""),
                            "task": dataset.get("task", ""),
                            "business_use_case": dataset.get("business_use_case", ""),
                            "warnings": dataset.get("warnings", ""),
                            "inherits_id": dataset.get("dataset_id", "")
                        }
                        payload.update(defaults)
                        break

        # Override any inherited values with user-specified values
        overrides = {
            "name": name,
            "version":version,
            "description": description,
            "permissions": permissions,
            "how_to_use": how_to_use,
            "task": task,
            "business_use_case": business_use_case,
            "warnings": warnings
        }
        payload.update({k: v for k, v in overrides.items() if v})

        # Map the type value to the corresponding endpoint
        endpoint_map = {
            "dataset": "dataset/",
            "model": "model/",
            "featureset": "featureset/"
        }

        endpoint = endpoint_map.get(type)
        if endpoint is None:
            print("Invalid type specified")
            return

        url = self.server_url + endpoint
        headers = {"Content-Type": "application/json", "agent_id": self.agent_id, "token": self.agent_token}
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("Registration submitted successfully")
        else:
            print("Error submitting registration: {}".format(response.content))

def governance():
    return Results()