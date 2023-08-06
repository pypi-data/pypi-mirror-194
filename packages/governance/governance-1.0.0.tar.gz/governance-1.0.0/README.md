# Governance

`governance` is a Python package for submitting data to an API endpoint. It provides a `Results` class that can be used to set an API key, server URL, and agent ID, and to submit data as a JSON payload to the API endpoint.

## Installation

You can install `governance` using pip:

```pip install governance```


## Usage

Here's an example of how to use `governance` to submit some data:

```python
import governance

results = governance.Results()
results.set_api_key("my-api-key")
results.set_server_url("https://example.com")
results.set_agent_id("my-agent-id")
results.submit({"key1": "value1", "key2": "value2"})
```

## License
governance is released under the MIT license. See LICENSE for more details.