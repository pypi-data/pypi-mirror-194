'''Class for making request to Octopart using nexarClient'''
import os, sys
from nexarClient import NexarClient

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
              return_data[mpn]["data"] = result
              return return_data                
        
        print("Part not found")
        return return_data
    
    #TODO: "partsSearch" which takes a list of part numbers and uses partSearch() to search fo each and return the result as a dict