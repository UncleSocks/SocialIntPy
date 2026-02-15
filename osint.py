import base64
import json
import tkinter as tk
from tkinter import ttk

import pyperclip
from urllib.parse import quote



WIDGET_LABEL_MAP = {
    "search_type":"Search Type:",
    "id_type":"ID Type:",
    "id_value":"ID:",
    "keyword":"Keyword:",
    "year":"Year:",
    "account":"Account:",
    "section":"Section:",
    "generate_button":"Generate URL"
}

FACEBOOK_BASE_URL = "https://www.facebook.com/"
FACEBOOK_BASE_SEARCH_URL = "https://www.facebook.com/search/"
SEARCH_TYPE_SELECTION = ["Posts", "Photos", "Videos", "People", "Places", 
                         "Events", "Account", "Search"]

YEAR_SELECTION = ["Top", "2025", "2024", "2023", "2022", "2021", 
                  "2020", "2019", "2018", "2017", "2016", "2015", 
                  "2014", "2013", "2012", "2011", "2010"]

ACCOUNT_INFORMATION_MAP = {
    "Timeline":"",
    "About":"about",
    "Intro":"directory_intro",
    "Category":"directory_category",
    "Personal Details":"directory_personal_details",
    "Work":"directory_work",
    "Education":"directory_education",
    "Hobbies":"directory_activites",
    "Interests":"directory_interests",
    "Travel":"directory_travel",
    "Links":"directory_links",
    "Contact Info":"directory_contact_info",
    "Privacy/Legal Info":"directory_privacy_and_legal_info",
    "Names":"directory_names",
    "Details About You":"about_details",
    "Following":"following",
    "Photos":"photos",
    "Photos Albums":"photos_albums",
    "Videos":"videos",
    "Reels":"reels",
    "Check-ins":"places_visited",
    "Visits":"map",
    "Recent Check-ins":"places_recent",
    "Sports":"sports",
    "Music":"music",
    "Movies":"movies",
    "TV":"tv",
    "Books":"books",
    "Apps & Games":"games",
    "Likes":"likes",
    "Events":"events",
    "Facts":"did_you_know",
    "Reviews":"reviews",
    "Reviews Given":"reviews_given",
    "Reviews Written":"reviews_written",
    "Notes":"notes"
}

SEARCH_QUERY_SELECTION = ["top", "posts", "people", "photos", "videos", 
                          "marketplace", "pages", "places", "groups",
                          "apps", "events", "links", "watch"]

POSTS_PHOTOS_VIDEOS_ID_TYPES = ["User ID", "Location ID"]
PEOPLE_ID_TYPES = ["Employer ID", "City ID", "School ID"]
EVENTS_ID_TYPES = ["Location ID"]



def encode(filter_string):
    string_bytes = filter_string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


class ConstructFbUrl:

    def __init__(self, selected_type, widgets):
        self.selected_type = selected_type
        self.widgets = widgets

    def _capture_misc_fields(self):
        self.keyword = (quote(self.widgets.keyword_entry.get().lower() if self.widgets.keyword_entry.get() else self.selected_type))
        self.selected_year = self.widgets.year_selection_combobox.get().lower()

    def _creation_time_json(self):
        creation_time_args = {
            "start_year":f"{self.selected_year}",
            "start_month":f"{self.selected_year}-1",
            "end_year":f"{self.selected_year}",
            "end_month":f"{self.selected_year}-12",
            "start_day":f"{self.selected_year}-1-1",
            "end_day":f"{self.selected_year}-12-31"
        }
        creation_time = {
            "name":"creation_time",
            "args":json.dumps(creation_time_args)
        }
        return json.dumps(creation_time)

    def _construct_user_id_url(self, user_id=None):
        if not user_id:
            output = "Unable to generate URL. Enter a user ID."
            return output
        
        filter_args_dict = {
                "name":"author",
                "args":f"{user_id}"
            }
        
        if self.selected_year == "top":
            raw_filter_dict = {
                "rp_author":f"{json.dumps(filter_args_dict)}"
            }
        else:
            raw_filter_dict = {
                "rp_author":f"{json.dumps(filter_args_dict)}",
                "rp_creation_time":f"{self._creation_time_json()}"
            }

        raw_filter = json.dumps(raw_filter_dict)
        encoded_filter = encode(raw_filter)
        new_fb_url = FACEBOOK_BASE_SEARCH_URL + f"{self.selected_type}" + f"?q={self.keyword}" + f"&epa=FILTERS&filters={encoded_filter}"
        return new_fb_url

    def _construct_location_id_url(self, location_id=None):
        if not location_id:
            output = "Unable to generate URL. Enter a location ID."
            return output
        
        if self.selected_type == "events":
            filter_args_dict = {
                "name":"filter_events_location",
                "args":f"{location_id}"
            }
            raw_filter_dict = {
                "rp_events_locations":f"{json.dumps(filter_args_dict)}"
            }

        else:
            filter_args_dict = {
                "name":"location",
                "args":f"{location_id}"
            }

            if self.selected_type == "posts" and self.selected_year == "top":
                raw_filter_dict = {
                    "rp_location":f"{json.dumps(filter_args_dict)}"
                }
            elif self.selected_type == "posts":
                raw_filter_dict = {
                    "rp_location":f"{json.dumps(filter_args_dict)}",
                    "rp_creation_time":f"{self._creation_time_json()}"
                }
            elif self.selected_type != "posts" and self.selected_year == "top":
                raw_filter_dict = {
                    "rp_author":f"{json.dumps(filter_args_dict)}"
                }
            else:
                raw_filter_dict = {
                    "rp_author":f"{json.dumps(filter_args_dict)}",
                    "rp_creation_time":f"{self._creation_time_json()}"
                }

        raw_filter = json.dumps(raw_filter_dict)
        encoded_filter = encode(raw_filter)
        new_fb_url = FACEBOOK_BASE_SEARCH_URL + f"{self.selected_type}" + f"?q={self.keyword}" + f"&epa=FILTERS&filters={encoded_filter}"
        return new_fb_url

        

    def construct_fb_url(self):
        if self.selected_type == "posts" or self.selected_type == "photos" \
            or self.selected_type == "videos" or self.selected_type == "events" \
                or self.selected_type == "people":
            selected_id = self.widgets.id_type_combobox.get().lower()
            
            id_value = self.widgets.id_entry.get().lower()
            if selected_id == "user id":
                self._capture_misc_fields()
                new_fb_url = self._construct_user_id_url(id_value)
                return new_fb_url
            elif selected_id == "location id":
                self._capture_misc_fields()
                new_fb_url = self._construct_location_id_url(id_value)
                return new_fb_url
            elif selected_id == "employer id" or  selected_id == "city id" \
                or selected_id == "school id":
                print(selected_id)
                
        return
    

def generate_url(widgets):
    selected_type = widgets.search_type_combobox.get().lower()
    if selected_type:
        fb_url = ConstructFbUrl(selected_type, widgets).construct_fb_url()
        pyperclip.copy(fb_url)
        widgets.output_label.config(state="normal")
        widgets.output_label.delete("1.0", "end")
        widgets.output_label.insert(tk.END, fb_url)
        widgets.output_label.config(state="disabled")
    return


class WidgetLogicController:
    def __init__ (self, widgets):
        self.widgets = widgets
        self.widget_disable = DisableWidgets(self.widgets)

    def _setup_posts_photos_videos_widgets(self):
        self.widget_disable.disable_id_entry()
        self.widgets.id_type_combobox.config(value=POSTS_PHOTOS_VIDEOS_ID_TYPES, state="readonly")
        self.widgets.year_selection_combobox.config(value=YEAR_SELECTION, state="readonly")
        self.widgets.year_selection_combobox.set("Top")
        self.widgets.keyword_entry.config(state="normal")

        self.widget_disable.disable_account_entry()
        self.widget_disable.disable_section_combobox()


    def _setup_people_widgets(self):
        self.widgets.id_type_combobox.config(values=PEOPLE_ID_TYPES, state="readonly")
        self.widgets.keyword_entry.config(state="normal")

        self.widget_disable.disable_year_selection()
        self.widget_disable.disable_account_entry()
        self.widget_disable.disable_section_combobox()

    def _setup_places_widgets(self):
        self.widgets.keyword_entry.config(state="normal")

        self.widget_disable.disable_id_type_combobox()
        self.widget_disable.disable_id_entry()
        self.widget_disable.disable_year_selection()
        self.widget_disable.disable_account_entry()
        self.widget_disable.disable_section_combobox()

    def _setup_events_widgets(self):
        self.widgets.id_type_combobox.config(values=EVENTS_ID_TYPES, state="readonly")
        self.widgets.id_type_combobox.set(EVENTS_ID_TYPES[0])
        self.widgets.id_entry.config(state="normal")
        self.widgets.keyword_entry.config(state="normal")

        self.widget_disable.disable_year_selection()
        self.widget_disable.disable_account_entry()
        self.widget_disable.disable_section_combobox()

    def _setup_account_widgets(self):
        self.widgets.account_entry.config(state="normal")
        self.widgets.section_combobox.config(state="readonly", values=list(ACCOUNT_INFORMATION_MAP.keys()))

        self.widget_disable.disable_id_entry()
        self.widget_disable.disable_keyword_entry()
        self.widget_disable.disable_year_selection()

    def _setup_search_widgets(self):
        self.widgets.keyword_entry.config(state="normal")
        self.widgets.section_combobox.config(state="readonly", values=SEARCH_QUERY_SELECTION)

        self.widget_disable.disable_id_type_combobox()
        self.widget_disable.disable_id_entry()
        self.widget_disable.disable_year_selection()
        self.widget_disable.disable_account_entry()


    def search_type_logic(self, event=None):
        self.widgets.id_type_combobox.set("")
        self.widgets.id_type_combobox.config(state="disabled")
        self.selected_type = self.widgets.search_type_combobox.get().lower()
        
        if self.selected_type == "posts" or self.selected_type == "photos" or \
            self.selected_type == "videos":
            self._setup_posts_photos_videos_widgets()
        elif self.selected_type == "people":
            self._setup_people_widgets()
        elif self.selected_type == "places":
            self._setup_places_widgets()
        elif self.selected_type == "events":
            self._setup_events_widgets()
        elif self.selected_type == "account":
            self._setup_account_widgets()
        elif self.selected_type == "search":
            self._setup_search_widgets()
        else:
            self.widget_disable.disable_id_type_combobox()
    
    
    def id_type_logic(self, event=None):
        self.selected_id = self.widgets.id_type_combobox.get().lower()
        if self.selected_id == "user id" or self.selected_id == "location id":
            self.widgets.id_entry.config(state="normal")

        elif self.selected_id == "employer id" or self.selected_id == "city id" \
            or self.selected_id == "location id":
            self.widgets.id_entry.config(state="normal")
        else:
            self.widgets.id_entry.config(state="disabled")


class DisableWidgets:

    def __init__(self, widgets):
        self.widgets = widgets

    def disable_id_type_combobox(self):
        self.widgets.id_type_combobox.set("")
        self.widgets.id_type_combobox.config(state="disabled")

    def disable_id_entry(self):
        self.widgets.id_entry.delete(first=0, last="end")
        self.widgets.id_entry.config(state="disabled")

    def disable_keyword_entry(self):
        self.widgets.keyword_entry.delete(first=0, last="end")
        self.widgets.keyword_entry.config(state="disabled")

    def disable_year_selection(self):
        self.widgets.year_selection_combobox.set("")
        self.widgets.year_selection_combobox.config(state="disabled")

    def disable_account_entry(self):
        self.widgets.account_entry.delete(first=0, last="end")
        self.widgets.account_entry.config(state="disabled")

    def disable_section_combobox(self):
        self.widgets.section_combobox.set("")
        self.widgets.section_combobox.config(state="disabled")



class GenerateWidgets:

    def __init__(self, root):
        self.root = root
        self._root_setup()
        self.widget_controller = WidgetLogicController(self)

    def _root_setup(self):
        self.root.title("Social Media Search Tool")
        self.root.geometry("690x500")
        window_icon = tk.PhotoImage(file="logo.png")
        self.root.iconphoto(True, window_icon)

    def display_widgets(self):
        self.search_type_widgets()
        self.id_type_widgets()
        self.id_entry_widgets()
        self.keyword_widgets()
        self.year_selection_widgets()
        self.account_widgets()
        self.section_widgets()
        self.generate_button()
        self.output_widgets()

    def search_type_widgets(self):
        search_type_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["search_type"])
        search_type_label.grid(row=0, column=0, padx=10, pady=15, sticky="E")
        self.search_type_combobox = ttk.Combobox(self.root, values=SEARCH_TYPE_SELECTION, state="readonly")
        self.search_type_combobox.grid(row=0, column=1, sticky="W")
        self.search_type_combobox.bind("<<ComboboxSelected>>", func=self.widget_controller.search_type_logic)

    def id_type_widgets(self):
        id_type_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["id_type"])
        id_type_label.grid(row=1, column=0, padx=10, pady=15, sticky="E")
        self.id_type_combobox = ttk.Combobox(self.root, state="disabled")
        self.id_type_combobox.grid(row=1, column=1, sticky="W")
        self.id_type_combobox.bind("<<ComboboxSelected>>", func=self.widget_controller.id_type_logic)

    def id_entry_widgets(self):
        id_entry_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["id_value"])
        id_entry_label.grid(row=1, column=2, padx=10, sticky="E")
        self.id_entry = tk.Entry(self.root, state="disabled")
        self.id_entry.grid(row=1, column=3, sticky="W")

    def keyword_widgets(self):
        keyword_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["keyword"])
        keyword_label.grid(row=2, column=0, padx=10, sticky="E")
        self.keyword_entry = tk.Entry(self.root, state="disabled")
        self.keyword_entry.grid(row=2, column=1, sticky="W")

    def year_selection_widgets(self):
        year_selection_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["year"])
        year_selection_label.grid(row=2, column=2, padx=10, sticky="E")
        self.year_selection_combobox = ttk.Combobox(self.root, state="disabled")
        self.year_selection_combobox.grid(row=2, column=3, sticky="W")

    def account_widgets(self):
        account_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["account"])
        account_label.grid(row=3, column=0, padx=10, pady=15, sticky="E")
        self.account_entry = tk.Entry(self.root, state="disabled")
        self.account_entry.grid(row=3, column=1, sticky="W")

    def section_widgets(self):
        section_label = tk.Label(self.root, text=WIDGET_LABEL_MAP["section"])
        section_label.grid(row=3, column=2, padx=10, sticky="E")
        self.section_combobox = ttk.Combobox(self.root, state="disabled")
        self.section_combobox.grid(row=3, column=3, sticky="W")

    def generate_button(self):
        self.generate_button = tk.Button(self.root, text=WIDGET_LABEL_MAP["generate_button"],
                                    command=lambda: generate_url(self), width=20)
        self.generate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=20)

    def output_widgets(self):
        output_frame = tk.Frame(self.root)
        output_frame.grid(row=5, column=0, columnspan=6, sticky="EW", padx=20)
        self.output_label = tk.Text(output_frame, wrap="char")
        self.output_label.pack(fill="both")
        self.output_label.config(height=15)
        self.output_label.config(state="disabled")


root = tk.Tk()
widgets = GenerateWidgets(root)
widgets.display_widgets()
root.mainloop()