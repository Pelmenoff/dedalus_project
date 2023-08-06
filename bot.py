import difflib, datetime, requests, subprocess
from classes import AddressBook, Name, Phone, Birthday, Record

API_KEY = "653c3ccd328356a16a58c6dbd440c093"

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
/// "upcomingbirthdays" or "ub" - Show upcoming birthdays.
/// "delete [name]" or "d [name]" - Delete a contact from the address book.
/// "search [query]" or "find [query]" or "f [query]" - Search for contacts by name or phone number.
/// "showcontacts all" or "sc all" - Show all contacts.
/// "showcontacts [page_number]" or "sc [page_number]" - Show contacts page by page. Enter 'all' to show all contacts at once.
/// "addnote [name] [note]" or "an [name] [note]" - Add a note to a contact.
/// "shownotes [name]" or "sn [name]" - Show notes for a contact.
/// "searchnote [query]" or "findnote [query]" or "fn [query]" - Search for notes by content.
/// "sort" or "s" - Sort contacts and notes alphabetically.
/// "time" or "t" - Get the current time.
/// "weather" or "w" - Get the current weather.
/// "help" or "h" - Show this help message.
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

def upcoming_birthdays_handler(*args):
    if len(args) == 0:
        return "/// Invalid command. Please provide the number of days for upcoming birthdays."

    try:
        days = int(args[0])
        current_date = datetime.now().date()
        upcoming_birthdays = []

        for contact in address_book.get_all_contacts():
            birthday = contact.birthday
            if birthday:
                days_remaining = (birthday.date - current_date).days
                if 0 <= days_remaining <= days:
                    upcoming_birthdays.append((contact.name, birthday.date))

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

def get_weather(city):
    # Construct the API URL with the city name and API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        # Extract and return weather information if the API call is successful
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        return f"The current weather in {city} is {weather_description}. Temperature: {temperature}°C"
    else:
        return "Failed to retrieve weather information"
    
def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return f"The current time is {current_time}"

def sort_files(path):
    try:
        subprocess.run(["python", "sort.py", path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False


def exit_handler(*args):
    return "/// Good bye!"


@input_error
def unknown_handler(*args):
    return "/// Invalid command. Type \"help\" to show all commands."


notes = []

@input_error
def add_note_handler(*args):
    if len(args) < 2:
        return "/// Invalid command. Please provide a title and text for the note."

    title = args[0]
    text = args[1]

    tags = []
    if len(args) > 2:
        tags = args[2].split(',')

    note = {"title": title, "text": text, "tags": tags}
    notes.append(note)
    return "/// Note added successfully."

@input_error
def show_notes_handler(*args):
    if len(args) == 0:
        if not notes:
            return "/// No notes found."
        output = ["/// All Notes:"]
        for note in notes:
            output.append(f"Title: {note['title']}, Text: {note['text']}, Tags: {', '.join(note['tags'])}")
        return "\n".join(output)

    if args[0] == "all":
        return show_notes_handler([])
    else:
        try:
            page_number = int(args[0])
            notes_per_page = 5
            start_index = (page_number - 1) * notes_per_page
            end_index = start_index + notes_per_page
            notes_page = notes[start_index:end_index]
            if not notes_page:
                return f"/// Page {page_number} is empty. Available pages: 1 to {len(notes)//notes_per_page+1}"
            output = [f"/// Notes (Page {page_number}):"]
            for note in notes_page:
                output.append(f"Title: {note['title']}, Text: {note['text']}, Tags: {', '.join(note['tags'])}")
            return "\n".join(output)
        except ValueError:
            return "/// Invalid page number. Please provide a positive integer page number or 'all'."

@input_error
def search_notes_handler(*args):
    if len(args) == 0:
        return "/// Invalid command. Please provide a search term."

    search_term = args[0].lower()
    matching_notes = []

    for note in notes:
        if (search_term in note["title"].lower()) or (search_term in note["text"].lower()) or any(search_term in tag.lower() for tag in note["tags"]):
            matching_notes.append(note)

    if not matching_notes:
        return f"/// No notes found matching the search term: \"{search_term}\""

    output = ["/// Matching Notes:"]
    for note in matching_notes:
        output.append(f"Title: {note['title']}, Text: {note['text']}, Tags: {', '.join(note['tags'])}")

    return "\n".join(output)

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
    cp_handler: ("changephone", "cp"),
    cd_handler: ("changebirthdate", "cb"),
    upcoming_birthdays_handler: ("upcomingbirthdays", "ub"),
    delete_handler: ("delete", "d"),
    search_handler: ("search", "find", "f"),
    exit_handler: ("bye", "exit", "break", "good bye", "close", "quit", "q"),
    show_all_handler: ("sc all", "showcontacts all", "sc", "showcontacts"),
    add_note_handler: ("addnote", "an"),
    show_notes_handler: ("shownotes", "sn"),
    search_notes_handler: ("searchnote", "findnote", "fn"),
    sort_files: ("sort", "s"),
    get_current_time: ("time", "t"),
    get_weather: ("weather", "w"),
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