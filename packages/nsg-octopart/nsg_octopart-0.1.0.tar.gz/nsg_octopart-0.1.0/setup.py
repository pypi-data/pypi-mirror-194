# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nsg_octopart']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'nsg-octopart',
    'version': '0.1.0',
    'description': 'NSG class for making request to Octopart using nexarClient',
    'long_description': '<p align="left">\n    <img src="https://eastus1-mediap.svc.ms/transform/thumbnail?provider=spo&inputFormat=jpg&cs=fFNQTw&docid=https%3A%2F%2Fnsg123-my.sharepoint.com%3A443%2F_api%2Fv2.0%2Fdrives%2Fb!GeVILip6n0GNxjPujL-PRbGX9o99ffxGssTvInH6KQtAebFS_i6LRJOK4tcYF7F9%2Fitems%2F01RORRWDKDTLCBKWXUWVEI3GQCNKSU6W3D%3Fversion%3DPublished&access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTBmZjEtY2UwMC0wMDAwMDAwMDAwMDAvbnNnMTIzLW15LnNoYXJlcG9pbnQuY29tQDI5ZTYzNWU1LTk2YzgtNDQ0MC04MzQ4LTQ1YmY3ZWE1NzgzYiIsImlzcyI6IjAwMDAwMDAzLTAwMDAtMGZmMS1jZTAwLTAwMDAwMDAwMDAwMCIsIm5iZiI6IjE2NzcwMjQwMDAiLCJleHAiOiIxNjc3MDQ1NjAwIiwiZW5kcG9pbnR1cmwiOiJkL2RxOGIvVjFGQWFqM1U4ODQ5RFN6bC93Y3J6UUFIbmxCalBMb00rVlk4PSIsImVuZHBvaW50dXJsTGVuZ3RoIjoiMTE2IiwiaXNsb29wYmFjayI6IlRydWUiLCJ2ZXIiOiJoYXNoZWRwcm9vZnRva2VuIiwic2l0ZWlkIjoiTW1VME9HVTFNVGt0TjJFeVlTMDBNVGxtTFRoa1l6WXRNek5sWlRoalltWTRaalExIiwic2lnbmluX3N0YXRlIjoiW1wia21zaVwiXSIsIm5hbWVpZCI6IjAjLmZ8bWVtYmVyc2hpcHxhbnRvbmlvLmFycm95YXZlQG5zZy1lbmdpbmVlcmluZy5jb20iLCJuaWkiOiJtaWNyb3NvZnQuc2hhcmVwb2ludCIsImlzdXNlciI6InRydWUiLCJjYWNoZWtleSI6IjBoLmZ8bWVtYmVyc2hpcHwxMDAzMjAwMjczOWU0MTQ5QGxpdmUuY29tIiwic2lkIjoiYzE2NjhjNmMtMDU5MC00MGQxLWE3ZjctMzk0N2NlYWIyZDA1IiwidHQiOiIwIiwidXNlUGVyc2lzdGVudENvb2tpZSI6IjMiLCJpcGFkZHIiOiI2Ni4xODMuMTguMTUyIn0.WkZIZyt5N1FNaU11QjJodmRhM0tkRlRwSlJTODNXM01mTnh5SmhiZ1JmWT0&cTag=%22c%3A%7B15C49A43-F45A-48B5-8D9A-026AA54F5B63%7D%2C1%22&encodeFailures=1&width=640&height=640&srcWidth=640&srcHeight=640" width="50" alt"NSG" >\n    <br>\n</p>\n\n# OctopartClient\n\n<p align="center">\n    <a href="#Usage">Usage</a> •\n    <a href="#Requirements">Requirements</a>\n</p>\n\n---\n\n## Usage\n\nOctopart API Reference:\n\nhttps://octopart.com/api/v4/reference#part\n\nNexar API login site:\n\nhttps://portal.nexar.com/\n\n- Credentials are in the "Credentials" section inside the Authorization tab for the application.\n\n- The App is called *HarnessQuotingApp*\n\n![image](https://user-images.githubusercontent.com/83880545/221388612-6f7eb6e3-304b-407e-b5a7-15be258fcca3.png)\n![image](https://user-images.githubusercontent.com/83880545/221388650-aeac6f79-b704-4553-8e31-4c7128136518.png)\n\n\n### Part Response Format:\n```Nginx\npart {\n          mpn\n          manufacturer {\n            name\n          }\n          shortDescription\n          specs {\n            attribute {\n              name\n              group\n            }\n            displayValue\n          }\n          octopartUrl\n          similarParts {\n            mpn\n            shortDescription\n            manufacturer {\n              name\n            }\n            octopartUrl\n            category {\n              name\n            }\n          }\n          companionProducts {\n            part {\n              mpn\n              shortDescription\n              manufacturer {\n                name\n              }\n              octopartUrl\n              category {\n                name\n              }\n            }\n          }\n          category {\n            name\n          }\n          bestDatasheet {\n            url\n          }\n          counts\n          medianPrice1000 {\n            price\n          }\n          sellers {\n            company {\n              name\n            }\n            country\n            offers {\n              sku\n              inventoryLevel\n              moq\n              prices {\n                quantity\n                price\n                currency\n              }\n              clickUrl\n              updated\n              factoryLeadDays\n            }\n            isRfq\n          }\n        }\n```\n\n---\n\n## Requirements\n\n',
    'author': 'Antonio Arroyave',
    'author_email': 'antonio.arroyave@nsg-engineering.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
