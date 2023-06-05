from collections import UserDict
from check_classes import Name, Phone, Mail, Address, FullName
from record import Record
from my_utils import sanitize_phone_number

class AddressBook(UserDict):
    """Contact book"""

    def record_exists(self, rec_name, is_raise=None):
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

    def rec_add(self, name, phone=None, birthday=None):
        """Adding a contact by name

        If the returned object is no longer needed, it can be deleted.
        """
        vname = name.value if type(name) == Name else name
        self.record_exists(vname, is_raise=1)
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
        if birthday:
            rec.birthday_save(birthday)

    def update_record(self, record):
        """Edit a contact by record"""
        vname = record.name.value
        rec = self.record_exists(vname, is_raise=-1)
        old = self.pop(vname)
        self.update({vname: rec})
        # del old
        return old

    def rec_update(self, rec_name, phone=None, birthday=None):
        """Edit a contact by name"""
        rec = self.record_exists(rec_name, is_raise=-1)
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
        if birthday:
            rec.birthday_save(birthday)

    def delete_record(self, record):
        """Deleting a contact by record"""
        self.rec_delete(record.name.value)

    def rec_delete(self, rec_name):
        """Deleting a contact by name

        If the returned object is no longer needed, it can be deleted.
        """
        rec = self.record_exists(rec_name, is_raise=-1)
        self.pop(rec.name.value)
        # if type(rec_name) != Record:
        #     del rec
        return rec

    def list_records(self, name=''):
        """Getting a list of all contacts"""
        res = []
        vname = name.value if type(name) == Name else name
        if len(vname) > 0:
            res.append(self.record_exists(vname, is_raise=-1).view_record())
        else:
            for key, rec in self.data.items():
                res.append(rec.view_record())
        return res

    def phone_add(self, name, phone):
        """Adding a phone number to an existing contact in self.phones"""
        rec = self.record_exists(name, is_raise=-1)
        rec.phone_add(phone)

    def phone_correct(self, name, phone, phone_new):
        """Changing the phone number in self.phones with a new number"""
        rec = self.record_exists(name, is_raise=-1)
        rec.phone_update(phone, phone_new)

    def phone_delete(self, name, phone):
        """Deleting a phone number from an existing contact in self.phones"""
        rec = self.record_exists(name, is_raise=-1)
        ps = rec.phone_delete(phone)
        return ps

    def birthday_save(self, name, birthday):
        """Saving the birthday in self.birthday"""
        rec = self.record_exists(name, is_raise=-1)
        rec.birthday_save(birthday)

    def address_save(self, name, address):
        """Saving the address in self.address"""
        rec = self.record_exists(name, is_raise=-1)
        rec.address_add(address)

    def address_delete(self, name, address):
        """Deleting a address number from an existing contact in self.addresses"""
        rec = self.record_exists(name, is_raise=-1)
        ps = rec.address_delete(address)
        return ps

    def mail_save(self, name, mail):
        """Saving the mail in self.mail"""
        rec = self.record_exists(name, is_raise=-1)
        rec.mail_add(mail)

    def mail_delete(self, name, mail):
        """Deleting a mail number from an existing contact in self.mails"""
        rec = self.record_exists(name, is_raise=-1)
        ps = rec.mail_delete(mail)
        return ps

    def full_name_save(self, name, full_name):
        """Saving the full_name in self.full_name"""
        rec = self.record_exists(name, is_raise=-1)
        rec.full_name_save(full_name)

    def full_name_delete(self, name, full_name):
        """Deleting a full_name number from an existing contact in self.full_name"""
        rec = self.record_exists(name, is_raise=-1)
        ps = rec.full_name_delete(full_name)
        return ps

    def search_records(self, mask):
        """Search for contacts by fragment of name or by fragment of phone number"""
        head = 'Contacts list (search):\n'
        sep = '--------------------------------------------------'
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

    def view_records(self, chunk_size=20):
        """
        Display the entire address book in chunks of chunk_size entries.

        If chunk_size == None or 0, then all records are displayed in one chunk.
        """
        _index = 0
        _chunk_num = 0
        _chunk_size = chunk_size
        head = 'Contacts list:\n'
        sep = '--------------------------------------------------'
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
                res = res + '\n' + sep
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
