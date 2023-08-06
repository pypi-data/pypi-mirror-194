import logging,json,simplejson
#from posixpath import split
from . import restClient as client
from . import Sobjects,utils,thread
" select fields(all) from vlocity_cmt__EntityFilter__c where Id in ('a5W7Z0000009gEiUAI','a5W7Z0000009gdtUAA','a5W7Z0000009gFfUAI','a5W7Z0000009gEdUAI')"

def query_base64(q,raiseEx=True):
    call = client.callAPI(f'/services/data/v55.0/query?q={q}')
    checkError(q,raiseEx)
    if call['totalSize'] > len(call['records']):
        len_max_records = len(call['records'])
        q_order = f"{q} order by Id asc"
        call = _query(q_order,nextRecords=False)
        len_records_last_call = len(call['records'])
        call_next = call
        while (len_records_last_call==len_max_records):
            lastId = call_next['records'][len_max_records-1]['Id']
            q_and= f"{q} and Id>'{lastId}' order by Id asc"
            call_next = _query(q_and,nextRecords=False)
            call['records'].extend(call_next['records'])
            len_records_last_call = len(call_next['records'])

    return call

def query_threaded(q,values,search="$$$",raiseEx=True):
    result = []

    def do_work(value):
        q1 = q.replace(search,value)
        res = _query(q1)
        return res

    def on_done(res,result):
        result.append(res)

    thread.execute_threaded(values,result,do_work,on_done,threads=1)

def checkError(q,raiseEx=True):
    lc = client.thread_lastCall()

    lc['query']=q
    if lc['error'] != None:
        lc['query'] = q
        if raiseEx==True:
            errorOther = lc['errorOther'] if 'errorOther' in lc else ''
            utils.raiseException(lc['errorCode'],lc['error'],'query',f"{errorOther} . {q}")
        return True    
    return False

def _query(q,raiseEx=True,logResponse = False,nextRecords=True,popAttributes=True):
    logging.debug(q)
    call = client.callAPI(f'/services/data/v55.0/query?q={q}')
   # print(len(call['records']))

    call_next = call
    if nextRecords:
        while 'nextRecordsUrl' in call_next:
            call_next = client.callAPI(call_next['nextRecordsUrl'])
          #  print(len(call_next['records']))
            call['records'].extend(call_next['records'])

    if checkError(q,raiseEx) == True:
        logging.warn(simplejson.dumps(call, indent=4))
        return None
  #  lc = client.thread_lastCall()
  #  lc['query']=q
  #  if lc['error'] != None:
  #      lc['query'] = q
  #      if raiseEx==True:
  #          errorOther = lc['errorOther'] if 'errorOther' in lc else ''
  #          utils.raiseException(lc['errorCode'],lc['error'],'query',f"{errorOther} . {q}")
  #          raise ValueError(simplejson.dumps(call, indent=4))
  #      logging.warn(simplejson.dumps(call, indent=4))

  #      return None

    if logResponse == True:
        utils.printJSON(call)
    for r in call['records']: r.pop('attributes')

    return call

#--------------------------------------------------------------------------------------------------------------------------------------------------------
def query(q,raiseEx=True,X=['Id','Name'],logResponse=False):
    """
    Executes a query in Salesforce.
    - q: the query string. "select.... from... limit..."
        the where clause can specify a normal field or $X and $Z. 
    - X: by default it will query for Id and Name. 
    - logResponse: 
    """
    if '$X=' not in q and '$Z=' not in q:
        return _query(q,raiseEx,logResponse)

    if '$Z='  in q:
        X=['Id','ProductCode','Name']
        q = q.replace('$Z=','$X=')

    selectfields = q.strip().split()

    for x in range(len(selectfields)):
        if selectfields[x].lower() == 'from':
            objectType = selectfields[x+1]

        if  '$X' in selectfields[x]:
            where = selectfields[x].split("'")
            value = where[1]

    for field in X:
        if field == 'Id':
            if Sobjects.isId(objectType,value) == False:
                continue
        q1 = q.replace('$X',field)
        call = _query(q1,raiseEx=False)      
        if call['totalSize'] > 0:
            return call

    return None

def queryRecords(q,raiseEx=True,X=['Id','Name']):
    select = query(q,raiseEx,X)
    if select == None:
        return None
    return select['records']

cache = {}
def queryFieldList(q,field=None,raiseEx=False,X=['Id','Name']):
    if '$X=' in q or '$Z=' in q:
        print(q)
        if q in cache:
            return cache[q]
    records = queryRecords(q,raiseEx,X)

    if records == None:
        return None

    if field == None:
        field = q.strip().split()[1]
    
    fieldList = []
  
    for record in records:
        fieldList.append(record[field])
        
    if '$X=' in q or '$Z=' in q:
        cache[q]=fieldList

    return fieldList

#" select Id from vlocity_cmt__AttributeAssignment__c where vlocity_cmt__AttributeUniqueCode__c='ATT_MOBILE_CREDITS' and  vlocity_cmt__ObjectId__c='01t7Z00000AVpCLQA1' "
def queryField(q,field=None,raiseEx=False,X=['Id','Name']):
    fieldList = queryFieldList(q,field,raiseEx,X)

    if fieldList == None or len(fieldList) == 0:
        return None

    if len(fieldList) > 1:
        logging.warn(f"There is more than one record returned. total records {len(fieldList)}, query={q}")

    return fieldList[0]

def queryIdF(objName,extendedF,init=None):
    """Returns the Id for the especified extendedF.
    - if extendedF is a string, returns the string
    - if extendedF is a dictionary, return extendedF['Id]
    - if extendedF is a fieldName:fieldValue, returns the query on object where fieldName=fieldValue
    """
    if extendedF == None:
        return None
    if type(extendedF) is dict:
        extendedF = extendedF['Id']
    ef = utils.extendedField(extendedF)
    if ef['field'] == 'Id':
        if Sobjects.checkId(ef['value']):
            return ef['value']
        else:
            utils.raiseException("No_Id",f"{extendedF} is not a valid Id")
    return queryField(f" select Id from {objName} where {ef['field']} = '{ef['value']}' ")
def logQuery(q,filename,raiseEx=False):
    if filename != None:
        client.logCall(filename)
    call = query(q,raiseEx)

    return call


def process( call):
    for asset in call['records']:
        asset['vlocity_cmt__PricingLogData__c'] = json.loads( asset['vlocity_cmt__PricingLogData__c'])

def take_snapshot(fileName,q,postProcessing=None):
    client.debugFile(fileName)
    client.setDebugReplyProcessing(postProcessing)
    query(q)

def records(call):
    return call['records']

def  IN_clause(list):
    values = []
    for p in list:
        values.append(f"'{p}'")
    return ",".join(values)