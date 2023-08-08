import datetime, requests, subprocess
from contacts import Name, Phone, Record, AddressBook, Birthday
from decorators import input_error

# API key for OpenWeatherMap API
API_KEY = "653c3ccd328356a16a58c6dbd440c093"

# Initialize the AddressBook object with the file name "contacts.csv"
contacts = AddressBook("contacts.csv")

# Function to add a birthday to a contact
def add_birthday(name, birthday):
    # Find matching names (case-insensitive) in the contacts
    matching_names = [n for n in contacts if n.lower() == name.lower()]
    if matching_names:
        # If the name is found, update the contact's birthday and save changes to disk
        record = contacts[matching_names[0]]
        record.birthday.day = birthday.day
        record.birthday.month = birthday.month
        contacts.save_data()
        return "Birthday added successfully"
    else:
        return "Contact not found"

# Function to add a new contact or edit an existing one
@input_error
def add_contact(name, phone=None, birthday=None):
    name = Name(name)
    phone = Phone(phone) if phone else None
    birthday = Birthday(birthday) if birthday else None
    rec: Record = contacts.get(str(name))
    if rec:
        rec.add_phone(phone)
        rec.birthday = birthday
    else:
        record = Record(name, phone, birthday)
        contacts.add_record(record)
    return "Contact added successfully"

# Function to change the phone number of an existing contact
@input_error
def change_contact(name, old_phone, new_phone):
    name = Name(name)
    rec = contacts[str(name)]
    if rec:
        old = Phone(old_phone)
        new = Phone(new_phone)
        rec.edit_phone(old, new_phone)
        contacts.save_data()
        return "Contact updated successfully"
    else:
        return "Contact not found"

# Function to get the phone number(s) of a contact
@input_error
def get_phone(name):
    matching_records = [record for record in contacts.values() if record.name.value.lower() == name.lower()]
    if matching_records:
        record = matching_records[0]
        return ", ".join([str(phone) for phone in record.phones])
    else:
        return "Contact not found"

# Function to search for contacts by name or phone
@input_error
def search_contacts(query):
    results = contacts.search_records(query)
    if results:
        output = ""
        for record in results.values():
            output += str(record)
        return output
    else:
        return "No contacts found"

# Function to show all saved contacts
def show_all_contacts():
    if contacts:
        output = ""
        for record in contacts.values():
            output += str(record)
        return output
    else:
        return "No contacts found"

# Function to get the current weather in a specified city using OpenWeatherMap API
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

# Function to get the current time
def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return f"The current time is {current_time}"

# Function to sort files in the specified directory using sort.py script
def sort_files(path):
    try:
        subprocess.run(["python", "sort.py", path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False

# Function to display available commands
def help_commands():
    return """
    Available commands:
    - hello: Greet the assistant
    - add <name> <phone> [birthday]: Add a contact with the given name, phone number, and the birthday (argument is provided in the format "DD/MM," the assistant will add the contact's birthday).
    - change <name> <old_phone> <new_phone>: Change the phone number of an existing contact
    - phone <name>: Get the phone number(s) of a contact
    - search <query>: Search contacts by name or phone
    - show all: Show all saved contacts
    - sort <path>: Sort selected folder
    - weather <city>: Get the current weather in the specified city
    - time: Get the current time
    - help: Show available commands
    - goodbye, close, exit: Close the assistant
    """

# Function to parse user input and execute corresponding commands
def parse_command(user_input):
    command = user_input[0]
    arguments = user_input[1:]

    if command == "hello":
        return "How can I help you?"
    elif command == "add":
        # Check if the user provided enough arguments to add a contact
        if len(arguments) >= 2:
            name = arguments[0]
            phone = arguments[-1]
            birthday = None
            if "/" in phone:  # Check if the last argument contains the birthday
                day, month = phone.split("/")
                try:
                    birthday = Birthday(int(day), int(month))
                except ValueError:
                    raise ValueError("Invalid birthday format. Use DD/MM format for the birthday.")
                phone = arguments[-2]  # Update phone to exclude the birthday
            return add_contact(name, phone, birthday)
        elif len(arguments) == 1:
            raise ValueError("Give me both name and phone, or only the name.")
        else:
            raise ValueError("Give me name and phone please")
    elif command == "change":
        if len(arguments) == 3:
            name, old_phone, new_phone = arguments
            return change_contact(name, old_phone, new_phone)
        else:
            raise ValueError("Give me name, old phone, and new phone please")
    elif command == "phone":
        if len(arguments) == 1:
            name = arguments[0]
            return get_phone(name)
        else:
            raise ValueError("Enter user name")
    elif command == "search":
        if len(arguments) == 1:
            query = arguments[0]
            search_results = contacts.search_records(query)
            if search_results:
                output = ""
                for record in search_results.values():
                    output += str(record)
                return output
            else:
                return "No matching contacts found"
        else:
            raise ValueError("Invalid command. Type 'help' to see the available commands.")
    elif command == "show":
        if len(arguments) == 1 and arguments[0] == "all":
            page_size = 10  # Set the desired page size
            contacts.set_page_size(page_size)
            output = ""
            for page in contacts.iterator():
                for record in page:
                    output += str(record)
            return output
        else:
            raise ValueError("Invalid command. Type 'help' to see the available commands.")
    elif command == "birthday":
        if len(arguments) >= 2:
            name = " ".join(arguments[:-1])
            date_str = arguments[-1]
            day, month = map(int, date_str.split("/"))
            birthday = Birthday(day, month)
            return add_birthday(name, birthday)
        else:
            raise ValueError("Give me name and birthday (in the format DD/MM) please")
    elif command == "weather":
        if len(arguments) == 1:
            city = arguments[0]
            return get_weather(city)
        else:
            raise ValueError("Enter city name")
    elif command == "time":
        return get_current_time()
    elif command == "help":
        return help_commands()
    elif command == "sort":
        if len(arguments) == 1:
            path = arguments[0]
            sort_files(path)
    elif command in ["good", "bye", "close", "exit"]:
        return "Good bye!"
    else:
        return "Invalid command. Type 'help' to see the available commands."

# Function to run the assistant and interact with the user
def main():
    print("Welcome to the Assistant! How can I help you?")
    contacts.load_data()  # Load address book data from the file
    while True:
        try:
            user_input = input("Enter a command: ").lower().split(" ")
            result = parse_command(user_input)
            print(result)
            if result == "Good bye!":
                break
        except Exception as e:
            print(str(e))
    contacts.save_data()  # Save address book data to the file before exiting

if __name__ == "__main__":
    main()