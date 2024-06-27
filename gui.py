from nicegui import app, events, ui
from utils.languages_file import languages
import pandas as pd

project_name=None
project_text= None


language_list=[]
for language in languages:
    language_list.append(language["name"])

app.native.window_args["resizable"]=False
app.native.start_args["debug"]=True

@ui.page("/existing_project")
def existing_project():
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
    ui.upload(on_upload=handle_file_upload)
    ui.link("Continue",project_information)


def handle_file_upload(e:events.UploadEventArguments):
    global project_name, project_text
    project_name=e.name
    project_text=pd.DataFrame(e.content.read().decode("utf-8").splitlines())

@ui.page("/project_information")
def project_information():
    global project_name, project_text
    ui.label("Project Information")            
    if project_name is not None:
        ui.input(label="What is the language code for your language?",value=project_name)
    if project_text is not None:
        ui.select(label="What column contains the name of the character?",options=project_text.columns.tolist())

ui.label("What do you want to do?")
ui.link("Create a New Project",create_project)
ui.link("Get Access to Existing Project",existing_project)

ui.run(native=True,window_size=(400,300),fullscreen=False,title="example")
