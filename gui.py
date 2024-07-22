from nicegui import app, events, ui
from utils.project import project
from utils.project_extention import extention
from utils.project_utils import actions, actions_name_list, user_actions, perform_user_actions, save_and_create_csv, update_user_actions
#the create_braille_table function is used to create the braille table for lib louis
#the create_braille_tests function is used to create the braille tests for lib louis
#the get_braille_from_text_in_source function is used to convert the text characters to braille characters in the source language file
from utils.braille import create_braille_table, create_braille_tests, get_braille_from_text_in_source
#The create_filtered_csv function is used to create the filtered csv file
#The regenerate_characters_using_hex function is used to regenerate the characters in the language source file
from utils.csv import create_filtered_csv, regenerate_characters_using_hex
#The add_characters_to_nvda function is used to add the symbols to the nvda symbols file
#The generate_locale_file function is used to generate the locale file for nvda
#The generate_character_set function is used to generate the character set for nvda
from utils.nvda import add_characters_to_nvda,generate_locale_file, generate_character_set, create_nvda_extention


app.native.window_args["resizable"]=True
app.native.start_args["debug"]=True

@ui.page("/existing_project")
def existing_project():
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Manage a project")
    ui.button("Create a New Project",on_click=lambda:ui.navigate.to("/create_project"))
    language_select = ui.select(options=sorted(project.languages_list),label="Select a Project",with_input=True,on_change=project.update_project_name)
    ui.button("Edit Project",on_click=lambda:ui.navigate.to("/edit_project_information"))
    with ui.dialog() as dialog,ui.card():
        ui.label("Are you Sure you want to Permenantly Remove this Project?")
        ui.button("Cancel",on_click=dialog.close)
        def confirm_delete():
            project.remove_project()
            language_select.options = sorted(project.languages_list)
            dialog.close()
        ui.button("Yes, Delete",on_click=confirm_delete)
    ui.button("Remove Project",on_click=dialog.open)
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


@ui.page("/edit_project_information")
def edit_project_information():
    regenerate_characters=False
    generate_braille=False
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Edit Project Information")            
    if project.project_name is not None:
        project.set_all_fields()
        project.load_language_source()
        ui.input(label="What is the name of your project?",value=project.project_name,on_change=project.update_project_name)
        ui.input("What is the language ISO code?",value=project.project_language_code,on_change=project.update_project_language_code)
        ui.input("What is the language system?",value=project.project_language_system_code,on_change=project.update_project_language_system_code)
    if project.project_text is not None:
        ui.select(label="What column contains the name of the character?",options=project.project_text.columns.tolist(),value=project.project_name_column,on_change=project.update_project_name_column)
        ui.select(label="What column contains the character?",options=project.project_text.columns.tolist(),value=project.project_character_column,on_change=project.update_project_character_column)
        ui.select(label="What column contains the Unicode value of the character?",options=project.project_text.columns.tolist(),value=project.project_unicode_column,on_change=project.update_project_unicode_column)
        ui.select(label="What column contains the Type of the character?",options=project.project_text.columns.tolist(),value=project.project_type_column,on_change=project.update_project_type_column)
        ui.select(label="What column contains the Braille character?",options=project.project_text.columns.tolist(),value=project.project_braille_column,on_change=project.update_project_braille_column)
        ui.checkbox(text="Generate Characters using Unicode Column",value=regenerate_characters)
        ui.checkbox(text="Generate Braille Characters for Braille Column",value=generate_braille)
    ui.button("Save Changes",on_click=lambda:save_project_edits(regenerate_characters,generate_braille))


def save_project_edits(regenerate_characters,generate_braille):
    if regenerate_characters==True:
        regenerate_characters_using_hex()
    if generate_braille==True:
        get_braille_from_text_in_source()
    save_and_create_csv()


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
    ui.select(options=sorted(project.languages_list),label="What Projects do you want to include in this extention?",multiple=True,on_change=extention.update_extention_included_projects)
    ui.button("Save Extention.",on_click=extention.save_extention)


@ui.page("/liblouis_table_builder")
def liblouis_table_builder():
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Table Builder")
    ui.select(label="What project do you want to use?",options=sorted(project.languages_list),with_input=True,on_change=project.update_project_name)
    ui.button("Generate table for Lib Louis",on_click=create_braille_table)
    ui.button("Generate Test for Lib Louis",on_click=lambda: ui.navigate.to("/create_test"))


@ui.page("/create_test")
def create_test():
    ui.button("Go Back",on_click=ui.navigate.back)
    ui.label("Create Test for Lib Louie.")
    ui.upload(on_upload=project.handle_test_upload,auto_upload=True)
    ui.button("Generate YAML Test for Lib Louis",on_click=create_braille_tests)


@ui.page("/braille_document_builder")
def braille_document_builder():
    ui.label("Braille Document Builder")
    ui.select(label="What project do you want to use?",options=sorted(project.languages_list),with_input=True,on_change=project.update_project_name)
    ui.upload(on_upload=project.handle_document_upload,auto_upload=True)


ui.label("Welcome to Niv Louie. What would you like to work on today?")
ui.link("Project Manager",existing_project)
ui.link("NVDA Extention Builder",nvda_extention_builder)
ui.link("Lib Louie Table/ Test Builder",liblouis_table_builder)
ui.link("Braille document Builder.",braille_document_builder)
ui.button("Exit",on_click=app.stop)


ui.run(native=True,window_size=(400,300),fullscreen=False,title="Language Project Manager")
