import warnings
#Pandas is used for reading the   csv files
import pandas as pd
#json is used for reading the json files
import json
#The languages variable is imported from the languages file
from utils.languages_file import languages

def create_braille_table(language_option):
    print("creating table for lib louis")
    #The language file is read in to pandas
    braille=pd.read_csv("languages/filtered_"+languages[language_option]["name"]+".csv")
    #The braille table is opened in write mode to create the table
    braille_table=open("braille/"+languages[language_option]["language_code"]+".tbl","w",encoding="utf8")
    #The braille column is converted to numbers
    braille[languages[language_option]["braille_column"]]=braille[languages[language_option]["braille_column"]].apply(braille_to_numbers)

    #The braille table is written to with the information for the language that is required for lib louis
    braille_table.write("""
# liblouis: """+languages[language_option]["name"]+""" Grade 1 table
#
# ------------
#-name: """+languages[language_option]["name"]+""" grade 1
#-index-name: """+languages[language_option]["name"]+""" uncontracted
#-display-name: """+languages[language_option]["name"]+""" uncontracted braille as used in the study of """+languages[language_option]["name"]+""" .
#
#+language:"""+languages[language_option]["language_code"]+"""
#+type:literary
#+contraction:no
#+grade:1
#+system:"""+languages[language_option]["language_code"]+"""

# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this file; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# liblouis  comes with ABSOLUTELY NO WARRANTY.

"""+languages[language_option]["language_information"]+languages[language_option]["contributors"])
    #This loop goes through each row in the braille file and writes the braille code and the number to the braille table
    for index, row in braille.iterrows():
        if len(row[languages[language_option]["braille_column"]]) > 0:
            new_line="letter "+str(row[languages[language_option]["char_column"]])+" "+str(row[languages[language_option]["braille_column"]])+"\n"
            braille_table.write(new_line)
        else:
            warnings.warn("this line was missing it's braille. This may be a mistake in your table. Character: "+row[languages[language_option]["char_column"]])

        #The braille table is closed to prevent memory leaks
    braille_table.close()


#The braille_converter.json file is opened and read in to the braille_object variable
braille_file=open("utils/braille_converter.json",encoding="utf8")
braille_object=json.load(braille_file)

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
                braille+=braille_object[char.lower()]
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

def create_braille_tests(language_option):
    """
    This function creates the braille tests for Lib Louis
    
    Parameters:
    language_option (int): The index of the language that the user has chosen

    """

    #The language file is read in to pandas
    language_file=pd.read_csv("languages/filtered_"+languages[language_option]["name"]+".csv",encoding="utf8")
    #The test csv file is read in to pandas
    test_csv=pd.read_csv("braille_tests/"+languages[language_option]["language_code"]+".csv",encoding="utf8")
    #The test yaml file is opened in write mode to create the test
    test_yaml=open("braille_tests/"+languages[language_option]["language_code"]+".yaml","w",encoding="utf8")
    #The test yaml file is written to with the information that is required for the test for Lib Louis
    test_yaml.write("""
# Yaml Test For """+languages[language_option]["name"]+"""
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this file; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# liblouis  comes with ABSOLUTELY NO WARRANTY.

display: unicode.dis
table:
  language: """+languages[language_option]["language_code"]+"""
  grade: 1
  __assert-match: """+languages[language_option]["language_code"]+""".tbl
flags: { testmode: forward }
tests:
  # """+languages[language_option]["name"]+"""
""")
    #This loop goes through each row in the test csv file
    for index,row in test_csv.iterrows():
        braille_test=""
        #This loop goes through each character in the text
        for char in row["Text"]:
            print("Test Char: ",char)
            #finds the braille code for the character
            temp_row=language_file.loc[language_file[languages[language_option]["char_column"]]== char].values[0]
            print(temp_row[-1],"\n")
            #adds the braille code to the braille test
            braille_test+=temp_row[-1]
        print(row["Text"]+": "+braille_test)
        #writes the braille test to the test yaml file
        test_yaml.write('  - ["'+row["Text"]+'", "'+braille_test+'"]\n')
    #The test yaml file is closed to prevent memory leaks
    test_yaml.close()

def get_braille_from_text_in_source(language_option):
    """
    This function converts the text characters to braille characters in the source language file
    
    Parameters:
    language_option (int): The index of the language that the user has chosen
    
    """
    print ("converting text to braille")
    #the language source file is read in to pandas
    language_file=pd.read_csv("languages/source/"+languages[language_option]["name"]+".csv")
    #selects the braille column
    braille_column=language_file[languages[language_option]["braille_column"]]
    #applies the get_braille function to the braille column to convert the text to braille
    new_braille_column=braille_column.apply(get_braille_from_text)
    #the braille column is replaced with the new braille column
    language_file["Braille"]=new_braille_column
    #the file is saved to the source folder
    language_file.to_csv("languages/source/"+languages[language_option]["name"]+".csv",index=False)
    print("done converting text to braille")
