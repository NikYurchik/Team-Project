from collections import UserList, UserDict
from datetime import datetime, date
from my_utils import format_phone_number, sanitize_phone_number, get_date, format_email, sanitize_email

"""

"""

# буде батьківським для всіх полів
class Field:
    def __init__(self, value):
        self.__value = value

class Name(Field):
    def __init__(self, name):
        self.value = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __repr__(self):
        return self.value

# необов'язкове поле з телефоном та таких один запис (Record) може містити кілька
class Phone(Field):
    def __init__(self, phone):
        self.value = phone

    @property
    def value(self):
        return format_phone_number(self.__value)

    @value.setter
    def value(self, phone):
        self.__value = sanitize_phone_number(phone)

    def __repr__(self):
        return self.value

class Birthday(Field):
    def __init__(self, birthday):
        self.value = birthday

    @property
    def value(self):
        return '' if self.__value == None else self.__value.strftime('%Y-%m-%d')

    @value.setter
    def value(self, birthday):
        self.__value = None if birthday == None else get_date(birthday)

    def __repr__(self):
        return self.__value.strftime('%A %d %B %Y')
    
class Address(Field):
    def __init__(self, address):
        self.value = address
        
    @property
    def value(self):
        return '' if self.__value == None else self.__value

    @value.setter
    def value(self, value):
        self.__value = None if value == None else self.__value
        
    def __repr__(self):
        return self.value
    
class Email(Field):
    def __init__(self, email):
        self.value = email
        
    @property
    def value(self):
        return format_email(self.__value)
    
    @value.setter
    def value(self, email):
        self.__value = sanitize_email(email)
        
    def __repr__(self):
        return self.value
    
class Fullname(Field):
    def __init__(self, full_name):
        self.value = full_name
        
    @property
    def value(self):
        return '' if self.__value == None else self.__value

    @value.setter
    def value(self, value):
        self.__value = None if value == None else self.__value

    def __repr__(self):
        return self.value

##########################################################################################

# відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name
class Record:
    """Single Contact Record"""

    def __init__(self, name, phone=None, email=None, address=None, full_name=None):
        self.name = name if type(name) == Name else Name(name)
        self.phones = UserList()
        if phone:
            self.phone_add(phone)
        self.emails = UserList()
        if email:
            self.email_add(email)
        self.birthday = Birthday(None)
        self.address = Address(None)
        self.full_name = Fullname(None)

    def phone_exists(self, phone, is_raise = None):
        """Search for a phone by number
        
        is_raise = None - errors are not generated
                 = 1 - error if record exists
                 = -1 - error if record does not exist
        """
        pname = phone.value if type(phone) == Phone else format_phone_number(sanitize_phone_number(phone))
        for i in range(len(self.phones)):
            ps = self.phones[i]
            if ps.value == pname:
                if is_raise == 1:
                    raise Exception(f'Phone "{phone}" alredy exists!')
                return ps
        if is_raise == -1:
            raise Exception(f'Phone "{phone}" not found!')
        return None
    
    def email_exists(self, email, is_raise = None):
        ename = email.value if type(email) == Email else format_email(sanitize_email(email))
        for i in range(len(self.emails)):
            ems = self.emails[i]
            if ems.value == ename:
                if is_raise == 1:
                    raise Exception(f'Email "{email}" alredy exists!')
                return ems
        if is_raise == -1:
            raise Exception(f'Email "{email}" not found!')
        return None

    def phone_add(self, phone):
        """Adding one phone to the self.phones list
        
        The 'phone' parameter can be of type Phone or a string.
        """
        if type(phone) == Phone:
            self.phone_exists(phone, is_raise = 1)
            self.phones.append(phone)
        elif len(phone) > 0:
            self.phone_exists(phone, is_raise = 1)
            self.phones.append(Phone(phone))
    
    def email_add(self, email):
        if type(email) == Email:
            self.email_exists(email, is_raise = 1)
            self.emails.append(email)
        elif len(email) > 0:
            self.email_exists(email, is_raise = 1)
            self.emails.append(Email(email))

    def phone_update(self, phone, phone_new):
        """Changing the phone number in self.phones with a new number
        
        The 'phone' and 'phone_new' parameters can be of type Phone or a string.
        If the returned object is no longer needed, it can be deleted.
        """
        ps = self.phone_exists(phone, is_raise = -1)
        self.phone_exists(phone_new, is_raise = 1)
        if type(phone_new) != Phone:
            ps.value = phone_new
        else:
            self.phones.remove(ps)
            self.phones.append(phone_new)
            # if type(phone) != Phone:
            #     del ps
            return ps
        
    def email_update(self, email, email_new):
        ems = self.email_exists(email, is_raise = -1)
        self.email_exists(email_new, is_raise = 1)
        if type(email_new) != Email:
            ems.value = email_new
        else:
            self.emails.remove(ems)
            self.emails.append(email_new)
            return ems

    def phone_delete(self, phone):
        """Removing one phone from the self.phones list
        
        The 'phone' parameter can be of type Phone or a string.
        If the returned object is no longer needed, it can be deleted.
        """
        ps = self.phone_exists(phone, is_raise = -1)
        self.phones.remove(ps)
        # if type(phone) != Phone:
        #     del ps
        return ps
    
    def email_delete(self, email):
        ems = self.email_exists(email, is_raise = -1)
        self.emails.remove(ems)
        return ems

    def view_record(self, is_birthday=True):
        """Get a list of phones in one line from self.phones"""
        res = self.name.value
        if is_birthday and self.birthday.value:
            res = res + ' [birthday ' + self.birthday.value + ']:'
        else:
            res = res + ':'
        st = ' '
        for ph in self.phones.data:
            res = res + st + ph.value
            st = ', '
        return res

    def birthday_save(self, birthday):
        """Saving the birthday in self.birthday"""
        self.birthday.value = birthday
        
    def address_save(self, address):
        self.address.value = address
        
    def full_name_save(self, full_name):
        self.full_name.value = full_name

    def days_to_birthday(self):     # повертає кількість днів до наступного дня народження
        if self.birthday.value:
            cdt = datetime.now().date()
            dt = self.birthday.value
            dt = date(cdt.year, dt.month, dt.day)
            if dt < cdt:
                dt = date(cdt.year + 1, dt.month, dt.day)
            rdt = (dt - cdt)
            return rdt.days
        return None

    def __repr__(self):
        return self.view_record()

##########################################################################################

class AddressBook(UserDict):
    """Contact book"""

    def record_exists(self, rec_name, is_raise = None):
        """Search for a contact by name
        
        is_raise = None - errors are not generated
                 = 1 - error if record exists
                 = -1 - error if record does not exist
        """
        if type(rec_name) == Record:
            vname = rec_name.name.value
        elif type(rec_name) == Name:
            vname = rec_name.value
        else:
            vname = rec_name
        if len(self.data) > 0:
            for key, rec in self.data.items():
                if key == vname:
                    if is_raise == 1:
                        raise Exception(f'Record "{vname}" alredy exists!')
                    return rec
            if is_raise == -1:
                raise Exception(f'Record "{vname}" not found!')
        return None

    def add_record(self, record):
        """Adding a contact by record"""
        self.record_exists(record)
        self.update({record.name.value: record})

    def rec_add(self, name, phone=None, birthday=None, email=None, address=None, full_name=None):
        """Adding a contact by name
        
        If the returned object is no longer needed, it can be deleted.
        """
        vname = name.value if type(name) == Name else name
        self.record_exists(vname, is_raise = 1)
        rec = Record(name)
        self.update({vname: rec})
        
        if type(phone) == Phone:
            rec.phone_add(phone)
        else:
            if len(phone) > 0:
                if type(phone) == type(()):
                    for ph in phone:
                        rec.phone_add(ph)
                else:
                    rec.phone_add(phone)
                    
        if type(email) == Email:
            rec.email_add(email)
        else:
            if len(email) > 0:
                if type(email) == type(()):
                    for em in email:
                        rec.email_add(em)
                else:
                    rec.email_add(email)
                    
        if birthday:
            rec.birthday_save(birthday)
        if address:
            rec.address_save(address)
        if full_name:
            rec.full_name_save(full_name)

    def update_record(self, record):
        """Edit a contact by record"""
        vname = record.name.value
        rec = self.record_exists(vname, is_raise = -1)
        old = self.pop(vname)
        self.update({vname: rec})
        #del old
        return old

    def rec_update(self, rec_name, phone=None, birthday=None, email=None, address=None, full_name=None):
        """Edit a contact by name"""
        rec = self.record_exists(rec_name, is_raise = -1)
        
        if type(phone) == Phone:
            rec.phones.clear()
            rec.phone_add(phone)
        else:
            if len(phone) > 0:
                rec.phones.clear()
                if type(phone) == type(()):
                    for ph in phone:
                        rec.phone_add(ph)
                else:
                    rec.phone_add(phone)
                    
        if type(email) == Email:
            rec.emails.clear()
            rec.email_add(email)
        else:
            if len(email) > 0:
                rec.emails.clear()
                if type(email) == type(()):
                    for em in email:
                        rec.email_add(em)
                else:
                    rec.email_add(email)
        
        if birthday:
            rec.birthday_save(birthday)
        if address:
            rec.address_save(address)
        if full_name:
            rec.full_name_save(full_name)

    def delete_record(self, record):
        """Deleting a contact by record"""
        self.rec_delete(record.name.value)

    def rec_delete(self, rec_name):
        """Deleting a contact by name
        
        If the returned object is no longer needed, it can be deleted.
        """
        rec = self.record_exists(rec_name, is_raise = -1)
        self.pop(rec.name.value)
        # if type(rec_name) != Record:
        #     del rec
        return rec
    
    def list_records(self, name=''):
        """Getting a list of all contacts"""
        res = []
        vname = name.value if type(name) == Name else name
        if len(vname) > 0:
            res.append(self.record_exists(vname, is_raise = -1).view_record())
        else:
            for key, rec in self.data.items():
                res.append(rec.view_record())
        return res

    def phone_add(self, name, phone):
        """Adding a phone number to an existing contact in self.phones"""
        rec = self.record_exists(name, is_raise = -1)
        rec.phone_add(phone)
        
    def email_add(self, name, email):
        rec = self.record_exists(name, is_raise = -1)
        rec.email_add(email)

    def phone_correct(self, name, phone, phone_new):
        """Changing the phone number in self.phones with a new number"""
        rec = self.record_exists(name, is_raise = -1)
        rec.phone_update(phone, phone_new)
        
    def email_correct(self, name, email, email_new):
        rec = self.record_exists(name, is_raise = -1)
        rec.email_update(email, email_new)

    def phone_delete(self, name, phone):
        """Deleting a phone number from an existing contact in self.phones"""
        rec = self.record_exists(name, is_raise = -1)
        ps = rec.phone_delete(phone)
        return ps
    
    def email_delete(self, name, email):
        rec = self.record_exists(name, is_raise = -1)
        ems = rec.email_delete(email)
        return ems

    def birthday_save(self, name, birthday):
        """Saving the birthday in self.birthday"""
        rec = self.record_exists(name, is_raise = -1)
        rec.birthday_save(birthday)
        
    def address_save(self, name, address):
        rec = self.record_exists(name, is_raise = -1)
        rec.address_save(address)
        
    def full_name_save(self, name, full_name):
        rec = self.record_exists(name, is_raise = -1)
        rec.full_name_save(full_name)

    def search_records(self, mask):
        """Search for contacts by fragment of name or by fragment of phone number"""
        head = 'Contacts list (search):\n'
        sep =  '--------------------------------------------------'
        res = ''
        sm = mask.lower()
        for key, rec in self.data.items():
            fl = False
            sk = key.lower()
            if sk.find(sm) >= 0:
                fl = True
            else:
                for ph in rec.phones:
                    sk = sanitize_phone_number(ph.value)
                    if sk.find(sm) >= 0:
                        fl = True
                        break
            if fl:
                st = rec.view_record()
                if len(res) > 0:
                    res = res + '\n' + st
                else:
                    res = st
        if len(res) > 0:
            res = head + sep + '\n' + res + '\n' + sep
        return res

    def view_records(self, chunk_size = 20):
        """
        Display the entire address book in chunks of chunk_size entries.

        If chunk_size == None or 0, then all records are displayed in one chunk.
        """
        _index = 0
        _chunk_num = 0
        _chunk_size = chunk_size
        head = 'Contacts list:\n'
        sep =  '--------------------------------------------------'
        res = head + sep
        try:
            for key, rec in self.data.items():
                if len(res) > 0:
                    res = res + '\n' + rec.view_record()
                else:
                    res = rec.view_record()
                _index += 1
                if (_chunk_size > 0) and (_index // _chunk_size != _chunk_num):
                    yield res
                    _chunk_num += 1
                    res = ''
            if len(res) > 0:
                res = res +'\n' + sep
                yield res
            else:
                yield sep
        finally:
            return 

    def __repr__(self):
        for res in self.view_records(0):
            pass
        return res

    def __str__(self):
        for res in self.view_records(0):
            pass
        return res

    # def __del__(self):
    #     print('End of work', self)

##########################################################################################

if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    rec.phone_add('0501234567')
    rec.birthday_save('29.04.1999')
    ab = AddressBook()
    ab.add_record(rec)
    ab.rec_add('Dany',('380634567890','+380990123456'),'2001/11/21')
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, UserList)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '123-456-7890'
    assert ab['Bill'].phones[1].value == '+38(050)123-4567'
    assert isinstance(ab['Bill'].birthday, Birthday)
    assert ab['Bill'].birthday.value == '1999-04-29'
    assert isinstance(ab['Dany'].phones[0], Phone)
    assert ab['Dany'].phones[0].value == '+38(063)456-7890'
    assert ab['Dany'].phones[1].value == '+38(099)012-3456'
    assert isinstance(ab['Dany'].birthday, Birthday)
    assert ab['Dany'].birthday.value == '2001-11-21'
    # print(ab['Dany'])
    # print(ab)
    # print('All Ok')

# book = AddressBook()
# book.rec_add('Yurii', ('+38(067)576-1490', '+38(050)031-7201'))
# # print(book.list_records())

# book.rec_add('My', '+1(250)241-7847')
# # print(book.list_records())

# book.rec_add('Maryna', '+38(095)001-6123')
# # print(book.list_records())
# # print(book.list_records('My'))
# # print(book)

# # book.rec_delete('My')
# # print(book.list_records())

# # book.rec_update('Yurii', ('+38(067)576-1490', '+38(050)031-7201', '+1(250)241-7845'))
# # print(book.list_records())

# # book['Yurii'].phone_update('+1(250)241-7845', '+1(250)241-7847')
# # print(book.list_records())
# # print(book['Yurii'])
# for txt in book.view_records(2):
#     print(txt)
