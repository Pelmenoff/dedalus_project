from classes import AddressBook, Name, Phone, Birthday, Record
from datetime import datetime


address_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "/// Contact not found."
        except ValueError:
            return "/// Invalid input. Provide a 10-digit number in the format [1234567890] or Date of birth in the format [XX.XX.XXXX]"
        except IndexError:
            return "/// Invalid command. Type \"help\" to show all commands."
    return wrapper


help_info = """/// Commands:
/// "add [name] [phone] [birthday]" - Add a contact to the address book. Birthday is optional.
/// "changephone [name] [old_phone] [new_phone]" or "cp [name] [old_phone] [new_phone]" - Change the phone number for a contact.
/// "changebirthdate [name] [new_date]" or "cb [name] [new_date]" - Change the birthdate for a contact.
/// "showcontacts all" or "sc all" - Show all contacts.
/// "showcontacts [page_number]" or "sc [page_number]" - Show contacts page by page. Enter 'all' to show all contacts at once.
/// "help" - Show this help message.
/// "exit", "bye", "good bye", "close", "quit", "q" - Turn off the assistant."""


@input_error
def hello_handler(*args):
    return "/// How can I help you?"


@input_error
def help_handler(*args):
    return f"{help_info}"


@input_error
def add_handler(*args):
    if len(args) < 2:
        return "/// Invalid command. Please provide name and phone."

    name = str(Name(args[0]))
    phone = str(args[1])
    birthday = None
    if len(args) > 2:
        birthday = Birthday(datetime.strptime(args[2], "%d.%m.%Y").date())

    rec: Record = address_book.get(name)
    if rec:
        return rec.add_phone(phone)

    address_book.add_record(name, phone, birthday)
    return f"/// Contact {name}: {phone} added successfully"


@input_error
def cp_handler(*args):
    if len(args) < 3:
        return "/// Invalid command. Please provide name, old phone, and new phone."

    name = args[0]
    old_phone = args[1]
    new_phone = args[2]

    rec: Record = address_book.get(name)
    if rec:
        if any(str(phone) == old_phone for phone in rec.phones):
            rec.change_phone(old_phone, new_phone)
            return f"/// Phone number changed from {old_phone} to {new_phone} for contact {name}"
        else:
            return f"/// Phone number {old_phone} not found for contact {name}"
    else:
        return f"/// No contacts with name: \"{name}\" in the address book"


@input_error
def cd_handler(*args):
    if len(args) < 2:
        return "/// Invalid command. Please provide name and new birthdate (in the format 'dd.mm.yyyy')."

    name = args[0]
    new_birthday = Birthday(datetime.strptime(args[1], "%d.%m.%Y").date())

    rec: Record = address_book.get(name)
    if rec:
        rec.birthday = new_birthday
        return f"/// Birthdate changed to {new_birthday} for contact {name}"
    else:
        return f"/// No contacts with name: \"{name}\" in the address book"


@input_error
def delete_handler(*args):
    if len(args) == 0:
        return "/// Invalid command. Please provide a name to delete."

    name = args[0]
    if name in address_book:
        del address_book[name]
        return f"/// Contact \"{name}\" deleted successfully."
    else:
        return f"/// Contact \"{name}\" not found."


@input_error
def search_handler(*args):
    if len(args) == 0:
        return "/// Invalid command. Please provide a search term."

    search_term = args[0].lower()
    matching_contacts = []

    for contact in address_book.get_all_contacts():
        if (search_term in str(contact.name).lower()) or any(search_term in str(phone.value).lower() for phone in contact.phones):
            matching_contacts.append(contact)

    if not matching_contacts:
        return f"/// No contacts found matching the search term: \"{search_term}\""
    
    output = [str(record) for record in matching_contacts]
    return "\n".join(output)


def exit_handler(*args):
    return "/// Good bye!"


@input_error
def unknown_handler(*args):
    return "/// Invalid command. Type \"help\" to show all commands."

def show_contacts_page(page_number):
    contacts = address_book.get_all_contacts()
    total_pages = (len(contacts) - 1) // 10 + 1
    if page_number < 1 or page_number > total_pages:
        return f"/// Invalid page number. Please provide a page number between 1 and {total_pages}."

    page_size = 10
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    contacts_page = contacts[start_index:end_index]
    if not contacts_page:
        return f"/// Page {page_number} is empty. Available pages: (1-{total_pages})."

    header = f"/// --- Contacts Page {page_number}/{total_pages} --- "
    output = [str(record) for record in contacts_page]
    page_content = "\n".join(output)
    footer = f"/// ---  End of Page {page_number}/{total_pages}  --- "

    return f"{header}\n{page_content}\n{footer}"


@input_error
def show_all_handler(*args):
    if len(args) == 0:
        return "/// Invalid command. Please provide 'all' or page number (e.g., '1', '2', 'sc all', 'sc 1', etc.)."

    if args[0] == "all":
        contacts = address_book.get_all_contacts()
        if contacts:
            output = [str(record) for record in contacts]
            return "\n".join(output)
        else:
            return "/// No contacts found in the address book."
    else:
        try:
            page_number = int(args[0])
            return show_contacts_page(page_number)
        except ValueError:
            return "/// Invalid page number. Please provide a positive integer page number or 'all'."


COMMANDS = {
    hello_handler: ("hello", "hi"),
    add_handler: ("add", "+", "plus"),
    cp_handler: ("changephone", "cp"),
    cd_handler: ("changebirthdate", "cb"),
    delete_handler: ("delete", "d"),
    search_handler: ("search", "find", "f"),
    exit_handler: ("bye", "exit", "break", "good bye", "close", "quit", "q"),
    show_all_handler: ("sc all", "showcontacts all", "sc", "showcontacts"),
    help_handler: ("help"),
}



def parser(text: str):
    if not text.strip():
        return unknown_handler, []

    command_parts = text.strip().split()
    cmd = command_parts[0]
    data = command_parts[1:] if len(command_parts) > 1 else []

    for handler, keywords in COMMANDS.items():
        if cmd.lower() in keywords:
            return handler, data
    return unknown_handler, []


def main():
    while True:
        user_input = input("/// ---> ")

        cmd, data = parser(user_input)

        result = cmd(*data)
        try:
            print(result)
        except IndexError:
            print(unknown_handler())

        if cmd == exit_handler:
            address_book.save_data()
            break


if __name__ == "__main__":
    main()