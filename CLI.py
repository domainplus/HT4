import re

contacts = {'Denis': '+38',
            'Alex': '+39',
            'Bob': '+40'}

def main():
    while True:
        request = input('ur action\n>>>:')
        if request in ('exit', 'close', 'good bye'):
            break

        for function_name in operations.keys():
            if request.lower() == function_name or request.lower().startswith(function_name + ' '):
                request = function_name + ' ' + request[len(function_name) + 1:] # This way we make sure that 'Phone Bob' transforms to 'phone Bob'
                if len(request.split(function_name)) > 1:  # if there are some parameters except for action name
                    parameters = request.lstrip(function_name).split()  # to receive parameters we get rid of action name
                else:
                    parameters = []

                action = operations.get(function_name, 'None')[0]

                print(action(*parameters))
                break

        else:
            print('Action not found. Pls try again')



def decor(func):
    def wrapper(*args, **kwargs):
        if not param_error(func, *args, **kwargs):  # I have heard a little! about SOLID and decided to put this check in outer func.
            try:
                result = func(*args, **kwargs)
                return result
            except KeyError as k:
                return f"KeyError: {k}. The key does not exist in the dictionary."
            except ValueError as v:
                print(f"ValueError: {v}. We need correct number.")
            except IndexError as i:
                print(f"IndexError: {i}. Index out of range.")
        else:
            return param_error(func, *args, **kwargs)

    return wrapper


def param_error(func, *args, **kwargs):

    err_message = ''

    operations_args = {
            'greeting': (0, 'No additional parameters needed. Try again.'),
            'add_contact': (2, 'We need Name and Tel No, separated by space. Try again.'),
            'change_contact': (2, 'We need Name and Tel No, separated by space. Try again.'),
            'show_contact': (1, 'We need Name. Try again.'),
            'show_all': (0, 'No additional parameters needed. Try again.'),
        }
    correct_no_args = operations_args.get(func.__name__)[0]

    if len(args) != correct_no_args:
        err_message = operations_args[func.__name__][1]

    if len(args) > 1:
        match = re.match(r'^\+?\d+$', args[1])  # Small validator for tel No. If we have it on the place of 2nd arg
        if not match:
            err_message = 'invalid tel No'
    #
    return err_message


@decor
def greeting():
    return 'How can I help you?'

@decor
def add_contact(*args):
    contacts.update({args[0]: args[1]})
    return contacts


@decor
def change_contact(*args):
    if args[0] not in contacts:
        return 'We dont have this contact to change'
    else:
        contacts.update({args[0]: args[1]})
    return contacts

@decor
def show_contact(*args):
    return contacts[args[0]]


@decor
def show_all():
    return contacts


operations = {
    'hello': [greeting, 0],
    'add': [add_contact, 2],
    'change': [change_contact, 2],
    'phone': [show_contact, 1],
    'show all': [show_all, 0]
}

if __name__ == '__main__':
    main()