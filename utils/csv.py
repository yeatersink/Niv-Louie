#Pandas is used for reading the   csv files
import pandas as pd
#The languages dictionary is imported from the languages.py file
from utils.languages_file import languages
#Warnings is imported to display warnings to the user
import warnings

def create_filtered_csv(language_option):
    """
    This function creates a filtered csv file that only contains the characters, names, and braille codes for the language    
    
    Parameters:
    language_option (int): The index of the language that the user has chosen

"""
    print("Generating",languages[language_option]["name"],"Spreadsheet")
    #The language file is read in to pandas
    language_file=pd.read_csv("languages/source/"+languages[language_option]["name"]+".csv")
    #selects the columns that are needed for the filtered csv file
    filtered_language=language_file[[languages[language_option]["char_column"],"Hex","Type",languages[language_option]["name_column"],languages[language_option]["braille_column"]]].copy()
    #Gets the name column
    name_column=filtered_language[[languages[language_option]["name_column"]]].copy()
    #applies the format_names function to the name column to remove any unwanted characters
    new_name_column=name_column[languages[language_option]["name_column"]].apply(format_names,args=(language_option,))
    #replaces the name column with the new name column
    filtered_language[languages[language_option]["name_column"]]=new_name_column
    #Checks if there are rows where there is a plus in the Hex column and the Type is not set to always
    if filtered_language[(filtered_language["Hex"].str.contains("\+")) & (filtered_language["Type"]!="always")].shape[0]>0:
        #Displays a warning to the user with the characters
        warnings.warn("There are characters with multiple hex values that are not set to always")
        print(filtered_language[(filtered_language["Hex"].str.contains("\+")) & (filtered_language["Type"]!="always")])
        #Checks if there are duplicates in the language file
    if filtered_language.duplicated(keep=False,subset=["Hex"]).sum() > 0:
        #Displays a warning to the user
        warnings.warn("There are duplicates in the language file")
        print(filtered_language[filtered_language.duplicated(keep=False,subset=["Hex"])])
    filtered_language = filtered_language.sort_values(by=["Hex"],key=lambda x:x.str.len(),ascending=False)
    #saves the filtered language file to the languages folder
    filtered_language.to_csv("languages/filtered_"+languages[language_option]["name"]+".csv",index=False)
    print("Spreadsheet Generated")

def format_names(name,language_option):
    """

    This function removes unwanted characters from the name of the character

    Parameters:
    name (str): The name of the character
    
    Returns:
    str: The name of the character without unwanted characters
    
    """
    print(name)

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

def regenerate_characters_using_hex(language_option):
    """
    
    This function regenerates the characters in the language file to the correct characters using the change_characters function
    
    Parameters:
    language_option (int): The index of the language that the user has chosen
    
    """
    print("Regenerating characters")
    #the language source file is read in to pandas
    language_file=pd.read_csv("languages/source/"+languages[language_option]["name"]+".csv")
    #the characters are changed to the correct characters
    language_file[languages[language_option]["char_column"]]=language_file["Hex"].apply(generate_characters)
    #the file is saved to the source folder
    language_file.to_csv("languages/source/"+languages[language_option]["name"]+".csv",index=False)
    print("Characters regenerated")

def generate_characters(hex):
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

