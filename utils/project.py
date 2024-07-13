from nicegui import app, events, ui
import io
import pandas as pd
import json
#the create_braille_table function is used to create the braille table for lib louis
#the create_braille_tests function is used to create the braille tests for lib louis
#the get_braille_from_text_in_source function is used to convert the text characters to braille characters in the source language file
from braille import create_braille_table, create_braille_tests, get_braille_from_text_in_source
#The create_filtered_csv function is used to create the filtered csv file
#The regenerate_characters_using_hex function is used to regenerate the characters in the language source file
from csv import create_filtered_csv, regenerate_characters_using_hex
#The add_characters_to_nvda function is used to add the symbols to the nvda symbols file
#The generate_locale_file function is used to generate the locale file for nvda
#The generate_character_set function is used to generate the character set for nvda
from nvda import add_characters_to_nvda,generate_locale_file, generate_character_set


# Function to load languages from JSON file
def load_languages():
    try:
        with open("utils/languages_file.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

#Loads the languages from the JSON file
languages = load_languages()


class Project:
    def __init__(self):
        self.project_name = None
        self.project_text = None
        self.project_name_column = None
        self.project_character_column = None
        self.project_unicode_column = None
        self.project_type_column = None
        self.project_braille_column = None
        self.user_actions=[]
        self.actions={"Add Characters to NVDA":add_characters_to_nvda,"Download Files for NVDA":generate_locale_file,"Write Table for Lib Louis":create_braille_table,"Write Test for Lib Louis":create_braille_tests}

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

    def update_user_actions(self,e:events.ValueChangeEventArguments):
        self.user_actions=e.value

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
        ui.notify("Project Saved",close_button="Ok")

    def remove_project(self):
        """
        Remove the project from the languages file
        """
        global languages
        removed=False
        if not self.project_name ==None:
            new_languages=filter(self.check_language_names,languages)
            if len(new_languages) < len(languages):
                removed=True
            languages=list(new_languages)
            with open("utils/languages_file.json","w",encoding="utf-8") as file:
                json.dump(languages,file,ensure_ascii=False,indent=4)
        if removed:
            ui.notify("Project Removed",close_button="Ok")
        else:
            ui.notify("Project not found",close_button="Ok")

    def check_language_names(self,language):
        """
        Check if the language name is the same as the project name.
    
        Parameters:
    language: The language to be checked.

    Returns:
    True if the language name is not the same as the project name, False otherwise.
        """
    
        if language["name"]==self.project_name:
            return False
        else:
            return True

    def perform_actions(self):
        for action in self.user_actions:
            ui.notify(action)


project = Project()
