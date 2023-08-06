# Governance

`governance` is a Python package for connecting a python notebook environment to the Mission Control MLOps platform. Mission Control enables teams to accelerate quality, velocity, and trust in their data science lifecycle by tightly embedding governance and compliance requirements directly into notebooks, and submitting testing and evaluation results to Mission Control for trust analysis.

More information about Mission Control can be found at www.takecontrol.ai. Interested teams can request Sandbox access to the Enterprise Server Edition.

## Installation

You can install `governance` using pip:

```pip install governance```


## Usage

### Submitting testing and evaluation results to Mission Control

```python
# test.py
import governance

governance.set_api_key("<YOUR MISSION CONTROL API KEY>")
governance.set_server_url("<THE BASE URL FOR YOUR MISSION CONTROL DEPLOYMENT>")
governance.set_agent_id("<YOUR MISSION CONTROL AGENT ID>")
governance.set_project_id("<YOUR MISSION CONTROL PROJECT ID>")
governance.set_stage_id("<YOUR MISSION CONTROL STAGE ID>")
governance.set_agent_token("<YOUR MISSION CONTROL TOKEN>")

# Submit the results of a calculation to be stored as a result associated with this stage of the data science lifecycle
governance.submit({"key1": "value1", "key2": "value2"})
```

## License
governance is released under the MIT license. See LICENSE for more details.