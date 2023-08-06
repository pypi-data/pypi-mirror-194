import unittest
from InCli import InCli
from InCli.SFAPI import account,restClient,digitalCommerce

class Test_DC(unittest.TestCase):
    def test_catalogs(self):
        restClient.init('DEVNOSCAT4')

        catalogs = digitalCommerce.getCatalogs()

        print()

    def test_getOffers(self):
        restClient.init('DEVNOSCAT4')

        catalogs = digitalCommerce.getCatalogs()
        for catalog in catalogs:
            try:
                offers = digitalCommerce.getOfferByCatalogue(catalog['vlocity_cmt__CatalogCode__c'])
                print(f"offers: {len(offers)}")
            except Exception as e:
                print(f"{catalog['vlocity_cmt__CatalogCode__c']}  {e.args[0]['error']}")

        print()

        
