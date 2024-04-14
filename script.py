import pandas as pd

def format_names(name):
    return name.replace("CUNEIFORM SIGN ","")

akkadian=pd.read_csv("languages/source/Akkadian.csv")
filtered_akkadian=akkadian[["Character(decimal)","Name"]]
name_column=filtered_akkadian["Name"]
new_name_column=name_column.apply(format_names)
filtered_akkadian["Name"]=new_name_column
filtered_akkadian.to_csv("languages/filtered_akkadian.csv")