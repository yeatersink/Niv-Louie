from nicegui import app, events, ui
import io
import pandas as pd
import json


# Function to load languages from JSON file
def load_languages():
    try:
        with open("utils/languages_file.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

class Project:
    def __init__(self):
        self.project_name = None
        self.project_text = None
        self.project_name_column = None
        self.project_character_column = None
        self.project_unicode_column = None
        self.project_type_column = None
        self.project_braille_column = None
        self.project_language_code = None
        self.project_language_system_code=None
        self.project_display_name=None
        self.project_index_name=None
        self.project_supported_braille_languages=None
        self.project_language_information=None
        self.project_contributors=None
        self.project_included_braille_tables=None
        self.project_test_display_type=None
        self.project_replace=None
        #Loads the languages from the JSON file
        self.languages = load_languages()
        self.languages_list = [language["name"] for language in self.languages]


    def update_languages_list(self):
        self.languages_list = [language["name"] for language in self.languages]

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

        for language in self.languages:
            if self.project_name.lower() == language["name"].lower():
                ui.notify("A project with that name already exists.",type="negative")

        if error:
            return

        project_object= {"name":self.project_name,"name_column":self.project_name_column,"char_column":self.project_character_column,"braille_column":self.project_braille_column,"type_column":self.project_type_column,"unicode_column":self.project_unicode_column}
        self.languages.append(project_object)
        self.update_languages_list()
        with open("utils/languages_file.json", "w", encoding="utf-8") as file:
            json.dump(self.languages, file, ensure_ascii=False, indent=4)
        project.project_text.to_csv("languages/source/"+project.project_name+".csv",index=False)

        ui.navigate.to("/existing_project")
        ui.notify("Project Saved",close_button="Ok")


    def remove_project(self):
        """
        Remove the project from the languages file
        """

        removed=False
        if self.project_name != None:
            new_languages=list(filter(self.check_language_names,self.languages))
            if len(new_languages) < len(self.languages):
                removed=True
            self.languages=list(new_languages)
            self.update_languages_list()
            with open("utils/languages_file.json","w",encoding="utf-8") as file:
                json.dump(self.languages,file,ensure_ascii=False,indent=4)
        if removed == True:
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

    def set_all_fields(self):
        if self.project_name==None:
            ui.notify("No Project Selected!",type="negative")
            return
        current_language=None
        for language in self.languages:
            if language["name"]==self.project_name:
                current_language=language
        if current_language==None:
            ui.notify("Couldn't Find that Project!",type="negative")
            return
        self.project_name_column=current_language["name_column"]
        self.project_character_column=current_language["character_column"]
        set.project_unicode_column=current_language["unicode_column"]
        self.project_type_column=current_language["type_column"]
        self.project_braille_column=current_language["braille_column"]


project = Project()
