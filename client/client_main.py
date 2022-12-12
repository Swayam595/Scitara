from prepare_client_socket import prepare_socket

def get_data_from_client():
    request_dict = dict()
    operation = input("Enter 'r' for read operation\nEnter 'i' for insert operation\nEnter 'u' for update operation: ")
    request_dict['op'] = operation
    if operation == 'r':
        request_dict['acc_id'] = input("Enter Account Number: ")
    elif operation == 'i':
        request_dict['new_acc_id'] = input("Enter your New Account Number: ")
        request_dict['balance'] = input("Enter your initial balance: ")
        request_dict['limit'] = input ("Enter minimum limit for the account: ")
    elif operation == 'u':
        request_dict['acc_id'] = input("Enter your Account Number: ")
        request_dict['w/d'] = input("Enter 'w' for withdrawing\nEnter 'd' for depositing money: ")
        request_dict['money'] = input("Enter Amount: ")
    return request_dict



def main():
    request_dict = get_data_from_client()
    prepare_socket(3699, request_dict)

if __name__ == "__main__":
    main()

