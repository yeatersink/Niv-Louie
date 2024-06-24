#pathlib is used for creating folders
import pathlib
#Pandas is used for reading the   csv files
import pandas as pd
#The languages variable is imported from the languages file
from utils.languages_file import languages

def add_characters_to_nvda(language_option):
    """

        This function adds the characters from the language file to the NVDA symbols file

        Args:
            language_option: The index of the language in the languages variable

    """
    print("adding symbols to nvda for",languages[language_option]["name"])
    #The language file is read in to pandas
    language_file=pd.read_csv("languages/filtered_"+languages[language_option]["name"]+".csv")
    #The nvda symbols file is opened in append mode to add the symbols to the end of the file
    nvda_symbols_file=open("C:/Program Files (x86)/NVDA/locale/en/symbols.dic","a+",encoding="utf8")
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
    print("symbols added to nvda for",languages[language_option]["name"])


def generate_locale_file(language_option):
    """

        This function generates a locale file for the language

        Args:
            language_option: The index of the language in the languages variable

    """
    print("generating nvda  locale file for for",languages[language_option]["name"])
    #The language file is read in to pandas
    language_file=pd.read_csv("languages/filtered_"+languages[language_option]["name"]+".csv")
    new_folder = pathlib.Path("nvda/",languages[language_option]["language_code"])
    new_folder.mkdir(parents=True,exist_ok=True)
    #The locale characters file is created
    nvda_locale_file=open("nvda/"+languages[language_option]["language_code"]+"/characterDescriptions.dic","w",encoding="utf8")
    nvda_locale_file.write("""#"""+languages[language_option]["name"]+""" characterDescriptions.dic
#A part of NonVisual Desktop Access (NVDA)
#URL: http://www.nvda-project.org/
#Copyright (c) 2024Matthew Yeater and Paul Geoghegan.
#This file is covered by the GNU General Public License.
\n""")
    language_file[languages[language_option]["name_column"]]=language_file[languages[language_option]["name_column"]].apply(format_names)
    #this loop goes through each row in the language file which has the type letter and adds the character and name to the nvda symbols file
    for index,row in language_file.loc[(language_file["Type"]=="letter")].sort_values(by=[languages[language_option]["name_column"]]).iterrows():
        new_line=str(row[languages[language_option]["char_column"]])+"\t"+str(row["Name"])+"\n"
        nvda_locale_file.write(new_line)
    #the file is closed to prevent memory leaks
    nvda_locale_file.close()
    #Checks if there are any non-letter characters in the language file
    if not language_file.loc[(language_file["Type"]!="letter")].empty:
        #The locale symbols file is created
        nvda_locale_file=open("nvda/"+languages[language_option]["language_code"]+"/symbols.dic","w",encoding="utf8")
        nvda_locale_file.write("""#"""+languages[language_option]["name"]+""" symbols.dic
#A part of NonVisual Desktop Access (NVDA)
#URL: http://www.nvda-project.org/
#Copyright (c) 2024Matthew Yeater and Paul Geoghegan.
#This file is covered by the GNU General Public License.
\n""")    
        #this loop goes through each row in the language file which does not have the type letter and adds the character and name to the nvda symbols file
        for index,row in language_file.loc[(language_file["Type"]!="letter")].sort_values(by=[languages[language_option]["name_column"]]).iterrows():
            new_line=str(row[languages[language_option]["char_column"]])+"\t"+str(row["Name"])+"\tmost\talways\n"
            nvda_locale_file.write(new_line)
        #the file is closed to prevent memory leaks
        nvda_locale_file.close()
    print("Generated Locale files for NVDA for",languages[language_option]["name"])

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