from prompt_toolkit import PromptSession


class Notebook:
    def __init__(self):
        self.notes = {}
        self.session = PromptSession()

    def add_note(self, parameters):
        if len(parameters) < 2:
            return 'Please enter title and content.'

        title = parameters[0]
        content = parameters[1:]
        self.notes[title] = ' '.join(content)
        return f'Note with title: "{title}" added.'

    def view_note(self, parameters):
        if len(parameters) != 1:
            return 'Please enter the title, to view.'

        title = parameters[0]
        if title in self.notes:
            return f'Title: {title}\Content: {self.notes[title]}'
        else:
            return f'Note with title: "{title}" was not found.'

    def show_all_notes(self):
        if not self.notes:
            return 'No notes.'

        output = "List of the notes:\n"
        for title, content in self.notes.items():
            output += f'Title: {title}\nContent: {content}\n\n'
        return output.strip()

    def edit_note(self, parameters):
        if len(parameters) != 1:
            return 'Please enter the title, to edit.'

        title = parameters[0]
        if title in self.notes:
            current_content = self.notes[title]
            new_content = self.session.prompt(f'You can now edit content of the note with title: "{title}": ',
                                              default=current_content)
            if new_content:
                self.notes[title] = new_content
                return f'NOte with title: "{title}" edited.'
            else:
                return f'Note with title: "{title}" was not edited.'
        else:
            return f'Note with title: "{title}" was not found.'

    def delete_note(self, parameters):
        if len(parameters) != 1:
            return 'Please enter the title, for deletion.'

        title = parameters[0]
        if title in self.notes:
            del self.notes[title]
            return f'Note with title: "{title}" deleted.'
        else:
            return f'Note with title: "{title}" was not found.'

