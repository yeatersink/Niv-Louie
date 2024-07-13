from nicegui import app, events, ui
from utils.project import languages, project


app.native.window_args["resizable"]=True
app.native.start_args["debug"]=True

@ui.page("/existing_project")
def existing_project():
    global languages
    language_list=[]
    for language in languages:
        language_list.append(language["name"])

    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Get Access to an Existing Language")
    ui.select(options=sorted(language_list),label="Select a Language",with_input=True,on_change=project.update_project_name)
    ui.select(options=project.actions.keys(),label="What do you want to do with this Project?",multiple=True,on_change=project.update_user_actions)
    with ui.dialog() as confirm_remove_project_dialog, ui.card():
        ui.label("Are you sure you want to completely remove this project?")
        ui.button("Cancel",on_click=confirm_remove_project_dialog.close)

        def remove_and_close():
            project.remove_project()
            confirm_remove_project_dialog.close

        ui.button("Delete",on_click=remove_and_close())
    with ui.button("More Options"):
        with ui.menu() as more_options_menu:
            ui.menu_item("Edit Project")
            ui.menu_item("Completely Remove Project",on_click=confirm_remove_project_dialog.open)
    ui.button("Next",on_click=project.perform_actions)


@ui.page("/create_project")
def create_project():
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Create New Project")
    ui.label("Upload your Spreadsheet.")
    ui.upload(on_upload=project.handle_file_upload,auto_upload=True)
    ui.link("Continue",project_information)


@ui.page("/project_information")
def project_information():
    global project_name, project_text, project_name_column, project_character_column, project_unicode_column, project_type_column, project_braille_column
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Project Information")            
    if project.project_name is not None:
        ui.input(label="What is the name of your project?",value=project.project_name,on_change=project.update_project_name)
    if project.project_text is not None:
        ui.select(label="What column contains the name of the character?",options=project.project_text.columns.tolist(),value=project.project_name_column,on_change=project.update_project_name_column)
        ui.select(label="What column contains the character?",options=project.project_text.columns.tolist(),value=project.project_character_column,on_change=project.update_project_character_column)
        ui.select(label="What column contains the Unicode value of the character?",options=project.project_text.columns.tolist(),value=project.project_unicode_column,on_change=project.update_project_unicode_column)
        ui.select(label="What column contains the Type of the character?",options=project.project_text.columns.tolist(),value=project.project_type_column,on_change=project.update_project_type_column)
        ui.select(label="What column contains the Braille character?",options=project.project_text.columns.tolist(),value=project.project_braille_column,on_change=project.update_project_braille_column)
    ui.button("Save Project",on_click=project.save_project)


ui.label("What do you want to do?")
ui.link("Create a New Project",create_project)
ui.link("Access Existing Project",existing_project)
ui.link("Create Braille document from Existing Project.")
ui.button("Exit",on_click=app.stop)


ui.run(native=True,window_size=(400,300),fullscreen=False,title="Language Project Manager")
