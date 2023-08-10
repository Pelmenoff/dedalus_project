import difflib, datetime, requests, subprocess, os, sys
from .classes import AddressBook, Name, Phone, Birthday, Email, Record
from datetime import datetime
from .notebook import Notebook

bot_ver = 'Dedalus v1.2.4'

API_KEY = "653c3ccd328356a16a58c6dbd440c093"

address_book = AddressBook()
notebook = Notebook()
save_path = "notebook_data.pickle"


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "/// Contact not found."
        except ValueError:
            return "/// Invalid input. Provide valid information."
        except IndexError:
            return "/// Invalid command. Type \"help\" to show all commands."
    return wrapper


help_info = """/// Commands:
/// "add [name] [phone] [birthday]" - Add a contact to the address book. Birthday is optional. Example: add John +1234567890 10.08.1985
/// "changephone [name] [old_phone] [new_phone]" - Change the phone number for a contact. Example: changephone John +1234567890 +9876543210
/// "changebirthdate [name] [new_date]" - Change the birthdate for a contact. Example: changebirthdate John 10.08.1990
/// "changeemail [name] [new_email]" - Change the email for a contact. Example: changeemail John john@example.com
/// "changename [name] [new_name]" or "rename [name] [new_name]" - Change the name of a contact. Example: changename John Bill
/// "upcomingbirthdays [number of days]" - Show upcoming birthdays. Example: upcomingbirthdays 7
/// "delete [name]" - Delete a contact from the address book. Example: delete John
/// "search [query]" or "find [query]" - Search for contacts by name or phone number. Example: search John
/// "showcontacts all" - Show all contacts. Example: showcontacts all
/// "showcontacts [page_number]" - Show contacts page by page. Enter 'all' to show all contacts at once. Example: showcontacts 2
/// "addnote [title] [content]" - Add a note.
/// "shownotes" - Show all notes.
/// "searchnote [title]" or "findnote [query]" - Search for notes with title. Example: searchnote Meeting
/// "editnote [title] [new_content]" - Editting note with given title.
/// "deletenote [title]" - Delliting note with given title.
/// "sort [path]" - Sort contacts and notes alphabetically. Example: sort D:\Folder
/// "weather [city]" - Get the current weather. Example: weather New York
/// "time" - Get the current time.
/// "help" - Show this help message.
/// "short" - List of short versions of all commands.
/// "exit", "bye", "good bye", "close", "quit" - Turn off the assistant."""

short_commands = """/// Commands:
/// "add [name] [phone] [birthday]" - Add a contact. Example: add John +1234567890 10.08.1985
/// "cp [name] [old_phone] [new_phone]" - Change phone number. Example: cp John +1234567890 +9876543210
/// "cb [name] [new_date]" - Change birthdate. Example: cb John 10.08.1990
/// "ce [name] [new_email]" - Change email. Example: ce John john@example.com
/// "cn [name] [new_name]" - Change name. Example: cn John Bill
/// "ub [number of days]" - Show upcoming birthdays. Example: ub 7
/// "d [name]" - Delete a contact. Example: d John
/// "f [query]" - Search for contacts. Example: f John
/// "sc all" - Show all contacts. Example: sc all
/// "sc [page_number]" - Show contacts page by page. Enter 'all' to show all contacts at once. Example: sc 2
/// "an [title] [content] [tag]" - Add a note.
/// "sn" - Show all notes.
/// "fn [title]" - Search for note with given title.
/// "en [title] [new_content]" - Editting note with given title.
/// "dn [title]" - Delliting note with given title.
/// "s [path]" - Sort contacts and notes alphabetically. Example: s D:\Folder
/// "w [city]" - Get the current weather. Example: w New York
/// "t" - Get the current time.
/// "h" - Show help message.
/// "q" - Turn off the assistant."""


@input_error
def hello_handler(*args):
    return "/// How can I help you?"


@input_error
def help_handler(*args):
    return f"{help_info}"

@input_error
def short_commands_handler(*args):
    return f"{short_commands}"


@input_error
def add_handler(*args):
    if len(args) < 2:
        return "/// Invalid command. Please provide name and phone."

    name = str(Name(args[0]))
    phone = str(args[1])
    birthday = None
    email = None

    if len(args) == 3:
        try:
            birthday = Birthday(datetime.strptime(args[2], "%d.%m.%Y").date())
        except ValueError:
            email = Email(args[2])
    elif len(args) == 4:
        try:
            birthday = Birthday(datetime.strptime(args[2], "%d.%m.%Y").date())
            email = Email(args[3])
        except ValueError:
            birthday = Birthday(datetime.strptime(args[3], "%d.%m.%Y").date())
            email = Email(args[2])
    elif len(args) == 5:
        try:
            email = Email(args[4])
            birthday = Birthday(datetime.strptime(args[3], "%d.%m.%Y").date())
        except ValueError:
            birthday = Birthday(datetime.strptime(args[4], "%d.%m.%Y").date())
            email = Email(args[3])

    rec: Record = address_book.get(name)
    if rec:
        if any(str(phone) == existing_phone.value for existing_phone in rec.phones):
            return f"/// Phone number {phone} already exists for contact: {name}."
        return rec.add_phone(phone)

    address_book.add_record(name, phone, birthday, email)
    message = f"/// Contact {name}: {phone} added successfully."
    if birthday:
        message += f" Birthday: {birthday}"
    if email:
        message += f" Email: {email}"
    return message

@input_error
def change_phone_handler(*args):
    if len(args) < 3:
        return "/// Invalid command. Please provide name, old phone, and new phone."

    name = args[0]
    old_phone = args[1]
    new_phone = args[2]

    rec: Record = address_book.get(name)
    if rec:
        if any(str(phone) == old_phone for phone in rec.phones):
            rec.change_phone(old_phone, new_phone)
            return f"/// Phone number changed from {old_phone} to {new_phone} for contact: {name}"
        else:
            return f"/// Phone number {old_phone} not found for contact: {name}"
    else:
        return f"/// No contacts with name: \"{name}\" in the address book"


@input_error
def change_birthdate_handler(*args):
    if len(args) < 2:
        return "/// Invalid command. Please provide name and new birthdate (in the format 'dd.mm.yyyy')."

    name = args[0]
    new_birthday = Birthday(datetime.strptime(args[1], "%d.%m.%Y").date())

    rec: Record = address_book.get(name)
    if rec:
        rec.birthday = new_birthday
        return f"/// Birthdate changed to {new_birthday} for contact: {name}"
    else:
        return f"/// No contacts with name: \"{name}\" in the address book"
    
@input_error
def change_email_handler(*args):
    if len(args) < 2:
        return "/// Invalid command. Please provide name and new email."

    name = args[0]
    new_email = args[1]

    rec: Record = address_book.get(name)
    if rec:
        rec.email = new_email
        return f"/// Email changed to {new_email} for contact: {name}"
    else:
        return f"/// No contacts with name: \"{name}\" in the address book"
    
@input_error
def change_name_handler(*args):
    if len(args) < 2:
        return "/// Invalid command. Please provide name and new name."

    old_name = args[0]
    new_name = args[1]

    rec: Record = address_book.get(old_name)
    if rec:
        rec.name.value = new_name
        return f"/// Name changed \"{old_name}\" ---> \"{new_name}\"."
    else:
        return f"/// No contacts with name: \"{old_name}\" in the address book"

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

@input_error
def upcoming_birthdays_handler(*args):
    if len(args) == 0:
        return "/// Invalid command. Please provide the number of days for upcoming birthdays."

    try:
        days = int(args[0])
        current_date = datetime.now().date()

        upcoming_birthdays = []

        for contact in address_book.get_all_contacts():
            birthday = contact.birthday.value
            if birthday:
                next_birthday = datetime(current_date.year, birthday.month, birthday.day).date()
                if next_birthday < current_date:
                    next_birthday = datetime(current_date.year + 1, birthday.month, birthday.day).date()
                days_remaining = (next_birthday - current_date).days
                if 0 <= days_remaining <= days:
                    upcoming_birthdays.append((contact.name.value, next_birthday))

        if not upcoming_birthdays:
            return f"/// No upcoming birthdays in the next {days} days."

        upcoming_birthdays.sort(key=lambda x: x[1])
        output = ["/// Upcoming Birthdays:"]
        for name, date in upcoming_birthdays:
            output.append(f"{name}: {date.strftime('%d.%m.%Y')}")
        return "\n".join(output)

    except ValueError:
        return "/// Invalid number of days. Please provide a positive integer."

    
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

def get_weather(*args):
    city = " ".join(args)

    if not city:
        return "/// Invalid command. Please provide the name of a city for weather information."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        return f"/// The current weather in {city} is {weather_description}. Temperature: {temperature}°C"
    else:
        return "/// Failed to retrieve weather information"
    
def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"/// The current time is {current_time}"

def sort_files(path):
    sort_script_path = os.path.join(os.path.dirname(__file__), "sort.py")
    try:
        subprocess.run([sys.executable, sort_script_path, path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False


def exit_handler(*args):
    notebook.save_to_file(save_path)
    return "/// Good bye!"


@input_error
def unknown_handler(*args):
    return "/// Invalid command. Type \"help\" to show all commands."

def add_note_handler(*data):
     return notebook.add_note(*data)

def show_all_notes_handler(*data):
    return notebook.show_all_notes(*data)


def view_note_handler(*data):
    return notebook.view_note(*data)


def edit_note_handler(*data):
    return notebook.edit_note(*data)

def delete_note_handler(*data):
    return notebook.delete_note(*data)

def find_closest_command(input_text):
    closest_command = ""
    max_similarity = 0

    for handler, keywords in COMMANDS.items():
        for keyword in keywords:
            similarity = difflib.SequenceMatcher(None, input_text, keyword).ratio()
            if similarity > max_similarity:
                max_similarity = similarity
                closest_command = keyword

    return closest_command

COMMANDS = {
    hello_handler: ("hello", "hi"),
    add_handler: ("add", "+", "plus"),
    change_phone_handler: ("changephone", "cp"),
    change_birthdate_handler: ("changebirthdate", "cb"),
    change_email_handler: ("changeemail", "ce"),
    change_name_handler: ("changename", "rename", "cn"),
    upcoming_birthdays_handler: ("upcomingbirthdays", "ub"),
    delete_handler: ("delete", "d"),
    search_handler: ("search", "find", "f"),
    exit_handler: ("bye", "exit", "break", "good bye", "close", "quit", "q"),
    show_all_handler: ("sc all", "showcontacts all", "sc", "showcontacts"),
    add_note_handler: ("addnote", "an"),
    show_all_notes_handler: ("shownotes", "sn"),
    view_note_handler: ("searchnote", "findnote", "fn"),
    edit_note_handler: ("editnote", "en"),
    delete_note_handler: ("deletenote", "dn"),
    sort_files: ("sort", "s"),
    get_current_time: ("time", "t"),
    get_weather: ("weather", "w"),
    short_commands_handler: ("shortcommands", "short"),
    help_handler: ("help", "h"),
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
    notebook.load_from_file(save_path)

    print(f"/// \U0001F916 {bot_ver} loaded. Waiting for command. \"help\" to show list of all commands.")

    while True:
        user_input = input("/// ---> ")

        cmd, data = parser(user_input)

        if cmd == unknown_handler:
            print(f"/// Invalid command. Did you mean '{find_closest_command(user_input)}'?")
            continue

        try:
            result = cmd(*data)
            print(result)
        except Exception as e:
            print(f"/// Error: {e}")

        if cmd == exit_handler:
            address_book.save_data()
            break


if __name__ == "__main__":
    main()