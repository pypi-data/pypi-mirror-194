# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopyo365',
 'aiopyo365.factories',
 'aiopyo365.providers',
 'aiopyo365.ressources',
 'aiopyo365.services']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'aiopyo365',
    'version': '0.1.1a0',
    'description': '',
    'long_description': '# aiopyo365\n\nAsync wrapper for Python >= 3.8 around [Microsoft v1.0 graph API](https://learn.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0&preserve-view=true).\n\n\n## Installation\n\n`pip install aiopyo365`\n\n\n## Requirements\n\npython 3.8 or greater\n\n### Application registration\nMicrosoft Graph APi requires to be authentificated. You will need to \nhave a [registred application](https://learn.microsoft.com/en-us/graph/auth-register-app-v2) in Azure that will provide you: \n* client id \n* client secret\n\nYou will also need to have the [required permissions](https://learn.microsoft.com/en-us/graph/permissions-reference) to be able to interact with  [the desired ressources](https://learn.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0&preserve-view=true). \n\n\n## Installation\n#TODO\n\n## Authentification\n\nTo authentificate you can use the `GraphAuthProvider` class in the `providers.auth module`.\n\nhere is how to use this class. it assumes that you have set the folowing environnement variables :\n\n* CLIENT_ID\n* CLIENT_SECRET\n* TENANT_ID\n\nThe class provide a method to fetch the token in the\nform of a `dict`.\n\n```python\nimport asyncio\nfrom aiopyo365.providers.auth import GraphAuthProvider\n\nasync def fetch_auth_header():\n    auth_provider =  GraphAuthProvider(\n            client_id=os.environ["CLIENT_ID"],\n            client_secret=os.environ["CLIENT_SECRET"],\n            tenant_id=os.environ["TENANT_ID"],\n        )\n    return await auth_provider.auth()\n\n\nif __name__ == \'__main__\':\n    auth_header = asyncio.run(fetch_auth_header())\n    print(auth_header)\n\n\n# output : {"authorization": "<token type> <token>"}\n```\n\n## Ressources\nThe library tries to resemble the organization of the graph API documentation.\n\nfor instance in the Graph documentation you will find the [`DriveItems`](https://learn.microsoft.com/en-us/graph/api/resources/driveitem?view=graph-rest-1.0) under the `Files` section.  \nIn  `aiopyo365`: \n```python\nfrom aiopyo365.ressources.files import DriveItems\n```\nIf you want to work directly with ressources class you will need to instanciate a `aiohttp session` with `auth header` and instanciate the client class.\n\n```python\nimport asyncio\nimport aiohttp\nfrom aiopyo365.ressources.files import DriveItems\n\nasync def upload_smallfile(content,file_name):\n    auth_provider =  GraphAuthProvider(\n            client_id=os.environ["CLIENT_ID"],\n            client_secret=os.environ["CLIENT_SECRET"],\n            tenant_id=os.environ["TENANT_ID"],\n        )\n    auth_header = await auth_provider.auth()\n    session = await aiohttp.ClientSession(headers=auth_header)\n    drive_items_client = DriveItems(base_url="url", session=session)\n    await drive_items_client.upload_small_file(content, file_name)\n    \n```\nYou can also use factories\nto work with variant of ressources\nhere we work with a driveItems dedicated to SharePoint (site).\n\n```python\nimport asyncio\nimport aiohttp\nimport os\nfrom aiopyo365.providers.auth import GraphAuthProvider\nfrom aiopyo365.factories.drive_items import DriveItemsSitesFactory\n\nasync def upload_smallfile(content,file_name):\n    auth_provider =  GraphAuthProvider(\n            client_id=os.environ["CLIENT_ID"],\n            client_secret=os.environ["CLIENT_SECRET"],\n            tenant_id=os.environ["TENANT_ID"],\n        )\n    auth_header = await auth_provider.auth()\n    session = await aiohttp.ClientSession(headers=auth_header)\n    drive_items_client = DriveItemsSitesFactory(site_id="site_id").create(session=session)\n    await drive_items_client.upload_small_file(content, file_name)\n    \n```\n\n## Services\n\n`aiopyo365` provide also service class that encapsulate many ressource to match business logic. It hides dealing with instanciate class client and so on.\nLet\'s reuse the upload of a file example from above and use the `SharePointService`\n\n```python\nimport os\nfrom aiopyo365.providers.auth import GraphAuthProvider\nfrom aiopyo365.services.sharepoint import SharePointService\n\nasync def upload_smallfile(content,file_name):\n    auth_provider =  GraphAuthProvider(\n            client_id=os.environ["CLIENT_ID"],\n            client_secret=os.environ["CLIENT_SECRET"],\n            tenant_id=os.environ["TENANT_ID"],\n        )\n    async with SharePointService(auth_provider,"SHAREPOINT_HOSTNAME","SHAREPOINT_SITE") as sharepoint:\n        resp = await sharepoint.upload(\n            small_file_path, "small_file", conflict_behavior="replace"\n        )\n        assert resp["createdDateTime"]\n    \n```',
    'author': 'gonza',
    'author_email': 'matgonzalez@hotmail.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
