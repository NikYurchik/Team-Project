import pathlib
import pickle
from my_utils import split
from virtual_assistant import AddressBook, Record

"""
This is a bot-assistant.

Bot implemented as a console application.

After starting it displays 'I'm ready' and the invitation '>>'.

Executes commands:
'hello' - responds to 'How can I help you?' and goes into interactive mode.
'add <name> <phone>' - saves a new contact in the phonebook.
'change <name> <phone>' - saves the new phone number of an existing contact in the phonebook.
'search <mask>' - search for contacts by fragment of name or by fragment of phone number.
'delphone <mame> <phone>' - deleting a phone number from an existing contact.
'delete <name>' - deleting a contact by name from the phonebook.
'birthday <name> <birthday> - save birthday of an existing contact in the phonebook.
'show <name> - returns the phone number for the specified contact.
'show /all' - displays all saved contacts with phone numbers and birthday.
'exit' - outputs 'Good bye!' and completes its work interactively.
"""

class Bot_assistant:

    def __init__(self) -> None:
        self.interactive_mode = 0   # 0 - режим командной строки;
                                    # 1 - интерактивный режим выполнения команды, выход по завершению выполнения команды;
                                    # 2 - полный интерактивный режим по команде 'hello', выход по команде 'exit'.
        self.done = True
        self.path_bin = pathlib.Path('AddressBook.bin')
        ab = None
        if self.path_bin.exists():
            try:
                ab = self.read_from_file(self.path_bin)
            except Exception:
                pass
        if ab == None or not isinstance(ab, AddressBook):
            ab = AddressBook()
        self.addressbook = ab

    # def input_error(func):
    #     def inner(argv):
    #         try:
    #             res = func(self, argv)
    #         except Exception as e:
    #             res = str ( e )
    #         return res
    #     return inner

    def fun_hello(self, argv):
        self.interactive_mode = 2   # полный интерактивный режим, выход по команде 'exit'.
        return 'How can I help you?'

    #@input_error
    def fun__add(self, argv):
        ph = argv[1]
        nm = argv[0].capitalize()
        if not isinstance(self.addressbook.get(nm), Record):
            self.addressbook.rec_add(nm, ph)
        else:
            self.addressbook.record_exists(nm).phone_add(ph)
        return 'Ok'

    #@input_error
    def fun_change(self, argv):
        ph = argv[1]
        nm = argv[0].capitalize()
        self.addressbook.rec_update(nm, ph)
        return 'Ok'

    #@input_error
    def fun_birthday(self, argv):
        ph = argv[1]
        nm = argv[0].capitalize()
        self.addressbook.birthday_save(nm, ph)
        return 'Ok'

    #@input_error
    def fun_phone(self, argv):
        nm = argv[0].capitalize()
        ph = self.addressbook.list_records(nm)
        return ph[0]

    def fun_search(self, argv):
        nm = argv[0]
        st = self.addressbook.search_records(nm)
        return st

    def fun_show_all(self, argv):
        if argv[0] == '/all':
            st = str(self.addressbook)
        else:
            nm = argv[0].capitalize()
            ph = self.addressbook.list_records(nm)
            st = ph[0]
        return st

    def fun_exit(self, argv):
        self.save_to_file(self.path_bin, self.addressbook)
        self.done = False
        self.interactive_mode = 0
        return 'Good bye!'

    def fun_delphone(self, argv):
        ph = argv[1]
        nm = argv[0].capitalize()
        self.addressbook.phone_delete(nm, ph)
        return 'Ok'
    
    def fun_delete(self, argv):
        nm = argv[0].capitalize()
        self.addressbook.rec_delete(nm)
        return 'Ok'

    """
    Dictionary of valid commands.
    The key is the first word of the command.
    Value - list of command details:
        [0] - allowable parameters in the command;
        [1] - additional command word;
        [2] - a function that executes a command.
    """
    funcs = {
        "hello": [0, '', fun_hello],
        "add": [2, '', fun__add],
        "change": [2, '', fun_change],
        "birthday": [2, '', fun_birthday],
        "search": [1, '', fun_search],
        "delphone": [2, '', fun_delphone],
        "delete": [1, '', fun_delete],
        "show": [1, '', fun_show_all],
        "exit": [0, '', fun_exit]
    }

    params = {
        "add": ['Name', '*Phone', '*BirthDay', '*Email', '*Address', '*FullName'],
        "change": ['Name', '*Phone', '*BirthDay', '*Email', '*Address', '*FullName'],
        "birthday": ['Name', '*BirthDay'],
        "search": ['Substring'],
        "delphone": ['Name', 'Phone'],
        "delete": ['Name'],
        "show": [1, '/all|Name'],

    }
    def parcer(self, command):
        """
        Parser of the entered command.

        Input parameter - the entered command.
        If an empty string is entered or the command is not in the dictionary, then an error will be 'Unexpected command!'.\n
        If the command is in the dictionary, but the number of command parameters does not match the allowed one from 
        the command dictionary, then there will be an error 'Not enough parameters!' or 'Too many parameters!'.\n
        If all checks passed without errors, then the function corresponding to the command is called.\n
        Command parameters are passed as a list.\n
        The parser returns the strings returned by the functions to the main loop.
        """
        res = 'Unexpected command'
        if len(command) > 0:
            cm = split(command)
            cm0 = cm[0].lower()
            lcm = len(cm) - 1
            lfn = self.funcs.get(cm0)
            if lfn == None:
                res = res + ' "' + cm[0] + '"!'     # Unexpected command - добавить подсказку подходящих команд
            else:
                ecm = lfn[0]
                if lcm < ecm:
                    res = f'Not enough parameters! Expected {lcm}, received {ecm}.'
                elif lcm > ecm:
                    res = f'Too many parameters! Expected {lcm}, received {ecm}.'
                elif len(lfn[1]) > 0 and cm[1].lower() != lfn[1]:
                    res = res + ' "' + cm[0] + ' ' + cm[1] + '"!'
                else:
                    if len(lfn[1]) > 0:
                        cm.pop(1)
                    cm.pop(0)
                    try:
                        res = lfn[2](self, cm)
                    except Exception as e:
                        res = str ( e )
        else:
            res = res + '!'
        return res

    def save_to_file(self, filename, addressbook):
        with open(filename, "wb") as fh:
            pickle.dump(addressbook, fh)

    def read_from_file(self, filename):
        with open(filename, "rb") as fh:
            unpacked = pickle.load(fh)
        return unpacked


def main():
    ba = Bot_assistant()
    print("I'm ready")
    while ba.done:
        st = input('>> ')
        an = ba.parcer(st)
        if len(an) > 0:
            print(an)

if __name__ == "__main__":
    main()
