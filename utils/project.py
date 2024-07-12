from nicegui import app, events, ui
import io
import pandas as pd
import json


class Project:
    def __init__(self):
        self.project_name = None
        self.project_text = None
        self.project_name_column = None
        self.project_character_column = None
        self.project_unicode_column = None
        self.project_type_column = None
        self.project_braille_column = None

    def update_project_name(self, e: events.ValueChangeEventArguments):
        self.project_name = e.value


    def update_project_name_column(self, e: events.ValueChangeEventArguments):
        self.project_name_column = e.value

    def update_project_character_column(self, e: events.ValueChangeEventArguments):
        self.project_character_column = e.value

    def update_project_unicode_column(self, e: events.ValueChangeEventArguments):
        self.project_unicode_column = e.value

    def update_project_type_column(self, e: events.ValueChangeEventArguments):
        self.project_type_column = e.value

    def update_project_braille_column(self, e: events.ValueChangeEventArguments):
        self.project_braille_column = e.value

    def handle_file_upload(self, e: events.UploadEventArguments):
        self.project_name = e.name.split(".")[0]
        content_as_file = io.StringIO(e.content.read().decode("utf-8"))
        self.project_text = pd.read_csv(content_as_file)

    def save_project(self):
        error=False
        if self.project_name is None:
            ui.notify("Please enter a name for your project.", type="negative")
            error=True
        if self.project_name_column is None:
            ui.notify("Please select a name column for your project.", type="negative")
            error=True
        if self.project_character_column is None:
            ui.notify("Please select a character column for your project.", type="negative")
            error=True
        if self.project_unicode_column is None:
            ui.notify("Please select a Unicode column for your project.", type="negative")
            error=True
        if self.project_type_column is None:
            ui.notify("Please select a type column for your project.", type="negative")
            error=True
        if self.project_braille_column is None:
            ui.notify("Please select a braille column for your project.", type="negative")
            error=True

        for language in languages:
            if self.project_name.lower() == language["name"].lower():
                ui.notify("A project with that name already exists.",type="negative")

        if error:
            return

        project_object= {"name":self.project_name,"name_column":self.project_name_column,"char_column":self.project_character_column,"braille_column":self.project_braille_column,"type_column":self.project_type_column,"unicode_column":self.project_unicode_column}
        languages.append(project_object)
        with open("utils/languages_file.json", "w", encoding="utf-8") as file:
            json.dump(languages, file, ensure_ascii=False, indent=4)
        project.project_text.to_csv("languages/source/"+project.project_name+".csv",index=False)
        ui.navigate.to("/existing_project")

        
project = Project()

# Function to load languages from JSON file
def load_languages():
    try:
        with open("utils/languages_file.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

#Loads the languages from the JSON file
languages = load_languages()

def remove_project(dialog):
    """
    Remove the project from the languages file and close the dialog.
    
    Parameters:
    dialog: The dialog to be closed.
    """
    if not project.project_name ==None:
        new_languages=filter(check_language_names,languages)
        languages=list(new_languages)
        with open("utils/languages_file.json","w",encoding="utf-8") as file:
            json.dump(languages,file,ensure_ascii=False,indent=4)
        dialog.close
        ui.notify("Project Removed",close_button="Ok")

def check_language_names(language):
    """
    Check if the language name is the same as the project name.
    
    Parameters:
language: The language to be checked.

Returns:
True if the language name is not the same as the project name, False otherwise.
	"""
    
    if language["name"]==project.project_name:
        return False
    else:
        return True
