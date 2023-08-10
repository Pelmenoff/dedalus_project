# Dedalus - Personal Assistant and Organizer

Dedalus is a personal assistant and organizer built using Python. It allows you to manage contacts, notes, weather information, and more. This README provides an overview of the codebase and the available commands.

## Getting Started

### There is two ways how you can use Dedalus:

##### To install Dedalus on your device, follow these steps:
1. Download dedalus_project-1.2.3-py3-none-any.whl file to your device.
2. Install it using `pip install dedalus_project-1.2.3-py3-none-any.whl`.
3. Run cmd or powershell and activate Dedalus using `dedalusrun` command.

##### If you want to use Dedalus without installing, follow these steps:
1. Clone or download the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run `py -m dedalus_project.bot` in your preferred Python environment.

## Features
-Add, manage, and search for contacts with names, phone numbers, birthdays, and emails.
-Add, view, edit, and delete notes.
-Display upcoming birthdays.
-Retrieve current weather information.
-Display current time.
-Sort files in a directory based on categories.

### Contact Management

Dedalus allows you to manage your contacts efficiently. You can add, update, and delete contacts, change their phone numbers, birthdates, and emails.

Available commands:
- `add [name] [phone] [birthday] [email]`: Add a contact with an optional birthday and email.
- `changephone [name] [old_phone] [new_phone]`: Change a contact's phone number.
- `changebirthdate [name] [new_date]`: Change a contact's birthdate.
- `changeemail [name] [new_email]`: Change a contact's email.
- `changename [name] [new_name]` or `rename [name] [new_name]`: Change a contact's name.
- `delete [name]`: Delete a contact.
- `search [query]` or `find [query]`: Search for contacts by name or phone number.
- `upcomingbirthdays [number of days]`: Show upcoming birthdays.
- `showcontacts all`: Show all contacts.
- `showcontacts [page_number]`: Show contacts page by page.
- `shortcommands` or `short`: Show a list of short versions of all commands.

### Note Management

You can also manage notes with Dedalus. Create, view, edit, and delete notes as needed.

Available commands:
- `addnote [title] [content]`: Add a note.
- `shownotes`: Show all notes.
- `searchnote [title]` or `findnote [query]`: Search for notes by title.
- `editnote [title] [new_content]`: Edit a note's content.
- `deletenote [title]`: Delete a note.

### Weather Information

Dedalus can provide you with current weather information for a specific city.

Available command:
- `weather [city]`: Get the current weather for a city.

### Time

You can also get the current time using the Dedalus assistant.

Available command:
- `time`: Get the current time.

### Sorting Files

Dedalus offers a file sorting feature where you can sort files in a given directory into categories like images, videos, documents, audio, and archives.

Available command:
- `sort [path]`: Sort files in the specified directory.

### Help

For a complete list of available commands and their descriptions, use the following command:

- `help`: Show a help message with all available commands.

### Exiting

To exit the Dedalus assistant, you can use any of the following commands:

- `exit`, `bye`, `good bye`, `close`, `quit`

## Usage Examples

Here are a few usage examples to help you get started:

- To add a contact: `add John Doe +1234567890 10.08.1985`
- To change a phone number: `changephone John +1234567890 +9876543210`
- To search for contacts: `search John`
- To add a note: `addnote Meeting Agenda Discuss project updates`
- To get the current weather: `weather New York`
- To see upcoming birthdays: `upcomingbirthdays 7`
- To exit the assistant: `exit`

## Note

This README provides an overview of the Dedalus assistant's features and usage. Make sure to explore the available commands and functionalities for a complete experience.