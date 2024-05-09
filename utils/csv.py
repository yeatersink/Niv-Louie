#Pandas is used for reading the   csv files
import pandas as pd
#The languages dictionary is imported from the languages.py file
from utils.languages_file import languages

def create_csv(language_option):
    """
    This function creates a filtered csv file that only contains the characters, names, and braille codes for the language    
    
    Parameters:
    language_option (int): The index of the language that the user has chosen

"""
    print("Generating",languages[language_option]["name"],"Spreadsheet")
    #The language file is read in to pandas
    language_file=pd.read_csv("languages/source/"+languages[language_option]["name"]+".csv")
    #selects the columns that are needed for the filtered csv file
    filtered_language=language_file[[languages[language_option]["char_column"],languages[language_option]["name_column"],languages[language_option]["braille_column"]]].copy()
    #Gets the name column
    name_column=filtered_language[[languages[language_option]["name_column"]]].copy()
    #applies the format_names function to the name column to remove any unwanted characters
    new_name_column=name_column[languages[language_option]["name_column"]].apply(format_names,args=(language_option,))
    #replaces the name column with the new name column
    filtered_language[languages[language_option]["name_column"]]=new_name_column
    #removes any duplicates from the filtered language data frame
    filtered_language.drop_duplicates(inplace=True,subset=[languages[language_option]["char_column"]])
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
