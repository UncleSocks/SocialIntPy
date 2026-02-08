import base64
import tkinter as tk
from tkinter import ttk
import pyperclip
from urllib.parse import quote


root = tk.Tk()
root.title("SocMed OSINT Helper")



FACEBOOK_BASE_URL = "https://www.facebook.com/search/"



def encode(filter_string):
    string_bytes = filter_string.encode('ascii')
    baase64_bytes = base64.b64encode(string_bytes)
    base64_string = baase64_bytes.decode('ascii')
    return base64_string


class ConstructFbUrl:

    def __init__ (self, selected_type):
        self.selected_type = selected_type
        self.construct_url()

    def _capture_keyword_and_year(self):
        self.keyword = (quote(keyword_entry.get().lower()) if keyword_entry.get() else self.selected_type)
        self.selected_year = select_year.get().lower()

    def construct_user_id(self, user_id):
        if self.selected_year == "top":
            raw_filter = f'{{"rp_author":"{{\\"name\\":\\"author\\",\\"args\\":\\"{user_id}\\"}}"}}'
        else:
            raw_filter = f'{{"rp_author":"{{\\"name\\":\\"author\\",\\"args\\":\\"{user_id}\\"}}","rp_creation_time":"{{\\"name\\":\\"creation_time\\",\\"args\\":\\"{{\\\\\\"start_year\\\\\\":\\\\\\"{self.selected_year}\\\\\\",\\\\\\"start_month\\\\\\":\\\\\\"{self.selected_year}-1\\\\\\",\\\\\\"end_year\\\\\\":\\\\\\"{self.selected_year}\\\\\\",\\\\\\"end_month\\\\\\":\\\\\\"{self.selected_year}-12\\\\\\",\\\\\\"start_day\\\\\\":\\\\\\"{self.selected_year}-1-1\\\\\\",\\\\\\"end_day\\\\\\":\\\\\\"{self.selected_year}-12-31\\\\\\"}}\\"}}"}}'
        
        encoded_filter = encode(raw_filter)
        new_fb_url = FACEBOOK_BASE_URL + f"{self.selected_type}" + f"?q={self.keyword}" + f"&epa=FILTERS&filters={encoded_filter}"
        return new_fb_url
    
    def construct_location_id(self, location_id):
        if self.selected_type == "events":
            raw_filter = f'{{"rp_events_location":"{{\\"name\\":\\"filter_events_location\\",\\"args\\":\\"{location_id}\\"}}"}}'
        
        elif self.selected_type == "posts":
            if self.selected_year == "top":
                raw_filter = f'{{"rp_location":"{{\\"name\\":\\"location\\",\\"args\\":\\"{location_id}\\"}}"}}'
            else:
                raw_filter = f'{{"rp_location":"{{\\"name\\":\\"location\\",\\"args\\":\\"{location_id}\\"}}","rp_creation_time":"{{\\"name\\":\\"creation_time\\",\\"args\\":\\"{{\\\\\\"start_year\\\\\\":\\\\\\"{self.selected_year}\\\\\\",\\\\\\"start_month\\\\\\":\\\\\\"{self.selected_year}-1\\\\\\",\\\\\\"end_year\\\\\\":\\\\\\"{self.selected_year}\\\\\\",\\\\\\"end_month\\\\\\":\\\\\\"{self.selected_year}-12\\\\\\",\\\\\\"start_day\\\\\\":\\\\\\"{self.selected_year}-1-1\\\\\\",\\\\\\"end_day\\\\\\":\\\\\\"{self.selected_year}-12-31\\\\\\"}}\\"}}"}}'

        elif self.selected_type != "posts" and self.selected_year == "top":
             raw_filter = f'{{"rp_author":"{{\\"name\\":\\"location\\",\\"args\\":\\"{location_id}\\"}}"}}'

        else:
            raw_filter = f'{{"rp_author":"{{\\"name\\":\\"location\\",\\"args\\":\\"{location_id}\\"}}","rp_creation_time":"{{\\"name\\":\\"creation_time\\",\\"args\\":\\"{{\\\\\\"start_year\\\\\\":\\\\\\"{self.selected_year}\\\\\\",\\\\\\"start_month\\\\\\":\\\\\\"{self.selected_year}-1\\\\\\",\\\\\\"end_year\\\\\\":\\\\\\"{self.selected_year}\\\\\\",\\\\\\"end_month\\\\\\":\\\\\\"{self.selected_year}-12\\\\\\",\\\\\\"start_day\\\\\\":\\\\\\"{self.selected_year}-1-1\\\\\\",\\\\\\"end_day\\\\\\":\\\\\\"{self.selected_year}-12-31\\\\\\"}}\\"}}"}}'

        encoded_filter = encode(raw_filter)
        new_fb_url = FACEBOOK_BASE_URL + f"{self.selected_type}" + f"?q={self.keyword}" + f"&epa=FILTERS&filters={encoded_filter}"
        return new_fb_url

    def construct_url(self):
        id  = id_types.get().lower()
        if id == "user id":
            user_id = id_entry.get()
            self._capture_keyword_and_year()
            new_fb_url = self.construct_user_id(user_id)
            return new_fb_url

        elif id == "location id":
            location_id = id_entry.get()
            self._capture_keyword_and_year()
            new_fb_url = self.construct_location_id(location_id)
            return new_fb_url




def generate_url():
        selected_type = search_types.get().lower()
        if selected_type:
            fb_url = ConstructFbUrl(selected_type).construct_url()
            pyperclip.copy(fb_url)
            output_label.config(text=fb_url)
        return


def display_ids(event=None):

    id_types.set("")
    id_types.config(state="disabled")
    #id_entry.delete(0, tk.END)
    #id_entry.config(state="disabled")

    selected_type = search_types.get().lower()

    if selected_type == "posts"  or selected_type == "photos" \
        or selected_type == "videos":
        id_types.config(value=["User ID", "Location ID"], state="readonly")

        select_year.config(values=["Top", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"],
                           state="readonly")
        select_year.set("Top")

    elif selected_type == "profiles":
        id_types.config(values=["Employer ID", "City ID", "School ID"], state="readonly")
        profile_entry.config(state="normal")
        keyword_entry.delete(0, tk.END)
        keyword_entry.config(state="disabled")
        select_year.set("")
        select_year.config(state="disabled")

    elif selected_type == "events":
        id_types.config(values=["Location ID"], state="readonly")
        select_year.set("")
        select_year.config(state="disabled")

    else:
        id_types.config(state="disabled")

    return selected_type


def get_ids(event=None):
    selected_id = id_types.get().lower()

    if selected_id == "user id" or  selected_id == "location id":
        id_entry.config(state="normal")
        keyword_entry.config(state="normal")

    elif selected_id == "employer id" or selected_id == "city id" or selected_id == "school id":
        id_entry.config(state="normal")     
    
    else:
        id_entry.config(state="disabled")
    
    return



search_label = tk.Label(root, text="Search Type:")
search_label.grid(row=0, column=0, padx=10, pady=10)

search_types = ttk.Combobox(root,
                            values=["Posts", "Photos", "Videos", "Profiles", "Events", "Account Details"],
                            state="readonly")
search_types.grid(row=0, column=1, padx=10)
search_types.bind("<<ComboboxSelected>>", display_ids)

id_label = tk.Label(root, text="ID Type:")
id_label.grid(row=1, column=0, padx=10, pady=15)

id_types = ttk.Combobox(root, state="disabled")
id_types.grid(row=1, column=1, padx=10)
id_types.bind("<<ComboboxSelected>>", get_ids)

id_entry_label = tk.Label(root, text="Enter ID:")
id_entry_label.grid(row=1, column=2, padx=10)
id_entry = tk.Entry(root, state="disabled")
id_entry.grid(row=1, column=3, padx=10)

keyword_label = tk.Label(root, text="Keyword(s):")
keyword_label.grid(row=2, column=0, padx=10)
keyword_entry = tk.Entry(root, state="disabled")
keyword_entry.grid(row=2, column=1, padx=10)

profile_label = tk.Label(root, text="Profile Name:")
profile_label.grid(row=2, column=2, padx=10)
profile_entry = tk.Entry(root, state="disabled")
profile_entry.grid(row=2, column=3)

year_label = tk.Label(root, text="Year:")
year_label.grid(row=2, column=4, padx=10)
select_year = ttk.Combobox(root, state="disabled")
select_year.grid(row=2, column=5)


output_frame = tk.Frame(root)
output_frame.grid(row=4, column=0, columnspan=4, sticky="w", padx=10)
output_label = tk.Label(output_frame, wraplength=500, justify="left", anchor="w")
output_label.pack(fill="x")


display_ids()
get_ids()


generate_button = tk.Button(root,
                            text="Generate URL",
                            command=generate_url)
generate_button.grid(row=3, column=0, padx=20, pady=25)







root.geometry("800x300")
root.mainloop()