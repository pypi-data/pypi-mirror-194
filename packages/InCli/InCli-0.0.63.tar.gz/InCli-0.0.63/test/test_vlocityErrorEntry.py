import unittest,simplejson
from InCli import InCli
from InCli.SFAPI import VlocityErrorLog,restClient

class Test_VlocityErrorEntry(unittest.TestCase):

    def test_get_errors(self):
        restClient.init('NOSPRD')

        VlocityErrorLog.get_errors()

        print()

    def test_print_errors(self):
        restClient.init('NOSDEV')

        VlocityErrorLog.print_error_records()

        print()
    def test_get_error_ip(self):
        restClient.init('NOSDEV')

        Id = 'a6K3O000000FHuqUAG'

        q = f"select fields(all) from vlocity_cmt__VlocityErrorLogEntry__c where Id='{Id}' limit 10"

        res = query.query(q)


        out=[]
        for record in res['records']:
            data = record['vlocity_cmt__InputData__c']
            datas = simplejson.loads(data)

            theFile =jsonFile.write('TheIPError_1',datas)
            
            out.append(datas)
            print(datas['ErrorMessage__c'])


      #  file_csv.write('VlocityErrorLogEntry_1',out)

        print()

        
