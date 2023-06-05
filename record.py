from collections import UserList
from check_classes import Name, Phone, Birthday, Address, Mail, FullName
from datetime import datetime, date
from my_utils import format_phone_number, sanitize_phone_number


class Record:
    """Single Contact Record"""

    def __init__(self, name, phone=None):
        self.name = name if type(name) == Name else Name(name)
        self.phones = UserList()
        if phone:
            self.phone_add(phone)
        self.birthday = Birthday(None)
        self.full_name = FullName(None)
        # self.address = None
        # self.mail = None
        self.mails = []
        self.addresses = []

    def phone_exists(self, phone, is_raise=None):
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

    def phone_add(self, phone):
        """Adding one phone to the self.phones list

        The 'phone' parameter can be of type Phone or a string.
        """
        if type(phone) == Phone:
            self.phone_exists(phone, is_raise=1)
            self.phones.append(phone)
        elif len(phone) > 0:
            self.phone_exists(phone, is_raise=1)
            self.phones.append(Phone(phone))

    def phone_update(self, phone, phone_new):
        """Changing the phone number in self.phones with a new number

        The 'phone' and 'phone_new' parameters can be of type Phone or a string.
        If the returned object is no longer needed, it can be deleted.
        """
        ps = self.phone_exists(phone, is_raise=-1)
        self.phone_exists(phone_new, is_raise=1)
        if type(phone_new) != Phone:
            ps.value = phone_new
        else:
            self.phones.remove(ps)
            self.phones.append(phone_new)
            # if type(phone) != Phone:
            #     del ps
            return ps

    def phone_delete(self, phone):
        """Removing one phone from the self.phones list

        The 'phone' parameter can be of type Phone or a string.
        If the returned object is no longer needed, it can be deleted.
        """
        ps = self.phone_exists(phone, is_raise=-1)
        self.phones.remove(ps)
        # if type(phone) != Phone:
        #     del ps
        return ps

    def view_record(self, is_birthday=True):
        """Get a list of phones in one line from self.phones"""
        res = self.name.value
        if is_birthday and self.birthday.value:
            res = res + ' [birthday ' + self.birthday.value + '] '
        else:
            res = res + ''
        if self.full_name.value:
            res = res + ' [full name: ' + self.full_name.value + '] '
        else:
            res = res + ''
        if any(self.mails):
            res = res + ' [mails: ' + ', '.join(map(str, self.mails)) + ']:'
        else:
            res = res + ''
        if any(self.addresses):
            res = res + ' [addresses: ' + ', '.join(map(str, self.addresses)) + '] '
        else:
            res = res + ''
        st = ' '
        for ph in self.phones.data:
            res = res + st + ph.value
            st = ', '
        return res

    def birthday_save(self, birthday):
        """Saving the birthday in self.birthday"""
        self.birthday.value = birthday

    def address_add(self, address):
        """Saving the address in self.addresses"""
        if isinstance(address, str):
            address = self.address_save(address)
        if str(address) in list(map(str, self.addresses)):
            raise Exception (f'This address has already been saved!')
        else: self.addresses.append(address)

    def address_save(self, address):
        """Saving the address in self.address"""
        address = Address(address)
        return address

    def address_delete(self, address):
        """Removing one phone from the self.addresses list"""
        for ad in self.mails:
            if str(ad) == address:
                self.mails.remove(ad)
                return ad
        return f'{address} not found.'

    def mail_add(self, mail):
        """Saving the mail in self.mails"""
        if isinstance(mail, str):
            mail = self.mail_save(mail)
        if str(mail) in list(map(str, self.mails)):
            raise Exception (f'This email has already been saved!')
        else: self.mails.append(mail)

    def mail_save(self, mail):
        """Saving the mail in self.mail"""
        mail = Mail(mail)
        return mail

    def mail_delete(self, mail):
        """Removing one mail from the self.mails list"""
        for ml in self.mails:
            if str(ml) == mail:
                self.mails.remove(ml)
                return ml
        return f'{mail} not found.'

    def full_name_save(self, full_name):
        """Saving the full_name in self.full_name"""
        self.full_name.value = full_name

    def full_name_delete(self, full_name):
        if self.full_name:
            self.full_name = None
            return full_name
        return f'{full_name} not found.'

    def days_to_birthday(self):  # повертає кількість днів до наступного дня народження
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