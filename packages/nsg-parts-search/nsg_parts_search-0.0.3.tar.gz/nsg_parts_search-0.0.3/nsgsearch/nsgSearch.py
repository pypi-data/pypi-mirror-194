'''Class for making request to Octopart using nexarClient'''
from nsgsearch.nexarClient import NexarClient

DEFAULT_QUERY_MPN = '''
query Search($mpn: String!) {
    supSearchMpn(q: $mpn, limit: 1) {
      results {
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
      }
    }
  }
'''

class NSG_OctopartSearch:
    """
    NSG Octopart Search is a class that uses the nexar API for making searches in Octopart
    """
    def __init__(self, clientId = "", clientSecret = ""):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.query = DEFAULT_QUERY_MPN

    def setCredentials(self, clientId: str, clientSecret: str):
        self.clientId = clientId
        self.clientSecret = clientSecret

    def changeQuery(self, newStructure):
        """
        Changes the query used by the client.
        """
        self.query = newStructure

    def startClient(self):
        if not self.clientId or not self.clientSecret:
            raise ValueError('You have not defined the credentials, use method setCredentials()')
        self.client = NexarClient(self.clientId, self.clientSecret)

    def partFound(self, mpn: str, data: dict):
        if not mpn:
            raise ValueError('Wrong Part Number Value')
        
        results = data.get("supSearchMpn").get("results")
        result_mpn = results[0].get("part").get("mpn")

        if mpn != result_mpn:
            return False
        return True
        
    def partSearch(self, mpn: str):
        """
        Returns the result of an Octopart search for a Manufacturer Part Number.

        This function is useful when only searching for one part particular number.

        Parameters
        ----------
        mpn : string
            Manufacturer Part Number.

        Return
        ------
        Dictionary
            Dictionary containing the response from the query in the following format:
            {
              "PN1": {
                "found" : True / False,
                "data" : {...}
              }
            }
        """

        if not mpn:
            raise ValueError('Part Number can not be empty', 'mpn')
        elif type(mpn) is not str:
            raise ValueError('Part Number must be a string', 'mpn')
        
        try:
          self.client
        except NameError:
            raise NameError('Client needs to be defined first, use method startClient()')
        
        variable = {
            'mpn': mpn
        }

        return_data = {
                mpn : {
                  "found" : False,
                  "data" : None
                }
            }

        result = self.client.get_query(self.query, variable)

        if result:
            if self.partFound(mpn, result): 
              return_data[mpn]["found"] = True
              results = result.get("supSearchMpn").get("results")
              part_data = results[0].get("part")
              return_data[mpn]["data"] = part_data
              return return_data                
        
        print("Part not found")
        return return_data
    
    def partsSearch(self, parts_list = None):
      """
      Uses the partSearch function over a list of part numbers.

      Return
      ------
          Dictionary containing the response from the query in the following format:

            {
              "PN#": {
                "found" : True / False,
                "data" : {...}
              },
              {...}
            }

      """
      results = {}
      if type(parts_list) is list or type(parts_list) is tuple:
        for part in parts_list:
          search_results = self.partSearch(part)
          for key, value in search_results.items():
            results[key] = value
        return results
      else:
        raise TypeError("Parts List must be of type list or tuple")
    
    def partPricesTable(self, part: dict, currency = "USD", wInventory = True):
        """
        Returns a table(list) made from dictionaries.

        This function is useful when you want to get the prices offered for a part number.

        Parameters
        ----------
        part : dict
            dictionary data from a part.
        currency : string
            default value is USD.
        wInventory : string
            If you only want to include results with inventory.

        Return
        ------
        List
            List of dictionaries containing:
            [
              table_row = {
                      'manufacturer' : manufacturer,
                      'partNumber' : partNumber,
                      'supplier' : supplier,
                      'price' : offer_price.get('price'),
                      'reqPurchase' : offer_price.get('quantity'),
                      'leadTime' : offer.get('factoryLeadDays'),
                      'updated' : offer.get('updated')
              },
              {...}
            ]
        """
        # Table as a list of dictionaries
        table = list()

        manufacturer = part.get('manufacturer', {}).get('name', "")
        partNumber = part.get('mpn', "")

        for seller in part.get('sellers', []):
          supplier = seller.get('company', "").get('name', "")
          for offer in seller.get('offers', []):
              if wInventory and offer.get('inventoryLevel', 0) == 0:
                 continue
              
              for offer_price in offer.get('prices', []):
                if offer_price.get('currency') == currency:
                  table_row = {
                     'manufacturer' : manufacturer,
                     'partNumber' : partNumber,
                     'supplier' : supplier,
                     'price' : offer_price.get('price'),
                     'reqPurchase' : offer_price.get('quantity'),
                     'leadTime' : offer.get('factoryLeadDays'),
                     'updated' : offer.get('updated')
                  }
                  table.append(table_row)

        return table  

      