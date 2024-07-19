from nicegui import app, events, ui
from utils.project import project
from utils.project_extention import extention
from utils.project_utils import actions, actions_name_list, user_actions, perform_user_actions, save_and_create_csv, update_user_actions
from utils.nvda import create_nvda_extention


app.native.window_args["resizable"]=True
app.native.start_args["debug"]=True

@ui.page("/existing_project")
def existing_project():
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Get Access to an Existing Language")
    language_select = ui.select(options=sorted(project.languages_list),label="Select a Language",with_input=True,on_change=project.update_project_name)
    ui.select(options=actions_name_list,label="What do you want to do with this Project?",multiple=True,on_change=update_user_actions)
    with ui.dialog() as confirm_remove_project_dialog, ui.card():
        ui.label("Are you sure you want to completely remove this project?")
        ui.button("Cancel",on_click=confirm_remove_project_dialog.close)

        def remove_and_close():
            project.remove_project()
            language_select.options = sorted(project.languages_list)
            confirm_remove_project_dialog.close()


        ui.button("Delete",on_click=remove_and_close)
    with ui.button("More Options"):
        with ui.menu() as more_options_menu:
            ui.menu_item("Edit Project")
            ui.menu_item("Completely Remove Project",on_click=confirm_remove_project_dialog.open)
    ui.button("Next",on_click=perform_user_actions)
    ui.button("Home",on_click=lambda: ui.navigate.to("/"))


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
        ui.input("What is the language ISO code?",value=project.project_language_code,on_change=project.update_project_language_code)
        ui.input("What is the language system?",value=project.project_language_system_code,on_change=project.update_project_language_system_code)
    if project.project_text is not None:
        ui.select(label="What column contains the name of the character?",options=project.project_text.columns.tolist(),value=project.project_name_column,on_change=project.update_project_name_column)
        ui.select(label="What column contains the character?",options=project.project_text.columns.tolist(),value=project.project_character_column,on_change=project.update_project_character_column)
        ui.select(label="What column contains the Unicode value of the character?",options=project.project_text.columns.tolist(),value=project.project_unicode_column,on_change=project.update_project_unicode_column)
        ui.select(label="What column contains the Type of the character?",options=project.project_text.columns.tolist(),value=project.project_type_column,on_change=project.update_project_type_column)
        ui.select(label="What column contains the Braille character?",options=project.project_text.columns.tolist(),value=project.project_braille_column,on_change=project.update_project_braille_column)
    ui.button("Save Project",on_click=save_and_create_csv)


@ui.page("/nvda_extention_builder")
def nvda_extention_builder():
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Extention Builder")
    ui.button("Create New Extention",on_click=lambda: ui.navigate.to("/create_extention"))
    ui.select(label="Select an Extention.",options=sorted(extention.extentions_list),on_change=extention.update_extention_name)
    ui.button("Generate extention",on_click=create_nvda_extention)
    ui.button("Next",on_click=perform_user_actions)
    ui.button("Home",on_click=lambda: ui.navigate.to("/"))


@ui.page("/create_extention")
def create_extention():
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Create Extention")
    ui.input(label="What is the name of your Project?",on_change=extention.update_extention_name)
    ui.input(label="Please briefly describe your Project?",on_change=extention.update_extention_summary)
    ui.input(label="Please provide a more detailed description of your Project?",on_change=extention.update_extention_description)
    ui.input(label="Who are the Authors of your Project?",on_change=extention.update_extention_author)
    ui.input(label="How many versions have you created of this Project?",on_change=extention.update_extention_version)
    ui.input(label="What is the minimum version of NVDA does this Extention support?",on_change=extention.update_extention_minimum_version)
    ui.input(label="What is the most recent version of NVDA that you have tested this Extention on?",on_change=extention.update_extention_last_tested_version)
    ui.input(label="What Language/ Locale does this Extention support ?",on_change=extention.update_extention_locale)
    ui.select(options=sorted(project.languages_list),label="What Projects do you want to include in this extention?",with_input=True,multiple=True,on_change=extention.update_extention_included_projects)
    ui.button("Save Extention.",on_click=extention.save_extention)


ui.label("What do you want to do?")
ui.link("Create a New Project",create_project)
ui.link("Project Manager",existing_project)
ui.link("NVDA Extention Builder",nvda_extention_builder)
ui.link("Create Braille document from Existing Project.")
ui.button("Exit",on_click=app.stop)


ui.run(native=True,window_size=(400,300),fullscreen=False,title="Language Project Manager")
