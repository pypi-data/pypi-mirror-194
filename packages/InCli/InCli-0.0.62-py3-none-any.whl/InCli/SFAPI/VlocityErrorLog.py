from . import query,utils
import simplejson

def get_errors(where=None,limit=None):
    l = f" limit {limit} " if limit!= None else " limit 50 "
    q = f"""select Id,
                    OwnerId,
                    IsDeleted,
                    Name,
                    CreatedDate,
                    CreatedById,
                    LastModifiedDate,
                    SystemModstamp,
                    vlocity_cmt__Action__c,
                    vlocity_cmt__ErrorTime__c,
                    vlocity_cmt__InputData__c,
                    vlocity_cmt__ObjectName__c,
                    vlocity_cmt__SourceName__c,
                    vlocity_cmt__SourceType__c 
                    from vlocity_cmt__VlocityErrorLogEntry__c order by vlocity_cmt__ErrorTime__c desc  {l}"""

    return query.query(q)

def print_error_list(limit=None):
    res = get_errors(limit=limit)
    if len(res['records'])==0: return print(f"There are no records to pring.")

    for record in res['records']:
        record['ErrorMessage__c'] = _get_record_error_message(record)
        record['vlocity_cmt__ErrorTime__c'] = record['vlocity_cmt__ErrorTime__c'][0:19]

    print(f"Printing {len(res['records'])} records from vlocity_cmt__VlocityErrorLogEntry__c.")
    utils.printFormated(res['records'],"Id:vlocity_cmt__SourceType__c:vlocity_cmt__SourceName__c:vlocity_cmt__ErrorTime__c:vlocity_cmt__Action__c:ErrorMessage__c",rename="vlocity_cmt__SourceType__c%sourceType:vlocity_cmt__ErrorTime__c%ErrorTime")

def _get_record_error_message(record):
    input_data = simplejson.loads(record['vlocity_cmt__InputData__c'])

    error_message = 'Other'

    if record['vlocity_cmt__SourceType__c'] == 'Odin':
        error_message = input_data['ErrorMessage__c'][0:70]

    elif record['vlocity_cmt__SourceType__c'] == 'Integration Procedure':
        if  'ErrorMessage'  in input_data:
            if 'ErrorCode' in input_data:
                error_message  = f"{input_data['ErrorCode']} {input_data['ErrorMessage']} "
            else:
                error_message  = f"{input_data['ErrorMessage']} "

        elif 'GenericLogMessage' in input_data:
            error_message = input_data['GenericLogMessage'][0:70]
        else: 
            if 'StepResult' in input_data:
                if 'result' in input_data['StepResult']:
                    if 'HTTPStatusCode' in input_data['StepResult']['result']:
                        error_message  = f"HttpCode {input_data['StepResult']['result']['HTTPStatusCode']} "
                    if 'errors' in input_data['StepResult']['result']:
                        error_message  = str(input_data['StepResult']['result']['errors'])

                if 'info' in input_data['StepResult']:
                    if 'status' in input_data['StepResult']['info']:
                        error_message  = f"{input_data['StepResult']['info']['status']} {input_data['StepResult']['info']['statusCode']}"
                if 'error' in input_data['StepResult']:
                        error_message  = f"{input_data['StepResult']['error']}"
    return error_message

def print_error_records(last=None):
    limit = last if last!=None else 50
    res = get_errors(limit=limit)

    for record in res['records']:
        record['vlocity_cmt__ErrorTime__c'] = record['vlocity_cmt__ErrorTime__c'][0:19]
        record['ErrorMessage__c'] = _get_record_error_message(record)

        _print_error_record(record,print_renames=False)
        print()
        print()

   # utils.printFormated(res['records'],"Id:vlocity_cmt__ErrorTime__c:vlocity_cmt__SourceType__c:vlocity_cmt__SourceName__c:vlocity_cmt__Action__c:ErrorMessage__c",rename="vlocity_cmt__SourceType__c%sourceType:vlocity_cmt__ObjectName__c%ObjectName:vlocity_cmt__ErrorTime__c%time")

def query_and_print_error_record(id):
    q = f"select fields(all) from vlocity_cmt__VlocityErrorLogEntry__c where Id='{id}'"
    records = query.queryRecords(q)

    if len(records)>0:
        record = records[0]
        _print_error_record(record)
    else:
        print(f"Record Id {id} not found.")

def _print_error_record(record,print_renames=True):
    record['ErrorMessage__c'] = _get_record_error_message(record)
    record['vlocity_cmt__ErrorTime__c'] = record['vlocity_cmt__ErrorTime__c'][0:19]

    utils.printFormated(record,"Id:vlocity_cmt__ErrorTime__c:vlocity_cmt__SourceType__c:vlocity_cmt__SourceName__c:vlocity_cmt__Action__c:ErrorMessage__c",rename="vlocity_cmt__SourceType__c%sourceType:vlocity_cmt__ObjectName__c%ObjectName:vlocity_cmt__ErrorTime__c%time",print_renames=print_renames)

    input_data = simplejson.loads(record['vlocity_cmt__InputData__c'])
    json_formatted_str = simplejson.dumps(input_data, indent=2, ensure_ascii=False)

    print(json_formatted_str)