import os
from pathlib import Path
import warnings
#Pandas is used for reading the   csv files
import pandas as pd
#json is used for reading the json files
import json
from utils.project import project
from nicegui import ui


appdata_dir=os.getenv("LOCALAPPDATA")
niv_louie_app_data=os.path.join(appdata_dir,"Niv_Louie")
os.makedirs(niv_louie_app_data,exist_ok=True)


def create_braille_table():
    print("creating table for lib louis")
    #The language file is read in to pandas
    braille=pd.read_csv(os.path.join(niv_louie_app_data,"languages","filtered_"+project.project_name+".csv"))
    braille_folder=os.path.join(niv_louie_app_data,"braille")
    if os.path.exists(braille_folder) == False:
        os.makedirs(braille_folder)

    #The braille table is opened in write mode to create the table
    braille_table=open(os.path.join(braille_folder,project.project_language_code+".utb"),"w",encoding="utf-8")
    #The braille column is converted to numbers
    braille[project.project_braille_column]=braille[project.project_braille_column].apply(braille_to_numbers)

    #The braille table is written to with the information for the language that is required for lib louis
    braille_table.write("""
# liblouis: """+project.project_name+"""
#
""")

    if project.project_display_name!=None:
        braille_table.write("#-display-name: "+project.project_display_name+"\n")
    else:
        braille_table.write("#-display-name: "+project.project_name+" uncontracted\n")
            
    if project.project_index_name!=None:
        braille_table.write("#-index-name: "+project.project_index_name+"\n")
    else:
                            braille_table.write("#-index-name: "+project.project_name+" uncontracted\n")
                            
    #Checks if the supported_braille_languages property exists on the language
    if project.project_supported_braille_languages!=None:
        for language in project.project_supported_braille_languages:
            braille_table.write("#+language: "+language+"\n")
    else:
        braille_table.write("#+language: "+project.project_language_code+"\n")
    braille_table.write("""#+type:literary
#+contraction:no
#+system:"""+project.project_language_system_code+"""
#+dots:6

#-license: lgpl-2.1

# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this file; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# liblouis  comes with ABSOLUTELY NO WARRANTY.

"""+project.project_language_information+project.project_contributors)
    braille=braille.sort_values(["Type",project.project_character_column])
    previous_char=""
    #This loop goes through each row in the braille file and writes the braille code and the number to the braille table
    for index, row in braille.iterrows():
        if row["Type"] != previous_char:
            braille_table.write("\n# "+str(row["Type"])+" op code characters\n")
            previous_char=row["Type"]
        if len(row[project.project_braille_column]) > 0:
            new_line=""
            if str(row[project.project_character_column]).isspace():
                new_line=row["Type"]+" \\s "+str(row[project.project_braille_column])+"  # space\n"
            else:
                new_line=row["Type"]+" "+str(row[project.project_character_column])+" "+str(row[project.project_braille_column])+"  # "+str(row[project.project_name_column])+"\n"
            braille_table.write(new_line)
        else:
            warnings.warn("this line was missing it's braille. This may be a mistake in your table. Character: "+row[project.project_character_column])

    if project.project_included_braille_tables!=None:
        braille_table.write("\n# Include additional braille tables\n")
        for table in project.project_included_braille_tables:
            braille_table.write("include "+table+"\n")
    #The braille table is closed to prevent memory leaks
    braille_table.close()
    ui.notify("Braille Table for Lib Louis has been Generated. ")
    ui.download(os.path.join(braille_folder,project.project_language_code+".utb"))


#The braille_converter.json file is opened and read in to the braille_object variable
braille_file=open("utils/braille_converter.json",encoding="utf8")
braille_object=json.load(braille_file)

#The braille_test_converter.json file is opened and read in to the braille_test_object variable
braille_test_file=open("utils/braille_test_converter.json",encoding="utf8")
braille_test_object=json.load(braille_test_file)

#The braille_numbers.json file is opened and read in to the braille_numbers_object variable
braille_numbers_file=open("utils/braille_to_numbers.json",encoding="utf8")
braille_numbers_object=json.load(braille_numbers_file)

def get_braille_from_text(text):
    """
    This function converts text characters to braille characters

    Parameters:
    text (str): The text that is to be converted to braille

    Returns:
    str: The braille code for the text

    """

    #The braille variable is initialized as an empty string
    braille=""
    print(text)
    if str(text) != "nan":
        #The text is checked to see if it contains any numbers
        if any(char.isdigit() for char in text):
            new_text=""
            #The text is looped
            for index,char in enumerate(text):
                #checks if the character is a number
                if char.isdigit():
                    #adds a number sign to the character
                    new_text+=""+char
                else:
                    #adds the character to the new text
                    new_text+=char
            #the text is replaced with the new text
            text=new_text
        #The text is checked to see if it contains any special characters
        if "[q~^]"*3 in text:
            text=text.replace("[q~^]"*3,"^#3")
        if "[q~^]"*2 in text:
            text=text.replace("[q~^]"*2,"^#2")
        if "[q~" in text:
            text=text.replace("[q~","")
        if "]" in text:
            text=text.replace("]","")
        print(text)

        #The text is looped through
        for char in text:
            #checks if the character is in the braille numbers object
            if char not in braille_numbers_object:
                #adds the new braille character to the braille variable
                braille+=braille_object[char]
            else:
                #adds the character to the braille variable
                braille+=char
        #returns the braille variable
        return braille
    else:
        return "nan"

def braille_to_numbers(text):
    """
    This function converts braille characters to numbers
    
    Parameters:
    text (str): The braille character that is to be converted
    
    Returns:
    str: The number that corresponds to the braille character

    """

    braille=""
    if str(text) != "nan":
        print(text)
        #loops through each character in the text
        for char in text:
            #converts the braille character to a number
            braille+=braille_numbers_object[char.lower()]+"-"
        #removes the last - from the braille variable
        if braille[-1]=="-":
            braille=braille[:-1]
        #returns the braille variable
        return braille
    else:
        return ""


def create_braille_tests(selected_project_list ):
    """
    This function creates the braille tests for Lib Louis
    
    Parameters:
     selected_project_list (list): The list of projects that the user has selected

    """
    #The language file is read in to pandas
    language_file=pd.read_csv(os.path.join(niv_louie_app_data,"languages","filtered_"+project.project_name+".csv"),encoding="utf-8")
    #The language file is concatenated with the other language files that are included in the project
    if len(selected_project_list)>1:
        for project_name in selected_project_list[1:]:
            print(project_name)
            temp_language_file=pd.read_csv(os.path.join(niv_louie_app_data,"languages","filtered_"+project_name+".csv"),encoding="utf-8")
            language_file=pd.concat([language_file,temp_language_file])
    if project.project_included_braille_tables:
        for table in project.project_included_braille_tables:
            for language in project.languages:
                if table.split(".")[0] == language["language_code"]:
                    print("found language "+language["language_code"])
                    temp_language_file=pd.read_csv(os.path.join(niv_louie_app_data,"languages","filtered_"+language["name"]+".csv"),encoding="utf-8")
                    language_file=pd.concat([language_file,temp_language_file])
    language_file=language_file.sort_values(by=["Hex"],key=lambda x:x.str.len(),ascending=False)
    language_file.to_csv("temp.csv",index=False)
    #The test csv file is read in to pandas
    test_csv=pd.read_csv("braille_tests/"+project.project_language_code+".csv",encoding="utf-8")
    #The test yaml file is opened in write mode to create the test
    test_yaml=open("braille_tests/"+project.project_language_code+".yaml","w",encoding="utf-8")
    #The test yaml file is written to with the information that is required for the test for Lib Louis
    test_yaml.write("""
# Yaml Test For """+project.project_name+"""

# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.

""")
    #Checks if the test_display_type property exists on the language
    if not project.project_test_display_type==None:
        test_yaml.write("display: "+project.project_test_display_type+"\n")
    else:
        test_yaml.write("display: unicode.dis\n")
        
    test_yaml.write("""table:
  language: """+project.project_language_code+"""
  __assert-match: """+project.project_language_code+""".utb
flags: { testmode: forward }
tests:
""")
    #This loop goes through each row in the test csv file
    for index,row in test_csv.iterrows():
        braille_test=row["Text"]
        #This checks if the test contains any numbers
        if any(char.isdigit() for char in braille_test):
            new_text=""
            previous_was_number=False 
            #This loop goes through each character in the text
            for index,char in enumerate(braille_test):
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
            braille_test=new_text
        #This loop goes through each character in the text
        for index,language_row in language_file.iterrows():
            if language_row[project.project_character_column] in braille_test and str(language_row[project.project_braille_column]) != "nan":
                braille_test=braille_test.replace(language_row[project.project_character_column],language_row[project. project_braille_column])
        #This loop goes through each character in the text and uses the braille test object to convert the text to braille
        for char in braille_test:
            if char in braille_test_object:
                braille_test=braille_test.replace(char,braille_test_object[char])
        #Checks if the test contains any non braille characters
        for char in braille_test:
            if char not in braille_numbers_object:
                warnings.warn("This test contains a character that is not in the braille object. This may be a mistake in your test. Character: "+char)
        #writes the braille test to the test yaml file
        test_yaml.write('  - ["'+row["Text"]+'", "'+braille_test+'"]\n')
    #The test yaml file is closed to prevent memory leaks
    test_yaml.close()
    print("done creating braille tests")
    ui.notify("Braille Test for Lib Louis has been Generateds. ")
    ui.download("braille_tests/"+project.project_language_code+".yaml")


def get_braille_from_text_in_source():
    """
    This function converts the text characters to braille characters in the source language file
    
    Parameters:
     (int): The index of the language that the user has chosen
    
    """
    print ("converting text to braille")
    #the language source file is read in to pandas
    language_file=pd.read_csv("languages/source/"+project.project_name+".csv")
    #selects the braille column
    braille_column=language_file[project.project_braille_column]
    #applies the get_braille function to the braille column to convert the text to braille
    new_braille_column=braille_column.apply(get_braille_from_text)
    #the braille column is replaced with the new braille column
    language_file["Braille"]=new_braille_column
    #the file is saved to the source folder
    language_file.to_csv("languages/source/"+project.project_name+".csv",index=False)
    print("done converting text to braille")
