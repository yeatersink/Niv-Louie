from nicegui import app, events, ui
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
from utils.project import project


user_actions=[]

actions={"Add Characters to NVDA":{"action":add_characters_to_nvda,"notification":"Added characters to NVDA!"},"create extention for NVDA":{"action":create_nvda_extention,"notification":"Extention created for NVDA !"},"Write Table for Lib Louis":{"action":create_braille_table,"notification":"Table written for Lib Louis!"},"Write Test for Lib Louis":{"action":create_braille_tests,"notification":"Test written for Lib Louis!"}}

actions_name_list=[key for key in actions]

def perform_user_actions():
    project.set_all_fields()
    global user_actions
    for action in user_actions:
        actions[action]["action"]()
        ui.notify(actions[action]["notification"])

def update_user_actions(e:events.ValueChangeEventArguments):
    global user_actions
    user_actions=e.value


def save_and_create_csv():
    project.save_project()
    create_filtered_csv()