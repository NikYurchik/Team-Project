import os
import pathlib
import pickle
from virtual_assistant import AddressBook, Record
from Notebook import Notebook
from my_utils import split
from sorter import Sorter
import parser_check

interactive_mode = 0
request_details = 1  # запрашивать ли в командном режиме недостающие реквизиты контакта;
display_birthdays = 0  # выводить ли при запуске бота список контактов, у которых день рождения попадает в заданный период от текущего дня;
number_of_days = 7  # количество дней от текущего дня для вывода списка контактов, у которых день рождения приходится на этот период.
display_lines = 10  # количество отображаемых строк в одной порции вывода списка контактов или заметок

addressbook = None  # адресная книга
notebook = None  # книга заметок


def check_addressbook():
    global addressbook
    if addressbook is None:
        # addressbook = load_addressbook_from_file(filename)
        path_bin = pathlib.Path('AddressBook.bin')
        ab = None
        if path_bin.exists():
            try:
                with open(path_bin, "rb") as fh:
                    ab = pickle.load(fh)
            except Exception:
                pass
        if ab is None or not isinstance(ab, AddressBook):
            ab = AddressBook()
        addressbook = ab


def check_notebook():
    global notebook
    if notebook is None:
        # nb = load_notebook_from_file(filename)
        path_bin = pathlib.Path('NoteBook.bin')
        nb = None
        if path_bin.exists():
            try:
                with open(path_bin, "rb") as fh:
                    nb = pickle.load(fh)
            except Exception:
                pass
        if nb is None or not isinstance(nb, Notebook):
            nb = Notebook()
        notebook = nb

    # def save_to_file(self, filename, addressbook):
    #     with open(filename, "wb") as fh:
    #         pickle.dump(addressbook, fh)


# ----------------------------------------
def fun_add_name(contact, value):
    print(f'Добавляем контакт {contact}')
    check_addressbook()
    addressbook.rec_add(contact)


def fun_get_name(contact, value):
    print(f'Проверяем наличие контакта {contact}')
    check_addressbook()
    ab = addressbook.record_exists(contact)
    return ab is not None  # True - есть, False - нет


def fun_del_name(contact, value):
    print(f'Удаляем контакт {contact}')
    check_addressbook()
    addressbook.rec_delete(contact)


def fun_add_phone(contact, value):
    print(f'Добавляем телефон {value} контакту {contact}')
    check_addressbook()
    addressbook.phone_add(contact, value)


cur_phone = None


def fun_get_phone(contact, value):
    print(f'Проверяем наличие телефона {value} у контакта {contact}')
    global cur_phone
    check_addressbook()
    addressbook.record_exists(contact).phone_exists(value, -1)
    cur_phone = value


def fun_set_phone(contact, value):
    print(f'Заменяем телефон у контакта {contact} на {value}')
    check_addressbook()
    addressbook.phone_correct(contact, cur_phone, value)


def fun_del_phone(contact, value):
    print(f'Заменяем телефон у контакта {contact} на {value}')
    check_addressbook()
    addressbook.phone_delete(contact, value)


def fun_set_birthday(contact, value):
    print(f'Заменяем дату рождения у контакта {contact} на {value}')
    check_addressbook()
    addressbook.birthday_save(contact, value)


def fun_set_address(contact, value):
    print(f'Заменяем адрес у контакта {contact} на {value}')
    check_addressbook()
    # addressbook.address_save(contact, value)


def fun_add_email(contact, value):
    print(f'Добавляем eMail {value} контакту {contact}')
    check_addressbook()
    # addressbook.email_add(contact, value)


cur_email = None


def fun_get_email(contact, value):
    print(f'Проверяем наличие eMail {value} у контакта {contact}')
    global cur_email
    check_addressbook()
    # addressbook.record_exists(contact).email_exists(value, -1)
    cur_email = value


def fun_set_email(contact, value):
    print(f'Заменяем eMail у контакта {contact} на {value}')
    check_addressbook()
    #  addressbook.email_correct(contact, cur_phone, value)


def fun_del_email(contact, value):
    print(f'Заменяем eMail у контакта {contact} на {value}')
    check_addressbook()
    # addressbook.email_delete(contact, value)


def fun_set_fullname(contact, value):
    print(f'Заменяем ФИО у контакта {contact} на {value}')
    check_addressbook()
    # addressbook.fullname_save(contact, value)


def fun_add_note(tags, note):
    print(f'Добавляем заметку "{note}" с тегами {tags}')


def fun_set_note(tags, note):
    print(f'Сохраняем измененную заметку "{note}" с тегами {tags}')


def fun_del_note(tags, note):
    print(f'Удаляем заметку с тегами {tags}')


def fun_add_tag():
    pass


def fun_get_tag():
    pass


def fun_set_tag():
    pass


def fun_del_tag():
    pass


def fun_find_substring(substring, tmp):
    print(f'Вывод всех контактов, содержащих подстроку {substring}')
    check_addressbook()
    res = addressbook.search_records(substring)
    print(res)


def fun_find_note(substring, tmp):
    print(f'Вывод всех заметок, содержащих подстроку {substring}')


def fun_show_name(name='', tmp=''):
    check_addressbook()
    if len(name) == 0:
        print('Вывод всех записей адресной книги')
        for txt in addressbook.view_records(2):
            print(txt)
    else:
        print(f'Вывод записи контакта {name}')
        res = addressbook.list_records(name)
        print('\n'.join(res))


def fun_show_note(tag='', tmp=''):
    if len(tag) == 0:
        print('Вывод всех заметок')
    else:
        print(f'Вывод заметок с тегом {tag}')


# ----------------------------------------
def get_param(name, required):
    done = True
    while done:
        # print('Введите ' + name)
        st = input(f'Введите {name} > ')
        if required and len(st) == 0:
            print('Параметр обязателен!')
        else:
            done = False
    return st


def fun_hello(command, list_params):
    global interactive_mode
    interactive_mode = 1
    print('How can I help you?')


def fun_exit(command, list_params):
    global interactive_mode
    interactive_mode = 0
    print('Good bye!')


def func_sorter(command, list_params):
    sort = Sorter()
    destination = input("Введіть шлях, куди сортувати (за замовчуванням '' - сортування в ту ж папку): ")
    sort.run(list_params, destination)


def get_param_and_exec(command, list_params):
    # print(command, list_params)
    error_text = ''
    k = command.find('_')
    if k > 0:
        error_text = command[0:k]
    pars = params.get(command)  # словарь параметров команды
    if pars is None:
        print(f'Не найден список параметров команды "{error_text}". Обратитесь к разработчику.')
        return False
    else:
        k = 0
        for key, val in pars.items():
            done = True
            if val[0] == 0 and request_details == 0:
                break
            while done:
                if val[0] < 0:
                    name = ''
                    st = ''
                else:
                    if k >= len(list_params):  # параметр не задан в команде
                        st = get_param(val[1], val[0])  # запрашиваем параметр
                        if st == '/q':
                            return True
                    else:
                        st = list_params[k]
                    if k == 0:
                        name = st
                try:
                    val[2](name, st)
                    k += 1
                    done = False
                except Exception as e:
                    print(str(e))
        return True


# ----------------------------------------
"""
[0] - максимальное количество параметров комадды.
[1] - ключ команды по умолчанию
[2] - функция выполнения команды
"""
funcs = {
    "hello": [0, '', fun_hello],
    "exit": [0, '', fun_exit],
    #
    "add": [6, 'contact', get_param_and_exec],
    "change": [6, 'contact', get_param_and_exec],
    "delete": [6, 'contact', get_param_and_exec],
    #
    "search": [1, '', get_param_and_exec],
    "show": [0, 'all', get_param_and_exec],
    "sort": [2, '', get_param_and_exec]
}

keys = {
    "add": ['contact', 'phone', 'birthday', 'address', 'email', 'fullname', 'note'],
    "change": ['contact', 'phone', 'birthday', 'address', 'email', 'fullname', 'note'],
    # "change": ['phone', 'birthday', 'address', 'email', 'fullname', 'note'],
    "delete": ['contact', 'phone', 'email', 'note'],
    "search": ['note'],
    "show": ['all', 'contact', 'note'],
    "sort": []
}

"""
[0] - обязательный ли параметр
[1] - наименование параметра при запросе значения
"""
params = {
    "add_contact": {'name': [1, 'Contact Name', fun_add_name],
                    'phone': [0, 'Contact Phone', fun_add_phone],
                    'birthday': [0, 'Contact BirthDay', fun_set_birthday],
                    'email': [0, 'Contact eMail', fun_add_email],
                    'address': [0, 'Contact Address', fun_set_address],
                    'fullname': [0, 'Contact FullName', fun_set_fullname]
                    },
    # "add_name": {'name': [1, 'Contact Name', fun_add_name],
    #                 'phone': [0, 'Contact Phone', fun_add_phone],
    #                 'birthday': [0, 'Contact BirthDay', fun_add_birthday], 
    #                 'email': [0, 'Contact eMail', fun_add_email], 
    #                 'address': [0, 'Contact Address', fun_add_address], 
    #                 'fullname': [0, 'Contact FullName', fun_add_fullname]
    #             },
    "add_phone": {'name': [1, 'Contact Name', fun_add_name],
                  'phone': [0, 'Contact Phone', fun_add_phone]
                  },
    "add_birthday": {'name': [1, 'Contact Name', fun_add_name],
                     'birthday': [0, 'Contact BirthDay', fun_set_birthday]
                     },
    "add_email": {'name': [1, 'Contact Name', fun_add_name],
                  'email': [0, 'Contact eMail', fun_add_email]
                  },
    "add_address": {'name': [1, 'Contact Name', fun_add_name],
                    'address': [0, 'Contact Address', fun_set_address]
                    },
    "add_fullname": {'name': [1, 'Contact Name', fun_add_name],
                     'fullname': [0, 'Contact FullName', fun_set_fullname]
                     },
    "add_note": {'tag': [0, 'Note Tag', fun_add_tag],
                 'note': [1, 'Text Note', fun_add_note]
                 },
    #
    # "change_contact": {'name': [1, 'Contact Name', fun_get_name],
    #                    'phone': [0, 'Contact Phone', fun_add_phone],
    #                    'birthday': [0, 'Contact BirthDay', fun_add_birthday], 
    #                    'email': [0, 'Contact eMail', fun_add_email], 
    #                    'address': [0, 'Contact Address', fun_add_address], 
    #                    'fullname': [0, 'Contact FullName', fun_add_fullname]
    #                   },
    "change_phone": {'name': [1, 'Contact Name', fun_get_name],
                     'phone': [0, 'Contact Phone', fun_get_phone],
                     'newphone': [0, 'New Contact Phone', fun_set_phone],
                     },
    "change_birthday": {'name': [1, 'Contact Name', fun_get_name],
                        'birthday': [0, 'Contact BirthDay', fun_set_birthday]
                        },
    "change_email": {'name': [1, 'Contact Name', fun_get_name],
                     'email': [0, 'Contact eMail', fun_get_email],
                     'newemail': [0, 'New Contact eMail', fun_set_email]
                     },
    "change_address": {'name': [1, 'Contact Name', fun_get_name],
                       'address': [0, 'Contact Address', fun_set_address]
                       },
    "change_fullname": {'name': [1, 'Contact Name', fun_get_name],
                        'fullname': [0, 'Contact FullName', fun_set_fullname]
                        },
    "change_note": {'tag': [0, 'Note Tag', fun_get_tag],
                    'note': [1, 'Text Note', fun_set_note]
                    },
    #
    "delete_contact": {'name': [1, 'Contact Name', fun_del_name]},
    "delete_phone": {'name': [1, 'Contact Name', fun_get_name],
                     'phone': [1, 'Contact Phone', fun_del_phone]
                     },
    "delete_email": {'name': [1, 'Contact Name', fun_get_name],
                     'email': [1, 'Contact eMail', fun_del_email]
                     },
    "delete_note": {'tag': [1, 'Note Tag', fun_del_note]},
    "delete_tag": {'tag': [1, 'Note Tag', fun_del_tag]},
    #
    "search": {'substring': [1, 'Substring', fun_find_substring]},
    "search_note": {'tag': [1, 'Note Tag', fun_find_note]},
    "show": {'all': [-1, '', fun_show_name]},
    "show_all": {'all': [-1, '', fun_show_name]},
    "show_name": {'name': [1, 'Contact Name', fun_show_name]},
    "show_note": {'tag': [1, 'Note Tag', fun_show_note]},
    "sort": {'source': [1, 'Шлях до папки сортування: ', func_sorter]}
}


def parcer(command):
    # print(command)
    # if len(command) == 0:
    #     main_bot.main()         # запуск интерактивного режима
    # else:
    #     main_bot.main_com(command)  # обработка введенной команды
    res = ''
    if len(command) > 0:
        res = 'Неизвестная команда'
        # print(type(command))
        if type(command) == list:
            cm = command
        else:
            cm = split(command)
        cm0 = cm[0].lower()
        lcm = len(cm) - 1
        # lfn = self.funcs.get(cm0)
        lfn = funcs.get(cm0)
        if lfn is None:
            res = res + ' "' + cm[0] + '"!'  # Unexpected command - добавить подсказку подходящих команд
            res += '\n' + str(parser_check.closest_command(cm0, funcs.keys()))

        else:
            if len(cm) > 1:  # есть параметры
                cm1 = cm[1]
                if cm1.startswith('--'):  # Есть ключ команды
                    cm1 = cm1[2::]
                    cm.pop(1)  # убираем ключ команды
                else:
                    cm1 = '--'
            else:
                cm1 = '--'

            if cm1 == '--':  # смотрим ключ по умолчанию
                cm1 = lfn[1]
                if len(cm1) > 0:  # есть ключ по умолчанию
                    cm1 = '_' + cm1
            else:
                cmk = keys.get(cm1)
                if cmk is None:
                    res = f'Недопустимый ключ --{cm1} у команды {cm0}'
                    return res
                cm.pop(1)  # убираем ключ команды
                cm1 = '_' + cm1
            cm1 = cm0 + cm1  # добавляем ключ к команде

            ecm = lfn[0]
            if lcm < ecm:
                # res = f'Введено параметров {lcm}, максимум {ecm}. Дополнительно запрашиваем остальные параметры.'
                print(f'Введено параметров {lcm}, максимум {ecm}. Дополнительно запрашиваем остальные параметры.')
            elif lcm > ecm:
                # res = f'Введено параметров {lcm}, максимум {ecm}. Лишние игнорируем.'
                print(f'Введено параметров {lcm}, максимум {ecm}. Лишние игнорируем.')
            cm.pop(0)  # убираем команду из списка

            # print(cm0)
            # print(cm)

            try:
                res = lfn[2](cm1, cm)
            except Exception as e:
                res = str(e)
    else:
        print('Переход в интеактивный режим ввода команд.')
        fun_hello('hello', [])
    return res


def clear_screen():
    os.system('clear')


def main():
    # sys_argv = sys.argv
    # sys_argv = ['bot.py']
    # sys_argv = ['bot.py','show']
    # sys_argv = ['bot.py','add', 'Юрий']
    # sys_argv = ['bot.py','add', 'Юрий']
    # print(sys_argv, len(sys_argv))
    command = []
    # if len(sys_argv) > 1:
    #     for i in range(len(sys_argv)-1):
    #         command.append(sys_argv[i+1])
    while True:
        print(parcer(command))
        if interactive_mode == 0:
            break
        cmd = input('Очікую команду: ')
        command = split(cmd)
        clear_screen()


if __name__ == "__main__":
    main()
