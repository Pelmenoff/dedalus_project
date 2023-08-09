import os
import pickle


class Notebook:
    def __init__(self):
        self.notes = {}

    def add_note(self, *parameters):
        if len(parameters) < 2:
            return '/// Please enter title and content.'

        title = parameters[0]
        content = parameters[1:]
        self.notes[title] = ' '.join(content)
        return f'/// Note with title: "{title}" added.'

    def view_note(self, *parameters):
        if len(parameters) != 1:
            return '/// Please enter the title, to view.'

        title = parameters[0]
        if title in self.notes:
            return f'/// Title: {title}\Content: {self.notes[title]}'
        else:
            return f'/// Note with title: "{title}" was not found.'

    def show_all_notes(self):
        if not self.notes:
            return '/// No notes.'

        output = "/// List of the notes:\n"
        for title, content in self.notes.items():
            output += f'/// Title: {title}\n/// Content: {content}\n/// \n'
        return output.strip()

    def edit_note(self, *parameters):
        if len(parameters) < 2:
            return '/// Please enter title and new content.'
        title = parameters[0]
        if title in self.notes:
            del self.notes[title]
        else:
            return f'/// Note with title: "{title}" was not found.'
        title = parameters[0]
        content = parameters[1:]
        self.notes[title] = ' '.join(content)
        return f'/// Note with title: "{title}" added.'

    def delete_note(self, *parameters):
        if len(parameters) != 1:
            return '/// Please enter the title, for deletion.'

        title = parameters[0]
        if title in self.notes:
            del self.notes[title]
            return f'/// Note with title: "{title}" deleted.'
        else:
            return f'/// Note with title: "{title}" was not found.'

    def save_to_file(self, filename):
        with open(filename, mode="wb") as file:
            pickle.dump(self.notes, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                if os.stat(filename).st_size == 0:
                    self.notes = {}
                else:
                    self.notes = pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError):
            self.notes = {}
            self.save_to_file(filename)