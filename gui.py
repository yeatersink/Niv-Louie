from nicegui import app, events, ui
from utils.languages_file import languages
import pandas as pd
import io

project_name=None
project_text= None
project_name_column=None
project_character_column=None
project_unicode_column=None
project_type_column=None
project_braille_column=None

app.native.window_args["resizable"]=False
app.native.start_args["debug"]=True

@ui.page("/existing_project")
def existing_project():
    global languages
    language_list=[]
    print(languages)
    for language in languages:
        language_list.append(language["name"])
    print(language_list)
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Get Access to an Existing Language")
    ui.select(options=language_list,label="Select a Language",with_input=True)
    ui.checkbox("Add Language to NVDA")
    ui.checkbox("Download File to add to NVDA")
    ui.checkbox("Download Language Spreadsheet")
    ui.button("Next")


@ui.page("/create_project")
def create_project():
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Create New Project")
    ui.label("Upload your Spreadsheet.")
    ui.upload(on_upload=handle_file_upload,auto_upload=True)
    ui.link("Continue",project_information)


def handle_file_upload(e:events.UploadEventArguments):
    global project_name, project_text
    project_name=e.name.split(".")[0]
    content_as_file = io.StringIO(e.content.read().decode("utf-8"))
    project_text=pd.read_csv(content_as_file)


@ui.page("/project_information")
def project_information():
    global project_name, project_text
    ui.label("Project Information")            
    if project_name is not None:
        ui.input(label="What is the name of your project?",value=project_name)
    if project_text is not None:
        ui.select(label="What column contains the name of the character?",options=project_text.columns.tolist(),value=project_name_column)
        ui.select(label="What column contains the Unicode character ?",options=project_text.columns.tolist(),value=project_character_column)
        ui.select(label="What column contains the Unicode value of the character?",options=project_text.columns.tolist(),value=project_unicode_column)
        ui.select(label="What column contains the Type of the character?",options=project_text.columns.tolist(),value=project_type_column)
        ui.select(label="What column contains the Braille character?",options=project_text.columns.tolist(),value=project_braille_column)
    ui.button("Save Project",on_click=save_project)


def save_project():
    global project_name, project_text, project_name_column, project_character_column, project_unicode_column, project_type_column, project_braille_column, languages
    project_object={"name":project_name,"name_column":project_name_column,"char_column":project_character_column,"braille_column":project_braille_column,"type_column":project_type_column,"unicode_column":project_unicode_column}
    languages.append(project_object)
    ui.navigate.to("/existing_project")


ui.label("What do you want to do?")
ui.link("Create a New Project",create_project)
ui.link("Get Access to Existing Project",existing_project)

ui.run(native=True,window_size=(400,300),fullscreen=False,title="example")
