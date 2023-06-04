import re


class Field:
    def __init__(self, value):
        self.__value = value


class Name(Field):  # work properly
    def __init__(self, name):
        self.value = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.match(r'^[a-zA-Z][\D\d]{3,}$', value):
            self.__value = value
        else:
            raise ValueError('The name must be longer than one letter and not contain numbers!')

    def __repr__(self):
        return self.value


class Phone(Field):  # work properly
    def __init__(self, phone):
        self.value = phone

    @property
    def value(self):
        return format_phone_number(self.__value)

    @value.setter
    def value(self, value):
        if re.match(r"(\b\d{10}\b)|(\+?\d{12}\b)", value):
            self.__value = sanitize_phone_number(value)
        else:
            raise ValueError('Incorrect phone number input, check it and try again, please!')

    def __repr__(self):
        return self.value


class Address(Field):
    def __init__(self, address):
        self.value = address

    @property
    def value(self):
        return '' if self.__value == None else self.__value

    @value.setter
    def value(self, address):
        self.__value = None if address == None else self.value

    def __repr__(self):
        return self.__value


class Mail(Field):
    def __init__(self, mail):
        self.value = mail

    @property
    def value(self):
        return '' if self.__value == None else self.__value

    @value.setter
    def value(self, mail):
        if not mail: self.__value = None
        elif re.findall(r'([a-zA-Z]{1,}[a-zA-Z0-9_\.]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,})', mail):
            self.__value = mail
        else:
            raise ValueError('Incorrect email input, check it and try again, please!')

    def __repr__(self):
        return self.__value


class FullName(Field):
    def __init__(self, full_name):
        self.value = full_name

    @property
    def value(self):
        return '' if self.__value == None else self.__value

    @value.setter
    def value(self, value):
        if re.match(r'(^[a-zA-Z\s\-]{2,}$)', value):
            self.__value = None if value == None else self.value
        else:
            raise ValueError('Incorrect full name input, check it and try again, please!')

    def __repr__(self):
        return self.__value

