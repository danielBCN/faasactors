def my_handler(event, context):
    message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])
    print(message)
    return {
        'message': message
    }

