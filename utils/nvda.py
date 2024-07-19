#pathlib is used for creating folders
import pathlib
#Pandas is used for reading the   csv files
import pandas as pd
#ui is used for displaying notifications
from nicegui import ui
from utils.project import project
from utils.project_extention import extention


def add_characters_to_nvda():
    """

        This function adds the characters from the language file to the NVDA symbols file

        Args:
            : The index of the language in the languages variable

    """
    print("adding symbols to nvda for",project.project_name)
    #The language file is read in to pandas
    language_file=pd.read_csv("languages/filtered_"+project.project_name+".csv")
    #The nvda symbols file is opened in append mode to add the symbols to the end of the file
    nvda_symbols_file=open("C:/Program Files (x86)/NVDA/locale/en/symbols.dic","a+",encoding="utf8")
    #a comment is added to the file to show where the symbols for the language start
    nvda_symbols_file.write("\n#"+project.project_name+"\n")
    #this loop goes through each row in the language file and adds the character and name to the nvda symbols file
    for index,row in language_file.iterrows():
        new_line=str(row[project.project_character_colum])+"\t"+str(row["Name"])+"\tmost\talways\n"
        nvda_symbols_file.write(new_line)
    #a comment is added to the file to show where the symbols for the language end
    nvda_symbols_file.write("#End "+project.project_name+"\n\n")
    #the file is closed to prevent memory leaks
    nvda_symbols_file.close()
    print("symbols added to nvda for",project.project_name)


def generate_locale_file():
    """

        This function generates a locale file for the language

        Args:
            : The index of the language in the languages variable

    """
    print("generating nvda  locale file for for",project.project_name)
    #The language file is read in to pandas
    language_file=pd.read_csv("languages/filtered_"+project.project_name+".csv")
    new_folder = pathlib.Path("nvda/",project.project_language_code)
    new_folder.mkdir(parents=True,exist_ok=True)
    #The locale characters file is created
    nvda_locale_file=open("nvda/"+project.project_language_code+"/characterDescriptions.dic","w",encoding="utf8")
    nvda_locale_file.write("""#"""+project.project_name+""" characterDescriptions.dic
#A part of NonVisual Desktop Access (NVDA)
#URL: http://www.nvda-project.org/
#Copyright (c) 2024Matthew Yeater and Paul Geoghegan.
#This file is covered by the GNU General Public License.
\n""")
    language_file[project.project_name_column]=language_file[project.project_name_column].apply(format_names)
    #this loop goes through each row in the language file which has the type letter and adds the character and name to the nvda symbols file
    for index,row in language_file.loc[(language_file["Type"]=="letter")].sort_values(by=[project.project_name_column]).iterrows():
        new_line=str(row[project.project_character_column])+"\t"+str(row["Name"])+"\n"
        nvda_locale_file.write(new_line)
    #the file is closed to prevent memory leaks
    nvda_locale_file.close()
    #Checks if there are any non-letter characters in the language file
    if not language_file.loc[(language_file["Type"]!="letter")].empty:
        #The locale symbols file is created
        nvda_locale_file=open("nvda/"+project.project_language_code+"/symbols.dic","w",encoding="utf8")
        nvda_locale_file.write("""#"""+project.project_name+""" symbols.dic
#A part of NonVisual Desktop Access (NVDA)
#URL: http://www.nvda-project.org/
#Copyright (c) 2024Matthew Yeater and Paul Geoghegan.
#This file is covered by the GNU General Public License.
\n""")    
        #this loop goes through each row in the language file which does not have the type letter and adds the character and name to the nvda symbols file
        for index,row in language_file.loc[(language_file["Type"]!="letter")].sort_values(by=[project.project_name_column]).iterrows():
            new_line=str(row[project.project_character_column])+"\t"+str(row["Name"])+"\tmost\talways\n"
            nvda_locale_file.write(new_line)
        #the file is closed to prevent memory leaks
        nvda_locale_file.close()
    print("Generated Locale files for NVDA for",project.project_name)


def create_nvda_extention():
    """
        This function creates a new extention for NVDA
    """
    print("Creating Extention for NVDA")
    extention.set_fields()
    new_folder = pathlib.Path("nvda_extentions/",extention.extention_name+".nvda-addon")
    new_folder.mkdir(parents=True,exist_ok=True)
    new_locale_folder=pathlib.Path("nvda_extentions/"+extention.extention_name+".nvda-addon/locale/",extention.extention_locale)
    new_locale_folder.mkdir(parents=True,exist_ok=True)
    manifest_file=open("nvda_extentions/"+extention.extention_name+".nvda-addon/manifest.ini","w",encoding="utf-8")
    manifest_file.write("""name = """+extention.extention_name+"""""""""
summary = \""""+extention.extention_summary+"""\"
description = \""""+extention.extention_description+"""\"
author = \""""+extention.extention_author+"""\"
version = """+extention.extention_version+"""
minimumNVDAVersion = """+extention.extention_minimum_version+"""
lastTestedNVDAVersion = """+extention.extention_last_tested_version+"""

[symbolDictionaries]
""")
    for language in extention.extention_included_projects:
        project.set_project_name(language)
        project.set_all_fields()
        manifest_file.write("[["+project.project_language_code+"]]\n")
        manifest_file.write("displayName = "+project.project_display_name+"\n")
        manifest_file.write("mandatory = false\n")
        add_characters_to_nvda_extention()
    manifest_file.close()
    ui.notify("Extention Generated!")


def add_characters_to_nvda_extention():
    """
        This function adds the characters from the language file to the NVDA extention
    """
    print("generating nvda  Character Set for for",project.project_name)
    #The language file is read in to pandas
    language_file=pd.read_csv("languages/filtered_"+project.project_name+".csv")
    #The character Set  file is created
    nvda_character_set_file=open("nvda_extentions/"+extention.extention_name+".nvda-addon/locale/"+extention.extention_locale+"/symbols-"+project.project_language_code+".dic","w",encoding="utf-8")
    nvda_character_set_file.write("""#"""+project.project_name+""" symbols.dic
#Copyright (c) 2024Matthew Yeater and Paul Geoghegan.
#This file is covered by the GNU General Public License.
\n""")
    language_file[project.project_name_column]=language_file[project.project_name_column].apply(format_names)
    #this loop goes through each row in the language file
    for index,row in language_file.sort_values(by=[project.project_name_column]).iterrows():
        new_line=str(row[project.project_character_column])+"\t"+str(row["Name"])+"\tmost\talways\n"
        nvda_character_set_file.write(new_line)
    #the file is closed to prevent memory leaks
    nvda_character_set_file.close()
    print("Generated Character Set file for NVDA extention for",project.project_name)


def generate_character_set():
    """
        This function generates a locale file for the language
    """
    print("generating nvda  Character Set for for",project.project_name)
    #The language file is read in to pandas
    language_file=pd.read_csv("languages/filtered_"+project.project_name+".csv")
    new_folder = pathlib.Path("nvda_character_sets/",project.project_language_code)
    new_folder.mkdir(parents=True,exist_ok=True)
    #The character Set  file is created
    nvda_character_set_file=open("nvda_character_sets/"+project.project_language_code+"/symbols.dic","w",encoding="utf8")
    nvda_character_set_file.write("""#"""+project.project_name+""" symbols.dic
#A part of NonVisual Desktop Access (NVDA)
#URL: http://www.nvda-project.org/
#Copyright (c) 2024Matthew Yeater and Paul Geoghegan.
#This file is covered by the GNU General Public License.
\n""")
    language_file[project.project_name_code]=language_file[project.project_name_column].apply(format_names)
    #this loop goes through each row in the language file
    for index,row in language_file.sort_values(by=[project.project_name_column]).iterrows():
        new_line=str(row[project.project_character_column])+"\t"+str(row["Name"])+"\tmost\talways\n"
        nvda_character_set_file.write(new_line)
    #the file is closed to prevent memory leaks
    nvda_character_set_file.close()
    print("Generated Character Set file for NVDA for",project.project_name)


def format_names(name):
    """

    This function removes unwanted characters from the name of the character

    Parameters:
    name (str): The name of the character
    
    Returns:
    str: The name of the character without unwanted characters
    
    """
    #Checks if the name is not a string
    if not isinstance(name,str):
        #If the name is not a string it is converted to a string
        name=str(name)

    return name.strip().lower()
