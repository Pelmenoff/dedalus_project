import json
from typing import Optional
from collections import UserDict
from datetime import date, datetime

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
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format. Please provide a 10-digit number.")
        self._value = value

    def __str__(self):
        return self.value


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
            raise ValueError("Invalid birthday format. Please provide a date object.")
        self._value = value

    def __str__(self):
        return self.value.strftime("%d-%m-%Y")


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = [] if phone is None else [Phone(phone)]
        self.birthday = birthday

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)
        return f"/// Contact {self.name}: {new_phone.value} added successfully"

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
        birthday_days_info = self.days_to_birthday()

        if birthday_days_info is not None:
            return f"/// {self.name}: {phones_str}, Birthday: {birthday_str}. {birthday_days_info} days"
        else:
            return f"/// {self.name}: {phones_str}, Birthday: {birthday_str}."


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.file_path = "address_book.json"  # File to store the data

        self.load_data()

    def add_record(self, name, phone, birthday=None):
        record = Record(name, phone, birthday)
        self.data[name] = record

    def get(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def get_all_contacts(self):
        return list(self.data.values())

    def __iter__(self):
        return AddressBookIterator(self.data.values())

    def save_data(self):
        with open(self.file_path, "w") as file:
            data_to_save = {
                "contacts": [
                    {
                        "name": contact.name.value,
                        "phones": [phone.value for phone in contact.phones],
                        "birthday": contact.birthday.value.strftime("%d-%m-%Y") if contact.birthday else None,
                    }
                    for contact in self.get_all_contacts()
                ]
            }
            json.dump(data_to_save, file, indent=2)

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                for contact_data in data.get("contacts", []):
                    name = contact_data.get("name")
                    phones = contact_data.get("phones", [])
                    birthday_str = contact_data.get("birthday")
                    birthday = Birthday(datetime.strptime(birthday_str, "%d-%m-%Y").date()) if birthday_str else None
                    self.add_record(name, phones[0], birthday)
                    for phone in phones[1:]:
                        self.get(name).add_phone(phone)
        except FileNotFoundError:
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
