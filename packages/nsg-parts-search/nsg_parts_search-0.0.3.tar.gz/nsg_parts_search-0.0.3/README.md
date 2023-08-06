# NSG Parts Search
<a href="https://nsg-engineering.com"><img src="https://lh6.googleusercontent.com/CWE0kETCdfJQd4YKOcCZTNCqPTNZxoDBXWLJsrp6-GkJXl-It7OUQ0wxhIHX4N5dHzM=w2400" align="left" width="100" hspace="10" vspace="6"></a>

A class used for querying parts in Octopart using [Nexar API v4.0](https://nexar.com/api).

The following class has all the needed methods required by NSG to create a query to [Octopart](https://octopart.com/).

This package is maintained and used by [NSG](https://nsg-engineering.com/), please refer to the licensing before using.

---

## Table of content
* [Installation](#Installation)
* [Prerequisites](#Prerequisites)
* [Usage](#Usage)
* [Response](#Response)
* [License](#License)

---

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **nsg-parts-search**.

```bash
pip install nsg-parts-search
```

## Prerequisites

Use the application client ID and secret. Refer to the [NSG Documentation](https://github.com/NSG-Engineering/OctopartClient).

Set environment variables *CLIENT_ID* and *CLIENT_SECRET*.

## Usage

General example to get a response from a list of parts search:
```python
from nsgsearch import *

# set credentials
clientId = os.environ['CLIENT_ID']
clientSecret = os.environ['CLIENT_SECRET']

# start the client
search = NSG_OctopartSearch()
search.setCredentials(clientId, clientSecret)
search.startClient()

# search for parts
parts_list = []
results = search.partsSearch(parts_list)

print(results)

```
### Filtering Functions
Say that from a list of parts you want a table of the Manufacturer, Suppliers, Quantity and Price per unit in USD:
```python
# loop through all parts
for part in parts_list:
    # enter just if the part number was found
    if results[part]['found']:
        part_data = results[part]['data']
        # get a table of prices for the part
        priceTable = search.partPricesTable(part_data)
```

Maybe now you want to get the lowest price from the table for that part number:
```python
def get_lowest_price(table):
  price = table[0]['price']
  supplier = str()
  qty = int()
  for row in table:
      if row['price'] < price:
          price = row['price']
          supplier = row['supplier']
          qty = row['reqPurchase']

  return ([supplier, qty, price])
```

Now let's say you want to get the lead times for all suppliers and filter your prices to be no more than 30 days old:
```python

```

## Response
The response from the search is a dictionary containing all the requested part numbers as keys.

Each key contains another dictionary with the keys **found** and **data** and have the following format:
```python
{
  "PN#": {
    "found" : True / False,
    "data" : {...}
  },
  {...}
}
```


The default query response has the following format:
```Nginx
part {
      mpn
      manufacturer {
        name
      }
      shortDescription
      specs {
        attribute {
          name
          group
        }
        displayValue
      }
      octopartUrl
      similarParts {
        mpn
        shortDescription
        manufacturer {
          name
        }
        octopartUrl
        category {
          name
        }
      }
      companionProducts {
        part {
          mpn
          shortDescription
          manufacturer {
            name
          }
          octopartUrl
          category {
            name
          }
        }
      }
      category {
        name
      }
      bestDatasheet {
        url
      }
      counts
      medianPrice1000 {
        price
      }
      sellers {
        company {
          name
        }
        country
        offers {
          sku
          inventoryLevel
          moq
          prices {
            quantity
            price
            currency
          }
          clickUrl
          updated
          factoryLeadDays
        }
        isRfq
      }
    }
```

You can change the query response by using the method changeQuery():
```python

newResponse = 
'''
query Search($mpn: String!) {
    supSearchMpn(q: $mpn, limit: 1) {
      results {
        part {
            mpn
            shortDescription
            manufacturer {
              name
            }
        }
      }
    }
}
'''

search.changeQuery(newResponse)

```
### API Part Reference
https://octopart.com/api/v4/reference#part

## License

[GNU LGPL](https://github.com/NSG-Engineering/nsg-parts-search/blob/450fdf3b791683e2b901b6f52517b66c69193bf8/LICENSE)
