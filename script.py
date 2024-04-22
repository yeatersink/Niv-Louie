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
    print("creating table for lib louis")
    akkadian=pd.read_csv("languages/filtered_akkadian.csv")
    braille_table=open("braille/beta-akkadian.tbl","w",encoding="utf-8")
    braille_table.write("""
# liblouis: Beta Akkadian Grade 1 table
#
# ------------
#-name: Beta Akkadian grade 1
#-index-name: Akkadian uncontracted
#-display-name: Akkadian uncontracted braille as used in the study of Akkadian .
#
#+language:akk
#+type:literary
#+contraction:no
#+grade:1
#+system:AKK

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

# Maintained by Matt Yeater and Paul Geoghegan
""")
    for index, row in akkadian.iterrows():
        new_line="always "+str(row["Character(decimal)"])+" "+str(row["Braille"])+"\n"
        braille_table.write(new_line)
    braille_table.close()
else:
    print("That was not a valid option")
