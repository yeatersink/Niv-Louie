from nicegui import app, events, ui
import json
import os.path

# Function to load extentions from JSON file
def load_extentions():
    try:
        with open("utils/extentions_file.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

class Extention:
    def __init__(self):
        self.    extention_name=None
        self.extention_summary=None
        self.extention_description=None
        self.extention_author=None
        self.extention_version=None
        self.extention_minimum_version=None
        self.extention_last_tested_version=None
        self.extention_locale=None
        self.extention_included_projects=None
        self.extentions=load_extentions()
        self.extentions_list = [addon["name"] for addon in self.extentions]


    def update_extentions_list(self):
        self.extentions_list = [addon["name"] for addon in self.extentions]

    def update_extention_name(self,e:events.ValueChangeEventArguments):
        self.extention_name=e.value

    def update_extention_summary(self,e:events.ValueChangeEventArguments):
        self.extention_summary=e.value

    def update_extention_description(self,e:events.ValueChangeEventArguments):
        self.extention_description=e.value

    def update_extention_author(self,e:events.ValueChangeEventArguments):
        self.extention_author=e.value
        
    def update_extention_version(self,e:events.ValueChangeEventArguments):
        self.extention_version=e.value

    def update_extention_minimum_version(self,e:events.ValueChangeEventArguments):
        self.extention_minimum_version=e.value

    def update_extention_last_tested_version(self,e:events.ValueChangeEventArguments):
        self.extention_last_tested_version=e.value

    def update_extention_locale(self,e:events.ValueChangeEventArguments):
        self.extention_locale=e.value

    def update_extention_included_projects(self,e:events.ValueChangeEventArguments):
        self.extention_included_projects=e.value

    def save_extention(self):
        error=False
        if self.extention_name==None:
            ui.notify("Name is required",type="negative")
            error=True
        if self.extention_summary==None:
            ui.notify("Summary is required",type="negative")
            error=True
        if self.extention_description==None:
            ui.notify("Description is required",type="negative")
            error=True
        if self.extention_author==None:
            ui.notify("Author is required",type="negative")
            error=True
        if self.extention_version==None:
            ui.notify("Version is required",type="negative")
            error=True
        if self.extention_minimum_version==None:
            ui.notify("Minimum version is required",type="negative")
            error=True
        if self.extention_last_tested_version==None:
            ui.notify("Last tested version is required",type="negative")
            error=True
        if self.extention_locale==None:
            ui.notify("Locale is required",type="negative")
            error=True
        if self.extention_included_projects==None:
            ui.notify("Included projects is required",type="negative")
            error=True

        for addon in self.extentions:
            if self.extention_name.lower() == addon["name"].lower():
                ui.notify("An extention with that name already exists.",type="negative")
                error=True

        if error:
            return

        extention_object={
            "name":self.extention_name,
            "summary":self.extention_summary,
            "description":self.extention_description,
            "author":self.extention_author,
            "version":self.extention_version,
            "minimum_version":self.extention_minimum_version,
            "last_tested_version":self.extention_last_tested_version,
            "locale":self.extention_locale,
            "included_projects":self.extention_included_projects
        }
        self.extentions.append(extention_object)
        self.update_extentions_list()
        with open("utils/extentions_file.json","w",encoding="utf-8") as file:
            json.dump(self.extentions,file,ensure_ascii=False,indent=4)
        ui.navigate.to("/nvda_extention_builder")
        ui.notify("Extention Saved.",close_button="Ok.")


    def set_fields(self):
        for addon in self.extentions:
            if self.extention_name==addon["name"]:
                self.extention_summary=addon["summary"]
                self.extention_description=addon["description"]
                self.extention_author=addon["author"]
                self.extention_version=addon["version"]
                self.extention_minimum_version=addon["minimum_version"]
                self.extention_last_tested_version=addon["last_tested_version"]
                self.extention_locale=addon["locale"]
                self.extention_included_projects=addon["included_projects"]
                break


    def save_changes(self,old_extention_name):
        updated=False
        if self.extention_name!=old_extention_name and self.extention_name in self.extentions_list:
            ui.notify("You have an Extention with that Name Already!")
            return

        for addon in self.extentions:
            if addon["name"]==old_extention_name:
                addon["name"]=self.extention_name
                addon["summary"]=self.extention_summary
                addon["description"]=self.extention_description
                addon["author"]=self.extention_author
                addon["version"]=self.extention_version
                addon["minimum_version"]=self.extention_minimum_version
                addon["last_tested_version"]=self.extention_last_tested_version
                addon["locale"]=self.extention_locale
                addon["included_projects"]=self.extention_included_projects
                self.update_extentions_list()
                with open("utils/extentions_file.json","w",encoding="utf-8") as file:
                    json.dump(self.extentions,file,ensure_ascii=False,indent=4)
                    os.rename("nvda_extentions/"+old_extention_name+".nvda-addon","nvda_extentions/"+self.extention_name+".nvda-addon")
                    os.rename("nvda_extentions/"+old_extention_name+"-nvda-addon-source","nvda_extentions/"+self.extention_name+"-nvda-addon-source")
                updated=True
                break
        if  updated==True:
            ui.notify("Addon has been Updated!")
        else:
            ui.notify("Failed to Update!")


    def remove_extention(self):
        for addon in self.extentions:
            if addon["name"]==self.extention_name:
                self.extentions.remove(addon)
                self.update_extentions_list()
                with open("utils/extentions_file.json","w",encoding="utf-8") as file:
                    json.dump(self.extentions,file,ensure_ascii=False,indent=4)
                os.remove("nvda_extentions/"+self.extention_name+"-nvda-addon-source")
                os.remove("nvda_extentions/"+self.extention_name+".nvda-addon")
                ui.notify("Extention has been Removed!")


extention=Extention()