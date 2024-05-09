#Pandas is used for reading the   csv files
import pandas as pd
#json is used for reading the json files
import json

#languages is a list of dictionaries that contain information about the languages that are being used in the project
#The dictionaries contain the following
#name: the name of the language
#language_code: the ISO code for the language
#name_column: the name of the column in the csv file that contains the name of the character
#char_column: the name of the column in the csv file that contains the character
#braille_column: the name of the column in the csv file that contains the braille code for the character
#replace: a list of strings that are to be removed from the name of the character
#language_information: a string that contains information about the language for Lib Louis
#contributers: a string that contains information about the people who have contributed to the project
languages=[
    {"name":"Akkadian","language_code":"akk","name_column":"Name","char_column":"Character(decimal)","braille_column":"Braille","replace":["CUNEIFORM SIGN"],"language_information":"""
#for more information on the Akkadian language, please go to:
#https://oracc.museum.upenn.edu/dcclt/signlists/signlists/
#The standard for Akkadian has been set by the academic community represented by ORACC. The braille code for Akkadian follows the standard set by ORACC. The braille code for Akkadian is represented in braille as the name for the sign in Akkadian. Thus, if the Akkadian sign is a "Lum," then the braille code for this sign would be lum.
""","contributers":"""
#This project is overseen by Ariel University and supervised by Dr. Shai Gordin
# Maintained by Matityahu Yeshurun and Paul Geoghegan
"""},
    {"name":"Greek","language_code":"grc-koine","name_column":"Name","char_column":"Character","braille_column":"Braille","replace":["CUNEIFORM SIGN"],"language_information":"""
#for more information on the Koine Greeklanguage, please go to:
#https://www.koinegreek.com/
#The standard for Koine Greek has been set by the academic community . The braille code for Koine Greek follows the standard set.
""","contributers":"""
#This project is overseen by Ariel University and supervised by Dr. Shai Gordin
# Maintained by Matityahu Yeshurun and Paul Geoghegan
"""},
        {"name":"Hebrew","language_code":"heb","name_column":"Name","char_column":"Character","braille_column":"Braille","replace":["point","punctuation","mark","letter","accent","*"],"language_information":"""
#for more information on the Hebrew language, please go to:
#https://mechon-mamre.org/index.htm
#The standard for Hebrew has been set by the community represented by Jewish studies. The braille code for Hebrew follows the standard set by HIJS. The braille code for Hebrew is represented in braille as the name for the sign in Hebrew. Thus, if the Hebrew sign is a "Bet," then the braille code for this sign would be bet represented by early forms of Hebrew braille.
""","contributers":"""
#This project is overseen by Ariel University and supervised by Dr. Shai Gordin 
# Maintained by Matityahu Yeshurun and Paul Geoghegan
"""},
        {"name":"Syriac","language_code":"syc","name_column":"Name","char_column":"Character","braille_column":"Braille","replace":[]},
        {"name":"Transliteration","language_code":"transliteration","name_column":"Name","char_column":"Character","braille_column":"Braille","replace":[],"language_information":"""
#for more information on the Transliteration table, please go to:
#http://oracc.ub.uni-muenchen.de/doc/help/languages/ugaritic/index.html
#The standard for Transliteration has been set by the academic community represented by ORACC. The braille code for transliteration follows the standard set by ORACC. The braille code for transliteration is represented in braille as the name for the sign in the transliteation table. Thus, if the sign is a "a," then the braille code for this sign would be a.
""","contributers":"""
#This project is overseen by Ariel University and supervised by Dr. Shai Gordin
# Maintained by Matityahu Yeshurun and Paul Geoghegan
"""},
        {"name":"Ugaritic","language_code":"ug","name_column":"Name","char_column":"Character(decimal)","braille_column":"Braille","replace":["UGARITIC LETTER","UGARITIC "],"language_information":"""
#for more information on the Ugaritic language, please go to:
#https://oracc.museum.upenn.edu/aemw/ugarit/corpus
#The standard for Ugaritic has been set by the academic community represented by ORACC. The braille code for Ugaritic follows the standard set by ORACC. The braille code for Ugaritic is represented in braille as the name for the sign in Ugaritic. Thus, if the Ugaritic sign is a "Alepha," then the braille code for this sign would be a.
""","contributers":"""
#This project is overseen by Ariel University and supervised by Dr. Shai Gordin
# Maintained by Matityahu Yeshurun and Paul Geoghegan
"""}
    ]

#The brailleconverter.json file is opened and read in to the braille_object variable
braille_file=open("utils/brailleconverter.json",encoding="utf8")

braille_object=json.load(braille_file)
#The braille_numbers.json file is opened and read in to the braille_numbers_object variable
braille_numbers_file=open("utils/brailletonumbers.json",encoding="utf8")
braille_numbers_object=json.load(braille_numbers_file)

def create_csv(language_option):
    """
    This function creates a filtered csv file that only contains the characters, names, and braille codes for the language    
    
    Parameters:
    language_option (int): The index of the language that the user has chosen

"""
    print("Generating",languages[language_option]["name"],"Spreadsheets")
    #The language file is read in to pandas
    language_file=pd.read_csv("languages/source/"+languages[language_option]["name"]+".csv")
    #selects the columns that are needed for the filtered csv file
    filtered_language=language_file[[languages[language_option]["char_column"],languages[language_option]["name_column"],languages[language_option]["braille_column"]]]
    #selects the name column
    name_column=filtered_language[languages[language_option]["name_column"]]
    #applies the format_names function to the name column to remove any unwanted characters
    new_name_column=name_column.apply(format_names)
    #replaces the name column with the new name column
    filtered_language["Name"]=new_name_column
    #removes any duplicates from the filtered language file
    filtered_language.drop_duplicates(inplace=True,subset=[languages[language_option]["char_column"]])
    #saves the filtered language file to the languages folder
    filtered_language.to_csv("languages/filtered_"+languages[language_option]["name"]+".csv")

def format_names(name):
    """

    This function removes unwanted characters from the name of the character

    Parameters:
    name (str): The name of the character
    
    Returns:
    str: The name of the character without unwanted characters
    
    """

    #checks if the name contains any of the unwanted characters
    if len(languages[language_option]["replace"]) > 0:
        #loops through the unwanted characters
        for phrase in languages[language_option]["replace"]:
            #checks if the unwanted character is in the name
            if phrase in name:
                #removes the unwanted character from the name
                name=name.replace(phrase,"").strip()
    #returns the name without the unwanted characters
    return name

def get_braille(text):
    """
    This function converts text characters to braille characters

    Parameters:
    text (str): The text that is to be converted to braille

    Returns:
    str: The braille code for the text

    """

    #The braille variable is initialized as an empty string
    braille=""
    #The text is checked to see if it contains any numbers
    if any(char.isdigit() for char in text):
        newText=""
        #The text is looped
        for index,char in enumerate(text):
            #checks if the character is a number
            if char.isdigit():
                #adds a number sign to the character
                newText+="#"+char
            else:
                #adds the character to the new text
                newText+=char
        #the text is replaced with the new text
        text=newText
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

def change_characters(hex):
    """
    This function changes the hex characters to the correct characters
    
    Parameters:
    hex (str): The hex character that is to be changed
    
    Returns:
    str: The correct character
    
    """
    
    new_char=""
        #checks if the hex character contains a plus sign as this indicates that there are multiple characters
    if "+" in hex:
        #splits the hex character into a list of characters and loops through the characters
        for char in hex.split("+"):
            #converts the hex character to a character and adds it to the new character
            new_char+=chr(int(char,16))
    else:
        #converts the hex character to a character
        new_char=chr(int(hex,16))
    #returns the new character
    return new_char

def braille_to_numbers(text):
    """
    This function converts braille characters to numbers
    
    Parameters:
    text (str): The braille character that is to be converted
    
    Returns:
    str: The number that corresponds to the braille character

    """

    braille=""
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

def create_tests(language_option):
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


print("Please Choose a Language")
#This loop prints out the languages that are available for the user to choose from
#we use index+1 to make the index start at 1 instead of 0
for index,language in enumerate(languages):
    print(languages[index]["name"],": ",index+1)
#The user is asked to choose a language
language_option=int(input("Choose a Language"))-1
print("enter 1 to generate spreadsheets, enter 2 to add symbols to nvda, enter 3 to generate braille table, enter 4 regenerate characters, enter 5 to convert text characters to braille characters, or enter 6 to produce braille test")
option=int(input("enter a number one through 6"))
#option 1 creates the filtered csv file
if option == 1:
    #The create_csv function is called with the chosen language
    create_csv(language_option)
#option 2 adds the symbols to the nvda symbols file
elif option==2:
    print("adding symbols to nvda for",languages[language_option]["name"])
    #The language file is read in to pandas
    language_file=pd.read_csv("languages/filtered_"+languages[language_option]["name"]+".csv")
    #The nvda symbols file is opened in append mode to add the symbols to the end of the file
    nvda_symbols_file=open("C:/Program Files (x86)/NVDA/locale/en/symbols.dic","a+",encoding="utf-8")
    #a comment is added to the file to show where the symbols for the language start
    nvda_symbols_file.write("\n#"+languages[language_option]["name"]+"\n")
    #this loop goes through each row in the language file and adds the character and name to the nvda symbols file
    for index,row in language_file.iterrows():
        new_line=str(row[languages[language_option]["char_column"]])+"\t"+str(row["Name"])+"\tmost\talways\n"
        nvda_symbols_file.write(new_line)
    #a comment is added to the file to show where the symbols for the language end
    nvda_symbols_file.write("#End "+languages[language_option]["name"]+"\n\n")
    #the file is closed to prevent memory leaks
    nvda_symbols_file.close()
#option 3 creates the braille table for lib louis
elif option==3:
    print("creating table for lib louis")
    #The language file is read in to pandas
    braille=pd.read_csv("languages/filtered_"+languages[language_option]["name"]+".csv")
    #The braille table is opened in write mode to create the table
    braille_table=open("braille/"+languages[language_option]["language_code"]+".tbl","w",encoding="utf-8")
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

"""+languages[language_option]["language_information"]+languages[language_option]["contributers"])
    #This loop goes through each row in the braille file and writes the braille code and the number to the braille table
    for index, row in braille.iterrows():
        new_line="letter "+str(row[languages[language_option]["char_column"]])+" "+str(row[languages[language_option]["braille_column"]])+"\n"
        braille_table.write(new_line)
        #The braille table is closed to prevent memory leaks
    braille_table.close()
#option 4 regenerates the characters in the language file
elif option==4:
    print("Regenerating characters")
    #the language source file is read in to pandas
    language_file=pd.read_csv("languages/source/"+languages[language_option]["name"]+".csv")
    #the characters are changed to the correct characters
    language_file[languages[language_option]["char_column"]]=language_file["Hex"].apply(change_characters)
    #the file is saved to the source folder
    language_file.to_csv("languages/source/"+languages[language_option]["name"]+".csv")
#option 5 converts the text characters to braille characters in the source language file
elif option == 5:
    print ("converting text to braille")
    #the language source file is read in to pandas
    language_file=pd.read_csv("languages/source/"+languages[language_option]["name"]+".csv")
    #selects the braille column
    braille_column=language_file[languages[language_option]["braille_column"]]
    #applies the get_braille function to the braille column to convert the text to braille
    new_braille_column=braille_column.apply(get_braille)
    #the braille column is replaced with the new braille column
    language_file["Braille"]=new_braille_column
    #the file is saved to the source folder
    language_file.to_csv("languages/source/"+languages[language_option]["name"]+".csv")
#option 6 creates the braille tests for Lib Louis
elif option==6:
    #The create_tests function is called with the chosen language
    create_tests(language_option)
#If the user enters an invalid option, they are told that the option is not valid
else:
    print("That was not a valid option")
