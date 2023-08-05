# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['awsiotclient']

package_data = \
{'': ['*']}

install_requires = \
['awsiotsdk>=1.5.11,<2.0.0']

setup_kwargs = {
    'name': 'awsiotclient',
    'version': '0.1.1',
    'description': 'The AWS IoT Device Client provides device-side functionality for AWS IoT services such as jobs, device shadow, and simple pubsub.',
    'long_description': '# aws-iot-device-client-python\n\nThe AWS IoT Device Client provides device-side functionality for AWS IoT services such as jobs, device shadow, and simple pubsub.\n\n## Installation\n\n### Minimum Requirements\n\n- Python 3.6+\n\n### Install from PyPI\n\n```shell\npython3 -m pip install awsiotclient\n```\n\n### Install from source\n\n```shell\ngit clone https://github.com/whill-labs/aws-iot-device-client-python\npython3 -m pip install ./aws-iot-device-client-python\n```\n\n## Usage\n\n### Create MQTT connection\n\n```python\nfrom awsiotclient import mqtt\n\n# Construct connection parameters\nconn_params = mqtt.ConnectionParams()\n\n# Required params\nconn_params.endpoint = <your_endpoint_url>\nconn_params.cert = <path_to_your_certificate>\nconn_params.key = <path_to_your_private_key>\nconn_params.root_ca = <path_to_your_root_ca>\n\n# Optional params\nconn_params.client_id = <client_id> # default "mqtt-" + uuid4()\nconn_params.signing_region = <signing_region> # default "ap-northeast-1" (Tokyo Region)\nconn_params.use_websocket = <True/False> # default False\n\n# Initialize connection\nmqtt_connection = mqtt.init(conn_params)\nconnect_future = mqtt_connection.connect()\nconnect_future.result()\n```\n\n### Use AWS IoT named shadow\n\nNote that usage of classic shadow client is similar to named shadow client.\n\n#### without delta (one-way communication from device to cloud)\n\n```python\nfrom awsiotclient import mqtt, named_shadow\n\n# <create mqtt connection here as described above>\nmy_client = named_shadow.client(\n    mqtt_connection,\n    thing_name="my_thing",\n    shadow_name="my_shadow"\n)\n\nmy_value = dict(foo="var")\nmy_clinet.change_reported_value(my_value)\n```\n\n#### with delta (two-way communication from/to device and cloud)\n\n```python\nfrom awsiotclient import mqtt, named_shadow\n\ndef my_delta_func(thing_name: str, shadow_name: str, value: Dict[str, Any]) -> None:\n    print("my_client invokes this callback when it receives delta message")\n    print(f"thing_name: {thing_name}, shadow_name: {shadow_name}, value: {value}")\n\n# <create mqtt connection here as described above>\nmy_client = named_shadow.client(\n    mqtt_connection,\n    thing_name="my_thing",\n    shadow_name="my_shadow",\n    delta_func=my_delta_func,\n)\n\nmy_value = dict(foo="var")\nmy_client.change_reported_value(my_value)\n# <wait until the client receives delta>\n```\n\n### Use AWS IoT jobs\n\n```python\nfrom awsiotclient import mqtt, named_shadow\n\ndef job_runner(id: str, document: dict):\n    print("my_client invokes this callback when it receives job document")\n    print(f"job id: {id}, document: {document}")\n\n# <create mqtt connection here as described above\njob_client = jobs.client(\n    mqtt_connection,\n    thing_name="my_thing",\n    job_func=job_runner\n)\n# <wait until the client receives job>\n```\n\n## License\n\nThis library is licensed under the Apache 2.0 License.\n\n## Acknowledgments\n\n- [AWS IoT Device SDK v2 for Python](https://github.com/aws/aws-iot-device-sdk-python-v2)\n',
    'author': 'Seiya Shimizu',
    'author_email': 'seiya.shimizu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whill-labs/aws-iot-device-client-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
