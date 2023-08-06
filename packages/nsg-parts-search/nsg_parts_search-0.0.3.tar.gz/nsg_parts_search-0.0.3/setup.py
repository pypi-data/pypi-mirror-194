# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nsgsearch']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'nsg-parts-search',
    'version': '0.0.3',
    'description': 'NSG class for making parts searches in Octopart using the Nexar API v4',
    'long_description': '# NSG Parts Search\n<a href="https://nsg-engineering.com"><img src="https://lh6.googleusercontent.com/CWE0kETCdfJQd4YKOcCZTNCqPTNZxoDBXWLJsrp6-GkJXl-It7OUQ0wxhIHX4N5dHzM=w2400" align="left" width="100" hspace="10" vspace="6"></a>\n\nA class used for querying parts in Octopart using [Nexar API v4.0](https://nexar.com/api).\n\nThe following class has all the needed methods required by NSG to create a query to [Octopart](https://octopart.com/).\n\nThis package is maintained and used by [NSG](https://nsg-engineering.com/), please refer to the licensing before using.\n\n---\n\n## Table of content\n* [Installation](#Installation)\n* [Prerequisites](#Prerequisites)\n* [Usage](#Usage)\n* [Response](#Response)\n* [License](#License)\n\n---\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install **nsg-parts-search**.\n\n```bash\npip install nsg-parts-search\n```\n\n## Prerequisites\n\nUse the application client ID and secret. Refer to the [NSG Documentation](https://github.com/NSG-Engineering/OctopartClient).\n\nSet environment variables *CLIENT_ID* and *CLIENT_SECRET*.\n\n## Usage\n\nGeneral example to get a response from a list of parts search:\n```python\nfrom nsgsearch import *\n\n# set credentials\nclientId = os.environ[\'CLIENT_ID\']\nclientSecret = os.environ[\'CLIENT_SECRET\']\n\n# start the client\nsearch = NSG_OctopartSearch()\nsearch.setCredentials(clientId, clientSecret)\nsearch.startClient()\n\n# search for parts\nparts_list = []\nresults = search.partsSearch(parts_list)\n\nprint(results)\n\n```\n### Filtering Functions\nSay that from a list of parts you want a table of the Manufacturer, Suppliers, Quantity and Price per unit in USD:\n```python\n# loop through all parts\nfor part in parts_list:\n    # enter just if the part number was found\n    if results[part][\'found\']:\n        part_data = results[part][\'data\']\n        # get a table of prices for the part\n        priceTable = search.partPricesTable(part_data)\n```\n\nMaybe now you want to get the lowest price from the table for that part number:\n```python\ndef get_lowest_price(table):\n  price = table[0][\'price\']\n  supplier = str()\n  qty = int()\n  for row in table:\n      if row[\'price\'] < price:\n          price = row[\'price\']\n          supplier = row[\'supplier\']\n          qty = row[\'reqPurchase\']\n\n  return ([supplier, qty, price])\n```\n\nNow let\'s say you want to get the lead times for all suppliers and filter your prices to be no more than 30 days old:\n```python\n\n```\n\n## Response\nThe response from the search is a dictionary containing all the requested part numbers as keys.\n\nEach key contains another dictionary with the keys **found** and **data** and have the following format:\n```python\n{\n  "PN#": {\n    "found" : True / False,\n    "data" : {...}\n  },\n  {...}\n}\n```\n\n\nThe default query response has the following format:\n```Nginx\npart {\n      mpn\n      manufacturer {\n        name\n      }\n      shortDescription\n      specs {\n        attribute {\n          name\n          group\n        }\n        displayValue\n      }\n      octopartUrl\n      similarParts {\n        mpn\n        shortDescription\n        manufacturer {\n          name\n        }\n        octopartUrl\n        category {\n          name\n        }\n      }\n      companionProducts {\n        part {\n          mpn\n          shortDescription\n          manufacturer {\n            name\n          }\n          octopartUrl\n          category {\n            name\n          }\n        }\n      }\n      category {\n        name\n      }\n      bestDatasheet {\n        url\n      }\n      counts\n      medianPrice1000 {\n        price\n      }\n      sellers {\n        company {\n          name\n        }\n        country\n        offers {\n          sku\n          inventoryLevel\n          moq\n          prices {\n            quantity\n            price\n            currency\n          }\n          clickUrl\n          updated\n          factoryLeadDays\n        }\n        isRfq\n      }\n    }\n```\n\nYou can change the query response by using the method changeQuery():\n```python\n\nnewResponse = \n\'\'\'\nquery Search($mpn: String!) {\n    supSearchMpn(q: $mpn, limit: 1) {\n      results {\n        part {\n            mpn\n            shortDescription\n            manufacturer {\n              name\n            }\n        }\n      }\n    }\n}\n\'\'\'\n\nsearch.changeQuery(newResponse)\n\n```\n### API Part Reference\nhttps://octopart.com/api/v4/reference#part\n\n## License\n\n[GNU LGPL](https://github.com/NSG-Engineering/nsg-parts-search/blob/450fdf3b791683e2b901b6f52517b66c69193bf8/LICENSE)\n',
    'author': 'Antonio Arroyave',
    'author_email': 'antonio.arroyave@nsg-engineering.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
