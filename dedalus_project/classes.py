import json, phonenumbers, re
from typing import Optional
from collections import UserDict
from datetime import date, datetime

class WrongPhoneNumber(Exception):
    pass

class WrongBirthdate(Exception):
    pass

class WrongEmail(Exception):
    pass

class Field:
    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = str(new_value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return str(self)


class Name:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = str(new_value).capitalize()

    def __str__(self):
        return str(self._value)

class Phone:
    def __init__(self, value=None):
        self._value = None
        if value:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise WrongPhoneNumber("Invalid phone number. Please provide a valid phone number.")
            self._value = value
        except phonenumbers.NumberParseException as e:
            raise WrongPhoneNumber("Invalid phone number format. Please provide a valid phone number in format +xxxxxxxxxxxx.") from e

    def __str__(self):
        return str(self._value)
    
    def __eq__(self, __value: object) -> bool:
        return self._value == __value._value


class Birthday:
    def __init__(self, value=None):
        self._value = None
        if value:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, date):
            try:
                value = datetime.strptime(value, "%d.%m.%Y").date()
            except ValueError:
                raise WrongBirthdate("Invalid birthday format. Please provide a valid date in format dd.mm.yyyy")
        self._value = value

    def __str__(self):
        return self._value.strftime("%d.%m.%Y")
    
class Email:
    def __init__(self, value=None):
        self._value = None
        if value:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        email_pattern = '[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]'
        if not re.match(email_pattern, value):
            raise ValueError("Invalid email format. Try again.")
        self._value = value

    def __str__(self):
        return str(self._value)   


class Record:
    def __init__(self, name, phones=None, birthday=None, email=None):
        self.name = Name(name)
        if phones is None:
            self.phones = []
        else:
            self.phones = [Phone(phones)] if isinstance(phones, str) else [Phone(phone) for phone in phones]
        self.birthday = birthday
        self.email = email

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)
        return f"/// Contact {self.name}: {new_phone.value} added successfully"

    def add_email(self, email):
        self.email = Email(email)
        return f"/// Contact {self.name}: Email added successfully"

    def change_phone(self, old_phone, new_phone):
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)

        if old_phone.value in [phone.value for phone in self.phones]:
            self.phones = [new_phone if phone.value == old_phone.value else phone for phone in self.phones]
            return f"/// Phone number changed from {old_phone.value} to {new_phone.value} for contact {self.name}"
        else:
            return f"/// Phone number {old_phone.value} not found for contact {self.name}"

    def days_to_birthday(self):
        if self.birthday:
            today = date.today()
            next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None

    def __str__(self):
        phones_str = ', '.join(str(phone) for phone in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "N/A"
        email_str = str(self.email) if self.email else "N/A"
        birthday_days_info = self.days_to_birthday()

        if birthday_days_info is not None:
            return f"/// {self.name}: {phones_str}, Birthday: {birthday_str}, Email: {email_str}. {birthday_days_info} days"
        else:
            return f"/// {self.name}: {phones_str}, Birthday: {birthday_str}, Email: {email_str}."


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.file_path = "address_book.json"
        self.load_data()

    def add_record(self, name, phone, birthday=None, email=None):
        record = Record(name, phone, birthday, email)
        self.data[name] = record

    def get(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def get_all_contacts(self):
        return list(self.data.values())

    def __iter__(self):
        return AddressBookIterator(self.data.values())

    def save_data(self):
        data = {
            "contacts": [
                {
                    "name": record.name.value,
                    "phones": [str(phone) for phone in record.phones],
                    "birthday": str(record.birthday) if record.birthday else None,
                    "email": str(record.email) if record.email else None
                }
                for record in self.get_all_contacts()
            ]
        }
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)

            for contact_data in data.get("contacts", []):
                name = contact_data.get("name")
                phones = contact_data.get("phones", [])
                birthday_str = contact_data.get("birthday")
                email_str = contact_data.get("email")

                birthday = None
                if birthday_str:
                    birthday = Birthday(datetime.strptime(birthday_str, "%d.%m.%Y").date())

                email = None
                if email_str:
                    email = Email(email_str)
                
                self.add_record(name, phones, birthday, email)

        except (FileNotFoundError, json.JSONDecodeError):
            pass


class AddressBookIterator:
    def __init__(self, records):
        self.records = records
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.records):
            record = self.records[self.index]
            self.index += 1
            return record
        raise StopIteration
