import boto3

dynamo_client  =  boto3.resource(service_name = 'dynamodb',
                                 region_name = 'ap-south-1',
                                 aws_access_key_id = 'AKIA2NZYKBDHSHIEYEUY',
                                 aws_secret_access_key = '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')

dynamo_client.get_available_subresources()

bank_table = dynamo_client.Table('Bank')

def check_item_exists(acc_id):
    response = bank_table.get_item(Key={'Account_ID': acc_id})
    if 'Item' in response:
        return True, response['Item']
    else:
        return False, {}

def insert(client_data):
    acc_id = int(client_data['new_acc_id'])
    present, items = check_item_exists(acc_id)
    if present:
        return {'Status': 'Failed', 'Message' : 'Account with %s is present.' % acc_id}
    else:
        data = {'Account_ID' : acc_id, 
                'Balance' : int(client_data['balance']),
                'Limit' : -1 * abs(int(client_data['limit'])),
                'Version' : 0}
        bank_table.put_item(Item = data)
        present, items = check_item_exists(acc_id)
        if present:
            return {'Status': 'Success', 'Message' : 'Account created with Number %s.' % acc_id, 'Items':items}  
        else:
            return {'Status': 'Failed', 'Message' : 'Account Not Created.'}

def read(client_data):
    acc_id = int(client_data['acc_id'])
    present, items = check_item_exists(acc_id)
    if present:
        return {'Status': 'Success', 'Items':items}  
    else:
        return {'Status': 'Failed', 'Message' : 'Account with id %s Not Found.'%acc_id}

def update(client_data):
    acc_id = int(client_data['acc_id'])
    present, items = check_item_exists(acc_id)
    if present:
        curr_balance = int(items['Balance'])
        limit = int(items['Limit'])
        op = client_data['w/d']
        money = int(client_data['money'])
        prev_version = int(items['Version'])
        if op == 'w':
            if curr_balance - money < limit:
                return {'Status' : 'Failed', 'Message' : 'Low Balnce.'}
            else:
                update_to_db(acc_id, prev_version + 1, curr_balance - money)
                present, updated_items = check_item_exists(acc_id)
                if present and int(updated_items['Version']) != prev_version and int(updated_items['Balance']) != curr_balance:
                    updated_items["Previous Balance"] = curr_balance
                    return {'Status':'Success', 'Updated Items':updated_items}
                else:
                    return {'Status' : 'Failed', 'Message' : 'Account was not updated. Try Again.'}
        elif op == 'd':
            update_to_db(acc_id, prev_version + 1, curr_balance + money)
            present, updated_items = check_item_exists(acc_id)
            if present and int(updated_items['Version']) != prev_version and int(updated_items['Balance']) != curr_balance:
                updated_items["Previous Balance"] = curr_balance
                return {'Status':'Success', 'Updated Items':updated_items}
            else:
                return {'Status' : 'Failed', 'Message' : 'Account was not updated. Try Again.'}
        else:
            return {'Status': 'Failed', 'Message': 'Wrong Entry'}  
    else:
        return {'Status': 'Failed', 'Message' : 'Account with id %s Not Found.'%acc_id}

def update_to_db(acc_id, new_version, new_balance):
    bank_table.update_item(
        Key={'Account_ID': acc_id}, UpdateExpression="SET Version = :val",
        ExpressionAttributeValues={':val' : str(new_version)}
    )

    bank_table.update_item(
        Key={'Account_ID': acc_id}, UpdateExpression="SET Balance = :bal",
        ExpressionAttributeValues={':bal' : str(new_balance)}
    )


    