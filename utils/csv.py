#json is used for reading the json files
import json
#Pandas is used for reading the   csv files
import pandas as pd
#Warnings is imported to display warnings to the user
import warnings
#os is imported to create directories
import os
#The project module is imported to get the project name
from utils.project import project
#the io module is imported to create a report file like object
import io
#the ui module is used to download the report
from nicegui import  ui
import sys
from utils.logger import logger

# Get the base path for the executable
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

#the braille_to_numbers file is used to check if there are any non-braille characters braille_numbers_object variable
try:
    braille_numbers_file=open(os.path.join(base_path,"utils","braille_to_numbers.json"),encoding="utf8")
    braille_numbers_object=json.load(braille_numbers_file)
except Exception as e:
    logger.error("Could not open braille_to_numbers.json"  + str(e))
    raise



appdata_dir=os.getenv("LOCALAPPDATA")
niv_louie_app_data=os.path.join(appdata_dir,"Niv_Louie")
os.makedirs(niv_louie_app_data,exist_ok=True)


def create_filtered_csv():
    """
    This function creates a filtered csv file that only contains the characters, names, and braille codes for the language    
    """
    logger.info("Generating "+project.project_name+" filtered Spreadsheet")
    language_source_path=os.path.join(niv_louie_app_data,"languages","source")
    #The language file is read in to pandas
    logger.info("Reading the language file")
    language_file=pd.read_csv(os.path.join(language_source_path,project.project_name+".csv"))
    #A dictionary is created to store the rows that contain errors
    report={
        "missing_columns":pd.DataFrame(columns=language_file.columns),
        "duplicates":pd.DataFrame(columns=language_file.columns),
        "missing_always":pd.DataFrame(columns=language_file.columns),
        "extra_equals_in_hex":pd.DataFrame(columns=language_file.columns),
        "hex_wrong_length":pd.DataFrame(columns=language_file.columns),
        "extra_spaces":pd.DataFrame(columns=language_file.columns),
        "missing_hex":pd.DataFrame(columns=language_file.columns),
        "missing_braille":pd.DataFrame(columns=language_file.columns),
        "non_braille_in_braille_column":pd.DataFrame(columns=language_file.columns)
        }
    #selects the columns that are needed for the filtered csv file
    logger.info("Selecting the columns that are needed for the filtered csv file")
    filtered_language=language_file[[project.project_character_column,"Hex","Type",project.project_name_column,project.project_braille_column]].copy()
    # Ensures the name column contains string values
    logger.info("Ensuring the name column contains string values")
    filtered_language[project.project_name_column] = filtered_language[project.project_name_column].astype(str)
    # Sets the index to start at 2 so that the line numbers of the csv will line up with the index of the dataframe
    logger.info("Setting the index to start at 2")
    filtered_language.index = range(2, 2 + len(filtered_language))
    #applies the format_names function to the name column to remove any unwanted characters
    logger.info("Applying the format_names function to the name column to remove any unwanted characters")
    filtered_language[project.project_name_column]=filtered_language[project.project_name_column].apply(format_names)
    #Checks if there are rows where there is a plus in the Hex column and the Type is not set to always
    if filtered_language[(filtered_language["Hex"].str.contains("\+")) & (~filtered_language["Type"].str.contains("always"))].shape[0]>0:
        logger.warning("There are characters with multiple hex values that are not set to always")
        #Adds the characters to the report dictionary
        report["missing_always"]=filtered_language[(filtered_language["Hex"].str.contains("\+")) & (~filtered_language["Type"].str.contains(r'\balways\b'))]

        #Checks if there are duplicates in the language file
    if filtered_language.duplicated(keep=False,subset=["Hex"]).sum() > 0:
        logger.warning("There are duplicates in the language file")
        #Adds the duplicates to the report dictionary
        report["duplicates"]=filtered_language[filtered_language.duplicated(keep=False,subset=["Hex"])]

    #Loops through the rows in filtered_language
    for index,row in filtered_language.iterrows():
        # Checks if the number of columns in the current row is less than the number of columns in the filtered file
        if len(row)<len(filtered_language.columns):
            logger.warning("There are missing columns in the language file on row "+str(index))
            #Adds the row to the report dictionary
            report["missing_columns"].loc[index]=row
        #Checks if there are any extra spaces in the character column
        if "  " in row[project.project_character_column]:
            logger.warning("There are characters with extra spaces in the character column on row "+str(index))
            #Adds the row to the report dictionary
            report["extra_spaces"].loc[index]=row
        # Checks if the hex column is empty, nan, or contains whitespace characters
        if row["Hex"]=="NAN" or row["Hex"]=="" or row["Hex"]=="nan" or row["Hex"].isspace():
            logger.warning("There are characters with missing hex on row "+str(index))
            #Adds the row to the report dictionary
            report["missing_hex"].loc[index]=row
        else:
            # Checks if there is more than one equals sign in the hex column in a row
            if "++" in row["Hex"]:
                logger.warning("There are characters with extra equals in the hex column on row "+str(index))
                #Adds the row to the report dictionary
                report["extra_equals_in_hex"].loc[index]=row
            # Checks if the hex column is not the correct length
            hex_list=row["Hex"].split("+")
            if any([len(hex_char)!=4 for hex_char in hex_list]):
                logger.warning("There are characters with hex values that are not the correct length on row "+str(index))
                #Adds the row to the report dictionary
                report["hex_wrong_length"].loc[index]=row
        #Checks if the braille column is empty, nan, or contains whitespace characters
        if row[project.project_braille_column]=="NAN" or row[project.project_braille_column]=="" or row[project.project_braille_column]=="nan" or row[project.project_braille_column].isspace():
            logger.warning("There are characters with missing braille on row "+str(index))
            #Adds the row to the report dictionary
            report["missing_braille"].loc[index]=row
        #Checks if there are any non-braille characters in the braille column
        elif any([char not in braille_numbers_object for char in str(row[project.project_braille_column])]):
            logger.warning("There are non-braille characters in the braille column on row "+str(index))
            #Adds the row to the report dictionary
            report["non_braille_in_braille_column"].loc[index]=row

    filtered_language = filtered_language.sort_values(by=["Hex"],key=lambda x:x.str.len(),ascending=False)
    #saves the filtered language file to the languages folder
    logger.info("Saving the filtered language file to the languages folder")
    if not os.path.exists(os.path.join(niv_louie_app_data,"languages","filtered")):
        os.makedirs(os.path.join(niv_louie_app_data,"languages","filtered"))
    filtered_language.to_csv(os.path.join(niv_louie_app_data,"languages","filtered",project.project_name+".csv"),index=False)
    #Creates a report file like object
    logger.info("Creating a report file like object")
    report_file = io.BytesIO()
    #writes basic information to the report
    try:
        report_file. write(("Report for "+project.project_name+"\n").encode("utf-8"))
        report_file.write(("Generated on "+pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")+"\n").encode("utf-8"))
    except Exception as e:
        logger.error("Could not write the basic information to the report file" + str(e))
        raise

    #Creates variable to check if there are any errors
    errors=False

    #Checks if there are any missing columns
    if len(report["missing_columns"])>0:
        #Writes the missing columns to the report
        try:
            errors=True
            report_file.write(("\n**Missing Columns: "+str(len(report["missing_columns"]))+"**\n").encode("utf-8"))
            report_file.write(report["missing_columns"].to_string().encode("utf-8"))
        except Exception as e:
            logger.error("Could not write the missing columns to the report file" + str(e))
            raise

    #Checks if there are any duplicates
    if len(report["duplicates"])>0:
        #Writes the duplicates to the report
        try:
            errors=True
            report_file.write(("\n**Duplicates: "+str(len(report["duplicates"]))+"**\n").encode("utf-8"))
            report_file.write(report["duplicates"].to_string().encode("utf-8"))
        except Exception as e:
            logger.error("Could not write the duplicates to the report file" + str(e))
            raise

    #Checks if there are any characters with multiple hex values that are not set to always
    if len(report["missing_always"])>0:
        #Writes the characters to the report
        try:
            errors=True
            report_file.write(("\n**Characters with multiple hex values that are not set to always: "+str(len(report["missing_always"]))+"**\n").encode("utf-8"))
            report_file.write(report["missing_always"].to_string().encode("utf-8"))
        except Exception as e:
            logger.error("Could not write the characters with multiple hex values that are not set to always to the report file" + str(e))
            raise

    #Checks if there are any characters with extra equals in the hex column
    if len(report["extra_equals_in_hex"])>0:
        #Writes the characters to the report
        try:
            errors=True
            report_file.write(("\n**Characters with extra equals in the hex column: "+str(len(report["extra_equals_in_hex"]))+"**\n").encode("utf-8"))
            report_file.write(report["extra_equals_in_hex"].to_string().encode("utf-8"))
        except Exception as e:
            logger.error("Could not write the characters with extra equals in the hex column to the report file" + str(e))
            raise

    #Checks if there are any characters with hex values that are not the correct length
    if len(report["hex_wrong_length"])>0:
        #Writes the characters to the report
        try:
            errors=True
            report_file.write(("\n**Characters with hex values that are not the correct length: "+str(len(report["hex_wrong_length"]))+"**\n").encode("utf-8"))
            report_file.write(report["hex_wrong_length"].to_string().encode("utf-8"))
        except Exception as e:
            logger.error("Could not write the characters with hex values that are not the correct length to the report file" + str(e))
            raise

    #Checks if there are any characters with extra spaces
    if len(report["extra_spaces"])>0:
        #Writes the characters to the report
        try:
            errors=True
            report_file.write(("\n**Characters with extra spaces: "+str(len(report["extra_spaces"]))+"**\n").encode("utf-8"))
            report_file.write(report["extra_spaces"].to_string().encode("utf-8"))
        except Exception as e:
            logger.error("Could not write the characters with extra spaces to the report file" + str(e))
            raise

    #Checks if there are any characters with non-braille characters in the braille column
    if len(report["non_braille_in_braille_column"])>0:
        #Writes the characters to the report
        try:
            errors=True
            report_file.write(("\n**Characters with non-braille characters in the braille column: "+str(len(report["non_braille_in_braille_column"]))+"**\n").encode("utf-8"))
            report_file.write(report["non_braille_in_braille_column"].to_string().encode("utf-8"))
        except Exception as e:
            logger.error("Could not write the characters with non-braille characters in the braille column to the report file" + str(e))
            raise

    #Checks if there are any characters with missing braille
    if len(report["missing_braille"])>0:
        #Writes the characters to the report
        try:
            errors=True
            report_file.write(("\n**Characters with missing braille: "+str(len(report["missing_braille"]))+"**\n").encode("utf-8"))
            report_file.write(report["missing_braille"].to_string().encode("utf-8"))
        except Exception as e:
            logger.error("Could not write the characters with missing braille to the report file" + str(e))
            raise

    #Checks if there are any characters with missing hex
    if len(report["missing_hex"])>0:
        #Writes the characters to the report
        try:
            errors=True
            report_file.write(("\n**Characters with missing hex: "+str(len(report["missing_hex"]))+"**\n").encode("utf-8"))
            report_file.write(report["missing_hex"].to_string().encode("utf-8"))
        except Exception as e:
            logger.error("Could not write the characters with missing hex to the report file" + str(e))
            raise

    #Checks if there are any errors
    if not errors:
        #Writes that there are no errors to the report
        try:
            report_file.write("\nNo errors found, good job!".encode("utf-8"))
        except Exception as e:
            logger.error("Could not write that there are no errors found to the report file" + str(e))
            raise

    #Downloads report file
    logger.info("Downloading the report file")
    ui.download(report_file.getvalue(), filename=project.project_name+"_report.txt")


def format_names(name):
    """

    This function removes unwanted characters from the name of the character

    Parameters:
    name (str): The name of the character
    
    Returns:
    str: The name of the character without unwanted characters
    
    """
    print(name)

    #checks if the name contains any of the unwanted characters
    if not project.project_replace==None:
        #loops through the unwanted characters
        for phrase in project.project_replace:
            #checks if the unwanted character is in the name
            if phrase in name:
                #removes the unwanted character from the name
                name=name.replace(phrase,"").strip()
    #returns the name without the unwanted characters
    return name

def regenerate_characters_using_hex():
    """
    
    This function regenerates the characters in the language file to the correct characters using the change_characters function
    
    Parameters:
     (int): The index of the language that the user has chosen
    
    """
    print("Regenerating characters")
    language_file_path = os.path.join(niv_louie_app_data,"languages","source",project.project_name+".csv")
    #the language source file is read in to pandas
    language_file=pd.read_csv(language_file_path)
    #the characters are changed to the correct characters
    language_file[project.project_character_column]=language_file["Hex"].apply(generate_characters)
    #the file is saved to the appdata source folder
    language_file.to_csv(language_file_path,index=False)
    #Updates project_text
    project.load_language_source()
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
    print(hex)
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


def regenerate_hex_using_characters():
    """
    
    This function regenerates the Unicode in the language file to the correct Hex using the change_characters function
        
    """
    print("Regenerating hex")
    language_file_path = os.path.join(niv_louie_app_data,"languages","source",project.project_name+".csv")
    #the language source file is read in to pandas
    language_file=pd.read_csv(language_file_path)
    #the Hex Column is changed to the correct Unicode Values 
    language_file["Hex"]=language_file[project.project_character_column].apply(generate_hex)
    #the file is saved to the appdata source folder
    language_file.to_csv(language_file_path,index=False)
    #Updates project_text
    project.load_language_source()
    print("Hex Column regenerated")


def generate_hex(characters):
    """
    This function generates the characters from hex to the correct Unicode
    
    Parameters:
    characters (str): The character or characters that is to be changed
    
    Returns:
    str: The correct hex
    
    """
    
    new_hex=""
    print(characters)

    if characters=="" or characters=="NAN":
        return ""

    #loops through the characters
    for char in characters:
        #converts the character to hex and adds it to the new hex
        new_hex+=hex(ord(char))[2:]+"+"

    #removes the last plus sign
    new_hex=new_hex[:-1]

    #returns the new hex
    return new_hex

