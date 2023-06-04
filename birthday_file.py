from datetime import datetime


def get_date(sdate):
    fmd = ('%Y%m%d', '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d',
           '%d%m%Y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y')
    dt = None
    for fm in fmd:
        try:
            dt = datetime.strptime(sdate, fm)
            break
        except ValueError:
            pass
    if dt == None:
        raise ValueError(f'The string "{sdate}" is not a date!')
    return dt.date()



class Field:
    def __init__(self, value):
        self.__value = value

class Birthday(Field):
    def __init__(self, birthday: str) -> None:
        self.value = birthday
        try:
            self.birthday = self.__value.replace(year=datetime.now().year)
        except ValueError:
            self.birthday = self.__value.replace(year=datetime.now().year, day=self.__value.day - 1)

    @property
    def value(self):
        return '' if self.__value == None else self.__value.strftime('%Y-%m-%d')

    @value.setter
    def value(self, birthday):
        self.__value = None if birthday == None else get_date(birthday)

    def __repr__(self):
        return self.__value.strftime('%A %d %B %Y')
    
    def days_to_birthday(self, lim=367):
        self.birthday = datetime.combine(
            self.birthday, datetime.min.time())

        if (self.birthday - datetime.now()).days >= 0:
            res = (self.birthday - datetime.now()).days + 1
        else:
            if datetime.now().year % 4:
                # 365 days for year
                res = (self.birthday - datetime.now()).days + 365 + 1
            else:
                # 366 days for a leap year
                res = (self.birthday - datetime.now()).days + 366 + 1
                
        if res <= lim:
            return res



if __name__ == '__main__':
    a = Birthday('2000-06-08')
    print(a)
    print(a.days_to_birthday(7))
    b = Birthday('2000-07-08')
    print(b.days_to_birthday(7))
    print(b.days_to_birthday())
