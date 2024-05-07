import pandas as pd
import json

languages=[
    {"name":"Akkadian","language_code":"akk","name_column":"Name","char_column":"Character(decimal)","braille_column":"Braille","replace":["CUNEIFORM SIGN"],"language_information":"""
#for more information on the Akkadian language, please go to:
#https://oracc.museum.upenn.edu/dcclt/signlists/signlists/
#The standard for Akkadian has been set by the academic community represented by ORACC. The braille code for Akkadian follows the standard set by ORACC. The braille code for Akkadian is represented in braille as the name for the sign in Akkadian. Thus, if the Akkadian sign is a "Lum," then the braille code for this sign would be lum.
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

braille_file=open("utils/brailleconverter.json",encoding="utf8")
braille_object=json.load(braille_file)
braille_numbers_file=open("utils/brailletonumbers.json",encoding="utf8")
braille_numbers_object=json.load(braille_numbers_file)

def create_csv(language_option):
    print("Generating",languages[language_option]["name"],"Spreadsheets")
    language_file=pd.read_csv("languages/source/"+languages[language_option]["name"]+".csv")
    filtered_language=language_file[[languages[language_option]["char_column"],languages[language_option]["name_column"],languages[language_option]["braille_column"]]]
    name_column=filtered_language[languages[language_option]["name_column"]]
    new_name_column=name_column.apply(format_names)
    filtered_language["Name"]=new_name_column
    filtered_language.drop_duplicates(inplace=True,subset=[languages[language_option]["char_column"]])
    filtered_language.to_csv("languages/filtered_"+languages[language_option]["name"]+".csv")

def format_names(name):
    if len(languages[language_option]["replace"]) > 0:
        for phrase in languages[language_option]["replace"]:
            if phrase in name:
                name=name.replace(phrase,"").strip()
    return name

def get_braille(text):
    braille=""
    if any(char.isdigit() for char in text):
        newText=""
        for index,char in enumerate(text):
            if char.isdigit():
                newText+="#"+char
            else:
                newText+=char
        text=newText
    if "[q~^]"*3 in text:
        text=text.replace("[q~^]"*3,"^#3")
    if "[q~^]"*2 in text:
        text=text.replace("[q~^]"*2,"^#2")
    if "[q~" in text:
        text=text.replace("[q~","")
    if "]" in text:
        text=text.replace("]","")
    print(text)

    for char in text:
        if char not in braille_numbers_object:
            braille+=braille_object[char.lower()]
        else:
            braille+=char
    if len(braille) > 1:
        if braille[-1]=="-":
            braille=braille[:-1]
    return braille

def change_characters(hex):
    new_char=""
    if "+" in hex:
        for char in hex.split("+"):
            new_char+=chr(int(char,16))
    else:
        new_char=chr(int(hex,16))
    return new_char

def braille_to_numbers(text):
    braille=""
    print(text)
    for char in text:
        braille+=braille_numbers_object[char.lower()]+"-"
    if braille[-1]=="-":
        braille=braille[:-1]
    return braille

def create_tests(language_option):
    language_file=pd.read_csv("languages/filtered_"+languages[language_option]["name"]+".csv",encoding="utf8")
    test_csv=pd.read_csv("braille_tests/"+languages[language_option]["language_code"]+".csv",encoding="utf8")
    test_yaml=open("braille_tests/"+languages[language_option]["language_code"]+".yaml","w",encoding="utf8")
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
    for index,row in test_csv.iterrows():
        braille_test=""
        for char in row["Text"]:
            print("Test Char: ",char)
            temp_row=language_file.loc[language_file[languages[language_option]["char_column"]]== char].values[0]
            print(temp_row[-1],"\n")
            braille_test+=temp_row[-1]
        print(row["Text"]+": "+braille_test)
        test_yaml.write('  - ["'+row["Text"]+'", "'+braille_test+'"]\n')
    test_yaml.close()


print("Please Choose a Language")
for index,language in enumerate(languages):
    print(languages[index]["name"],": ",index+1)
language_option=int(input("Choose a Language"))-1
print("enter 1 to generate spreadsheets, enter 2 to add symbols to nvda, enter 3 to generate braille table, enter 4 to remove extra characters, enter 5 to convert text characters to braille characters, or enter 6 to produce braille test")
option=int(input("enter a number one through 6"))
if option == 1:
    create_csv(language_option)
elif option==2:
    print("adding symbols to nvda for",languages[language_option]["name"])
    language_file=pd.read_csv("languages/filtered_"+languages[language_option]["name"]+".csv")
    nvda_symbols_file=open("C:/Program Files (x86)/NVDA/locale/en/symbols.dic","a+",encoding="utf-8")
    nvda_symbols_file.write("\n#"+languages[language_option]["name"]+"\n")
    for index,row in language_file.iterrows():
        new_line=str(row[languages[language_option]["char_column"]])+"\t"+str(row["Name"])+"\tmost\talways\n"
        nvda_symbols_file.write(new_line)
    nvda_symbols_file.write("#End "+languages[language_option]["name"]+"\n\n")
    nvda_symbols_file.close()
elif option==3:
    print("creating table for lib louis")
    braille=pd.read_csv("languages/filtered_"+languages[language_option]["name"]+".csv")
    braille_table=open("braille/"+languages[language_option]["language_code"]+".tbl","w",encoding="utf-8")
    braille[languages[language_option]["braille_column"]]=braille[languages[language_option]["braille_column"]].apply(braille_to_numbers)
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
    for index, row in braille.iterrows():
        new_line="letter "+str(row[languages[language_option]["char_column"]])+" "+str(row[languages[language_option]["braille_column"]])+"\n"
        braille_table.write(new_line)
    braille_table.close()
elif option==4:
    print("removing characters")
    language_file=pd.read_csv("languages/source/"+languages[language_option]["name"]+".csv")
    language_file[languages[language_option]["char_column"]]=language_file["Hex"].apply(change_characters)
    language_file.to_csv("languages/source/"+languages[language_option]["name"]+".csv")
elif option == 5:
    print ("converting text to braille")
    language_file=pd.read_csv("languages/source/"+languages[language_option]["name"]+".csv")
    braille_column=language_file[languages[language_option]["braille_column"]]
    new_braille_column=braille_column.apply(get_braille)
    language_file["Braille"]=new_braille_column
    language_file.to_csv("languages/source/"+languages[language_option]["name"]+".csv")
elif option==6:
    create_tests(language_option)
else:

    print("That was not a valid option")
