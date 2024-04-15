import pandas as pd

def format_names(name):
    return name.replace("CUNEIFORM SIGN ","")

print("enter 1 to generate spreadsheets or enter 2 to add symbols to nvda")
option=int(input("enter one or two"))
if option == 1:
    print("Generating Spreadsheets")
    akkadian=pd.read_csv("languages/source/Akkadian.csv")
    filtered_akkadian=akkadian[["Character(decimal)","Name"]]
    name_column=filtered_akkadian["Name"]
    new_name_column=name_column.apply(format_names)
    filtered_akkadian["Name"]=new_name_column
    filtered_akkadian.to_csv("languages/filtered_akkadian.csv")
elif option==2:
    print("adding symbols to nvda")
    akkadian=pd.read_csv("languages/filtered_akkadian.csv")
    nvda_symbols_file=open("C:/Program Files (x86)/NVDA/locale/en/symbols.dic","a+",encoding="utf-8")
    nvda_symbols_file.write("\n#Beta Akkadian")
    for index,row in akkadian.iterrows():
        new_line=str(row["Character(decimal)"])+"\t"+str(row["Name"])+"\tmost\talways\n"
        nvda_symbols_file.write(new_line)
    nvda_symbols_file.write("#End Beta Akkadian")
    nvda_symbols_file.close()
else:
    print("That was not a valid option")
