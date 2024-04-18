import pandas as pd
import json

braille_file=open("utils/brailleconverter.json")
braille_object=json.load(braille_file)


def format_names(name):
    return name.replace("CUNEIFORM SIGN ","")

def get_braille(text):
    braille=""
    if any(char.isdigit() for char in text):
        for index,char in enumerate(text):
            if char.isdigit():
                text=text[:index]+"_#"+text[index:]
    if "[q~*]" in text:
        text=text.replace("[q~*]","*")
    if "[q~+]" in text:
        text=text.replace("[q~+]","+")
    if "[q~/]" in text:
        text=text.replace("[q~/]","/")
    if "[q~^]"*3 in text:
        text=text.replace("[q~^]"*3,"^#3")
    if "[q~^]"*2 in text:
        text=text.replace("[q~^]"*2,"^#2")
    if "[q~$]" in text:
        text=text.replace("[q~$]","OPPOSING")
    if "[q~&]" in text:
        text=text.replace("[q~&]","CROSSING")
    if "lt;" in text:
        text=text.replace("lt;","<")
    if "[q~%]" in text:
        text=text.replace("[q~%]","ROTATED NINETY DEGREES")

    for char in text:
        braille+=braille_object[char.lower()]+"-"

    if braille[-1]=="-":
        braille=braille[:-1]
    return braille

print("enter 1 to generate spreadsheets, enter 2 to add symbols to nvda, or enter 3 to genera te braille table")
option=int(input("enter one, two, or three"))
if option == 1:
    print("Generating Spreadsheets")
    akkadian=pd.read_csv("languages/source/Akkadian.csv")
    filtered_akkadian=akkadian[["Character(decimal)","Name","Braille"]]
    name_column=filtered_akkadian["Name"]
    new_name_column=name_column.apply(format_names)
    filtered_akkadian["Name"]=new_name_column
    braille_column=filtered_akkadian["Braille"]
    new_braille_column=braille_column.apply(get_braille)
    filtered_akkadian["Braille"]=new_braille_column
    filtered_akkadian.to_csv("languages/filtered_akkadian.csv")
elif option==2:
    print("adding symbols to nvda")
    akkadian=pd.read_csv("languages/filtered_akkadian.csv")
    nvda_symbols_file=open("C:/Program Files (x86)/NVDA/locale/en/symbols.dic","a+",encoding="utf-8")
    nvda_symbols_file.write("\n#Beta Akkadian\n")
    for index,row in akkadian.iterrows():
        new_line=str(row["Character(decimal)"])+"\t"+str(row["Name"])+"\tmost\talways\n"
        nvda_symbols_file.write(new_line)
    nvda_symbols_file.write("#End Beta Akkadian\n\n")
    nvda_symbols_file.close()
elif option==3:
    braille_file=open("utils/brailleconverter.json")
    braille_object=json.load(braille_file)
    
else:
    print("That was not a valid option")
