from nicegui import app, events, ui
from utils.languages_file import languages

project_name=""
project_text=""

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
    #create a dialog
    with ui.dialog() as dialog:
        with ui.card():
            ui.label("Project Information")
            ui.input(label="What is the language code for your language?",)

    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Create New Project")
    ui.label("Upload your Spreadsheet.")
    ui.upload(on_upload=handle_file_upload)
    ui.button("Continue",on_click=dialog.open)


def handle_file_upload(e:events.UploadEventArguments):
    project_name=e.name
    project_text=e.content.read().decode("utf-8")

ui.label("What do you want to do?")
ui.link("Get Access to Existing Project",existing_project)
ui.link("Create a New Project",create_project)

ui.run(native=True,window_size=(400,300),fullscreen=False,title="example")
