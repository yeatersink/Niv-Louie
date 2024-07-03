from nicegui import app, events, ui
import pandas as pd
import io
import json

project_name=None
project_text= None
project_name_column=None
project_character_column=None
project_unicode_column=None
project_type_column=None
project_braille_column=None

app.native.window_args["resizable"]=False
app.native.start_args["debug"]=True

# Function to load languages from JSON file
def load_languages():
    try:
        with open("utils/languages_file.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

#Loads the languages from the JSON file
languages = load_languages()

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
    ui.select(options=["Add Characters to NVDA","Download Files for NVDA","Write Table for Lib Louis","Write Test for Lib Louis"],label="What do you want to do with this Project?",multiple=True)
    with ui.button("More Options"):
        with ui.menu() as more_options_menu:
            ui.menu_item("Completely Remove Project")
    ui.menu_item("Edit Project")
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
        ui.input(label="What is the name of your project?",value=project_name,on_change=update_project_name)
    if project_text is not None:
        ui.select(label="What column contains the name of the character?",options=project_text.columns.tolist(),value=project_name_column)
        ui.select(label="What column contains the character?",options=project_text.columns.tolist(),value=project_character_column)
        ui.select(label="What column contains the Unicode hex value of the character?",options=project_text.columns.tolist(),value=project_unicode_column)
        ui.select(label="What column contains the Type of the character?",options=project_text.columns.tolist(),value=project_type_column)
        ui.select(label="What column contains the Braille character?",options=project_text.columns.tolist(),value=project_braille_column)
    ui.button("Save Project",on_click=save_project)

def update_project_name(e:events.ValueChangeEventArguments):
    global project_name
    project_name=e.value


def save_project():
    global project_name, project_text, project_name_column, project_character_column, project_unicode_column, project_type_column, project_braille_column, languages
    project_object={"name":project_name,"name_column":project_name_column,"char_column":project_character_column,"braille_column":project_braille_column,"type_column":project_type_column,"unicode_column":project_unicode_column}
    languages.append(project_object)
    with open("utils/languages_file.json", "w", encoding="utf-8") as file:
        json.dump(languages, file, ensure_ascii=False, indent=4)
    project_text.to_csv("languages/source/"+project_name+".csv",index=False)
    ui.navigate.to("/existing_project")


ui.label("What do you want to do?")
ui.link("Create a New Project",create_project)
ui.link("Get Access to Existing Project",existing_project)

ui.run(native=True,window_size=(400,300),fullscreen=False,title="example")
