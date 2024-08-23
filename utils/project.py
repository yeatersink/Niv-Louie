from nicegui import app, events, ui
import io
import os
from pathlib import Path
import pandas as pd
import json
from docx import Document
import warnings


appdata_dir=os.getenv("LOCALAPPDATA")
niv_louie_app_data=os.path.join(appdata_dir,"Niv_Louie")
os.makedirs(niv_louie_app_data,exist_ok=True)


#The braille_test_converter.json file is opened and read in to the braille_test_object variable
braille_test_file=open("utils/braille_test_converter.json",encoding="utf8")
braille_converter_object=json.load(braille_test_file)

#The braille_numbers.json file is opened and read in to the braille_numbers_object variable
braille_numbers_file=open("utils/braille_to_numbers.json",encoding="utf8")
braille_numbers_object=json.load(braille_numbers_file)


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

    def load_language_source(self):        self.project_text=pd.read_csv(os.path.join(niv_louie_app_data,"languages","source",self.project_name+".csv"))

    def set_project_name(self, project_name):
        self.project_name = project_name

    def update_project_name(self, e: events.ValueChangeEventArguments):
        self.project_name = e.value
        self.set_all_fields()


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

    def update_project_language_code(self, e: events.ValueChangeEventArguments):
        self.project_language_code = e.value
        
    def update_project_language_system_code(self, e: events.ValueChangeEventArguments):
        self.project_language_system_code = e.value

    def update_project_display_name(self, e: events.ValueChangeEventArguments):
        self.project_display_name = e.value

    def update_project_index_name(self, e: events.ValueChangeEventArguments):
        self.project_index_name = e.value

    def update_project_supported_braille_languages(self, e: events.ValueChangeEventArguments):
        self.project_supported_braille_languages = e.value.split(",")

    def update_project_language_information(self, e: events.ValueChangeEventArguments):
        self.project_language_information = e.value

    def update_project_contributors(self, e: events.ValueChangeEventArguments):
        self.project_contributors = e.value

    def update_project_included_braille_tables(self, e: events.ValueChangeEventArguments):
        self.project_included_braille_tables = e.value.split(",")

    def update_project_test_display_type(self, e: events.ValueChangeEventArguments):
        self.project_test_display_type = e.value

    def update_project_replace(self, e: events.ValueChangeEventArguments):
        self.project_replace = e.value.split(",")

    def handle_file_upload(self, e: events.UploadEventArguments):
        self.project_name = e.name.split(".")[0]
        content_as_file = io.StringIO(e.content.read().decode("utf-8"))
        self.project_text = pd.read_csv(content_as_file)


    def handle_test_upload(self, e: events.UploadEventArguments):
        self.set_all_fields()
        content_as_file = io.StringIO(e.content.read().decode("utf-8"))
        test_file= pd.read_csv(content_as_file)
        test_path=os.path.join(niv_louie_app_data,"braille_tests")
        if os.path.exists(test_path)==False:
            os.makedirs(test_path,exist_ok=True)
        test_file.to_csv("braille_tests/"+self.project_language_code+".csv",index=False)
        ui.notify("Test file for Lib Louis has been Saved. ")


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
        if self.project_language_code is None:
            ui.notify("Please enter a language code for your project.", type="negative")
            error=True
        if self.project_display_name is None:
            ui.notify("Please enter a display name for your project.", type="negative")
            error=True
        if self.project_language_information is None:
            ui.notify("Please enter language information for your project.", type="negative")
            error=True
        if self.project_contributors is None:
            ui.notify("Please enter contributors for your project.", type="negative")
            error=True
        if self.project_test_display_type is None:
            ui.notify("Please enter a test display type for your project.", type="negative")
            error=True
        if self.project_replace is None:
            ui.notify("Please enter replace for your project.", type="negative")
            error=True
        if self.project_supported_braille_languages is None:
            self.project_supported_braille_languages = []
        if self.project_included_braille_tables is None:
            self.project_included_braille_tables = []
        if self.project_index_name is None:
            self.project_index_name = ""
        if self.project_language_system_code is None:
            self.project_language_system_code = ""

        for language in self.languages:
            if self.project_name.lower() == language["name"].lower():
                ui.notify("A project with that name already exists.",type="negative")
                error=True

        if error:
            return

        project_object= {
            "name":self.project_name,
            "name_column":self.project_name_column,
            "char_column":self.project_character_column,
            "braille_column":self.project_braille_column,
            "type_column":self.project_type_column,
            "unicode_column":self.project_unicode_column,
            "language_code":self.project_language_code,
            "language_system_code":self.project_language_system_code,
            "display_name":self.project_display_name,
            "index_name":self.project_index_name,
            "supported_braille_languages":self.project_supported_braille_languages,
            "language_information":self.project_language_information,
            "contributors":self.project_contributors,
            "included_braille_tables":self.project_included_braille_tables,
            "test_display_type":self.project_test_display_type,
            "replace":self.project_replace
            }
        self.languages.append(project_object)
        self.update_languages_list()
        language_source_folder=os.path.join(niv_louie_app_data,"languages","source")
        if os.path.exists(language_source_folder) == False:
            os.makedirs(language_source_folder,exist_ok=True)
        with open("utils/languages_file.json", "w", encoding="utf-8") as file:
            json.dump(self.languages, file, ensure_ascii=False, indent=4)
        project.project_text.to_csv(os.path.join(language_source_folder,project.project_name+".csv"),index=False)

        ui.navigate.to("/existing_project")
        ui.notify("Project Saved",close_button="Ok")


    def save_existing_project(self,old_project_name):
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
        if self.project_language_code is None:
            ui.notify("Please enter a language code for your project.", type="negative")
            error=True
        if self.project_display_name is None:
            ui.notify("Please enter a display name for your project.", type="negative")
            error=True
        if self.project_language_information is None:
            ui.notify("Please enter language information for your project.", type="negative")
            error=True
        if self.project_contributors is None:
            ui.notify("Please enter contributors for your project.", type="negative")
            error=True
        if self.project_test_display_type is None:
            ui.notify("Please enter a test display type for your project.", type="negative")
            error=True
        if self.project_replace is None:
            ui.notify("Please enter replace for your project.", type="negative")
            error=True
        if self.project_supported_braille_languages is None:
            self.project_supported_braille_languages = []
        if self.project_included_braille_tables is None:
            self.project_included_braille_tables = []
        if self.project_index_name is None:
            self.project_index_name = ""
        if self.project_language_system_code is None:
            self.project_language_system_code = ""

        if self.project_name.lower() != old_project_name.lower():
            for language in self.languages:
                if self.project_name.lower() == language["name"].lower():
                    ui.notify("A project with that name already exists.",type="negative")
                    error=True

        if error:
            return


        project_object= {
            "name":self.project_name,
            "name_column":self.project_name_column,
            "char_column":self.project_character_column,
            "braille_column":self.project_braille_column,
            "type_column":self.project_type_column,
            "unicode_column":self.project_unicode_column,
            "language_code":self.project_language_code,
            "language_system_code":self.project_language_system_code,
            "display_name":self.project_display_name,
            "index_name":self.project_index_name,
            "supported_braille_languages":self.project_supported_braille_languages,
            "language_information":self.project_language_information,
            "contributors":self.project_contributors,
            "included_braille_tables":self.project_included_braille_tables,
            "test_display_type":self.project_test_display_type,
            "replace":self.project_replace
            }
        if self.project_name.lower() != old_project_name.lower():
            self.languages.append(project_object)
        else:
            for language in self.languages:
                if language["name"].lower() == old_project_name.lower():
                    language=project_object
        self.update_languages_list()
        language_source_folder=os.path.join(niv_louie_app_data,"languages","source")
        if os.path.exists(language_source_folder) == False:
            os.makedirs(language_source_folder,exist_ok=True)
        with open("utils/languages_file.json", "w", encoding="utf-8") as file:
            json.dump(self.languages, file, ensure_ascii=False, indent=4)
        project.project_text.to_csv(os.path.join(language_source_folder,project.project_name+".csv"),index=False)

        ui.navigate.to("/existing_project")
        ui.notify("Project Saved",close_button="Ok")


    def remove_project(self):
        """
        Remove the project from the languages file
        """

        removed=False
        if self.project_name != None:
            source_path=os.path.join(niv_louie_app_data,"languages","source",self.project_name+".csv")
            if os.path.exists(source_path):
                os.remove(source_path)
            filtered_path=os.path.join(niv_louie_app_data,"languages","filtered_"+self.project_name+".csv")
            if os.path.exists(filtered_path):
                os.remove(filtered_path)
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
        self.project_character_column=current_language["char_column"]
        self.project_unicode_column=current_language["unicode_column"]
        self.project_type_column=current_language["type_column"]
        self.project_braille_column=current_language["braille_column"]
        self.project_language_code=current_language["language_code"]
        self.project_display_name=current_language["display_name"]
        if "language_system_code" in current_language:
            self.project_language_system_code=current_language["language_system_code"]
        if "index_name" in current_language:
            self.project_index_name=current_language["index_name"]
        if "supported_braille_languages" in current_language:
            self.project_supported_braille_languages=current_language["supported_braille_languages"]
        self.project_language_information=current_language["language_information"]
        self.project_contributors=current_language["contributors"]
        if "included_braille_tables" in current_language:
            self.project_included_braille_tables=current_language["included_braille_tables"]
        if "test_display_type" in current_language:
            self.project_test_display_type=current_language["test_display_type"]
        if "replace" in current_language:
            self.project_replace=current_language["replace"]


project = Project()


def convert_text_to_braille(name,content):
    """
    This     function creates the braille tests for Lib Louis

    Parameters:
    (int): The index of the language that the user has chosen

    """

    #The language files are read in to pandas
    language_file_list=[]
    for selected_language in project.document_projects_to_use:
        language_file_list.append({"name":selected_language, "file":pd.read_csv(os.path.join(niv_louie_app_data,"languages","filtered_"+selected_language+".csv"),encoding="utf-8")})
    braille_content=""
    #This loop goes through each row in the content
    for row in content.text.split("\n"):
        new_braille_content=row
        #This checks if the test contains any numbers
        if any(char.isdigit() for char in new_braille_content):
            new_text=""
            previous_was_number=False 
            #This loop goes through each character in the text
            for index,char in enumerate(new_braille_content):
                #This checks if the character is a number
                if char.isdigit() and previous_was_number==False:
                    #This adds a number sign to the character
                    new_text+="⠼"+char
                    previous_was_number=True
                else:
                    #This adds the character to the new text
                    new_text+=char
                    previous_was_number=False
            #This replaces the text with the new text
            new_braille_content=new_text
        for current_language in language_file_list:
            project.set_project_name(current_language["name"])
            project.set_all_fields()
            language_file=current_language["file"]
            #This loop goes through each character in the text
            for index,language_row in language_file.iterrows():
                if language_row[project.project_character_column] in new_braille_content and language_row[project.project_braille_column] != "nan":
                    new_braille_content=new_braille_content.replace(language_row[project.project_character_column],language_row[project. project_braille_column])
    #This loop goes through each character in the text and uses the braille test object to convert the text to braille
        for char in new_braille_content:
            if char in braille_converter_object:
                new_braille_content=new_braille_content.replace(char,braille_converter_object[char])
    #Checks if the test contains any non braille characters
        for char in new_braille_content:
            if char not in braille_numbers_object:
                warnings.warn("This test contains a character that is not in the braille object. This may be a mistake in your test. Character: "+char)
        #This adds the new braille content to the braille content
        braille_content+=new_braille_content+"\n"
    return braille_content
