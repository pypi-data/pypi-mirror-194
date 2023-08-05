# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymsx', 'pymsx.api']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.74,<2.0.0',
 'dacite>=1.8.0,<2.0.0',
 'dataconf>=2.1.3,<3.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pydantic>=1.10.5,<2.0.0',
 'requests-toolbelt>=0.10.1,<0.11.0',
 'requests>=2.28.2,<3.0.0',
 'urllib3==1.25.11']

setup_kwargs = {
    'name': 'pymsx',
    'version': '0.3.0',
    'description': 'Mosaics AI Python Client',
    'long_description': '# 🧰  pymsx - Mosaics AI MSX Client for Python\n\n[![PyPI](https://img.shields.io/pypi/v/pymsx?style=flat-square)](https://pypi.org/project/pymsx/)\n[![Interrogate](https://raw.githubusercontent.com/Mosaics-ai/pymsx/main/assets/interrogate_badge.svg)](https://github.com/Mosaics-AI/pymsx)\n\nThis repository contains the source code for Mosaics AI\'s official python client. This client is currently in pre-alpha version, so feedback is always welcome!\n\nYou are welcome to file an issue here for general use cases. You can also contact Mosaics Support [here](help.mosaics.ai).\n\n## Requirements\n\nPython 3.8 or above is required.\n\n## Documentation\n\nFor the latest documentation, see\n\n- [Mosaics AI](https://www.mosaics.ai)\n\n## Quickstart\n\nInstall the library with `pip install pymsx`\n\nNote: Don\'t hard-code authentication secrets into your Python. Use environment variables\n\nemail/Password Authentication:\n\n```bash\nexport MSX_USERNAME=*************\nexport MSX_PASSWORD=*************\n```\n\nIf you already have a token, use that instead:\n\n```bash\nexport MSX_TOKEN=*****************************************\n```\n\nExample usage:\n```python\nimport os\nimport pandas as pd\nfrom pymsx.client import MsxClient\n\n# If no credentials are supplied, then environment variables are required.\nemail = "help@mosaics.ai"\npassword = "$mosaics123"\n\n# ...or try using an active token.\n# This may fail, see exception handling below.\ntoken = None\n\n# First create client with active token or credentials\nmsx = MsxClient(\n    # ...using email/password\n    email=email,\n    password=password,\n    # ...or if using token, token will take priority\n    token=token\n)\n\n# Check the health of your server\nhealth = msx.health().dict()\n\nprint("Health: ", health)\n\nassert health is not None and health[\'status\'] == \'live\'\n\n# Add a dataset to your msx system\n\n# From a DataFrame\npath = "/path/to/dataset/data.csv"\ndf = pd.DataFrame(path)\nresult = msx.datasets.add(df=df)\n\n# Or pass in a string path to read from fs directly\nresult = msx.datasets.add(path=path)\n\nif result.ok:\n    print("DataFrame uploaded: ", result.details)\nelse\n    print("Upload failed: ", result.error)\n```\n\nException handling:\n```python\nfrom pymsx.client import MsxClient\nfrom pymsx.exceptions import ApiResponseError, InvalidTokenError\n\ntry:\n    try:\n        # An InvalidToken error is raised if the token is expired or incorrect\n        msx = MsxClient(\n            token=token\n        )\n    except InvalidTokenError:\n        print(f"Token invalid, logging in instead.")\n        # Catch all other errors using ApiResponseErrors\n        msx = MsxClient(\n            email=email,\n            password=password\n        )\nexcept ApiResponseError as e:\n    print(f"Could not create msx client: {e.error}")\n    return\n```\n\n## Contributing\n\nWe will allow contributing soon!\n\n## License\n\n[Apache License 2.0](LICENSE)\n',
    'author': 'mosaics.ai',
    'author_email': 'info@mosaics.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.mosaics.ai/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.10',
}


setup(**setup_kwargs)
