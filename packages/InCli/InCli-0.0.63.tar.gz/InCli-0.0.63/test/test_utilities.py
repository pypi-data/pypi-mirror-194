import unittest,simplejson
from InCli.SFAPI import restClient,query,Sobjects

class Test_Utilities(unittest.TestCase):
    def test_limits(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0/limits'
        res = restClient.callAPI(action)

        print()


    def test_id(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0'
        res = restClient.callAPI(action)

        print()

    def test_id(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0'
        res = restClient.callAPI(action)
        for key in res.keys():
            print()
            action = res[key]
            res1 = restClient.callAPI(action)
            print(action)
            print(res1)

        print()
    
    def test_select(self):
        restClient.init('DEVNOSCAT4')

        q = f"select fields(all) from vlocity_cmt__VlocityTrackingEntry__c order by vlocity_cmt__Timestamp__c desc limit 100"
        res = query.query(q)
        for r in res['records']:
            ll = simplejson.loads(r['vlocity_cmt__Data__c'])
            json_formatted_str = simplejson.dumps(ll, indent=2, ensure_ascii=False)
            print(json_formatted_str)
            print()
    def test_delete_logs(self):
        restClient.init('demo240')

        q = "select Id from ApexLog where LogUserId='005Dm000000Yj0rIAC' "
        res = query.query(q)

        id_list = [record['Id'] for record in res['records']]
        
        Sobjects.deleteMultiple('ApexLog',id_list)
        print()

    def delete(self,q):
        res = query.query(q)

        id_list = [record['Id'] for record in res['records']]
        
        Sobjects.deleteMultiple('ApexLog',id_list)
        print()

    def test_delete_something(self):
        restClient.init('DEVNOSCAT4')

        q = "select Id from vlocity_cmt__ConfigurationSnapshot__c  "
        self.delete(q)