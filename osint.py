import base64
import tkinter as tk
from tkinter import ttk
import pyperclip
from urllib.parse import quote


root = tk.Tk()
root.title("Social Media Intelligence Filter-inator")


FACEBOOK_BASE_URL = "https://www.facebook.com/"
FACEBOOK_BASE_SEARCH_URL = "https://www.facebook.com/search/"
UNAME_INFORMATION_MAP = {
    "timeline":"",
    "about":"about",
    "employment":"about?section=work",
    "education":"about?section=education",
    "locations":"about?section=living",
    "contact info":"about?section=contact-info",
    "basic info":"about?section=basic-info",
    "relationships":"about?section=relationships",
    "family":"about?section=family",
    "biography":"about?section=bio",
    "life events":"about?section=year-overview",
    "friends":"friends",
    "following":"following",
    "photos":"photos",
    "photos albums":"photos_albums",
    "videos":"videos",
    "reels":"reels",
    "check-ins":"places_visited",
    "visits":"map",
    "recent check-ins":"places_recent",
    "sports":"sports",
    "music":"music",
    "movies":"movies",
    "tv":"tv",
    "books":"books",
    "apps & games":"games",
    "likes":"likes",
    "events":"events",
    "facts":"did_you_know",
    "reviews":"reviews",
    "reviews given":"reviews_given",
    "reviews written":"reviews_written",
    "notes":"notes"
}



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

    def construct_user_url(self, user_id=None):
        
        if not user_id:
            output = "Unable to generate URL. Enter a user ID."
            return output

        if self.selected_year == "top":
            raw_filter = f'{{"rp_author":"{{\\"name\\":\\"author\\",\\"args\\":\\"{user_id}\\"}}"}}'
        else:
            raw_filter = f'{{"rp_author":"{{\\"name\\":\\"author\\",\\"args\\":\\"{user_id}\\"}}","rp_creation_time":"{{\\"name\\":\\"creation_time\\",\\"args\\":\\"{{\\\\\\"start_year\\\\\\":\\\\\\"{self.selected_year}\\\\\\",\\\\\\"start_month\\\\\\":\\\\\\"{self.selected_year}-1\\\\\\",\\\\\\"end_year\\\\\\":\\\\\\"{self.selected_year}\\\\\\",\\\\\\"end_month\\\\\\":\\\\\\"{self.selected_year}-12\\\\\\",\\\\\\"start_day\\\\\\":\\\\\\"{self.selected_year}-1-1\\\\\\",\\\\\\"end_day\\\\\\":\\\\\\"{self.selected_year}-12-31\\\\\\"}}\\"}}"}}'
        
        encoded_filter = encode(raw_filter)
        new_fb_url = FACEBOOK_BASE_SEARCH_URL + f"{self.selected_type}" + f"?q={self.keyword}" + f"&epa=FILTERS&filters={encoded_filter}"
        return new_fb_url
    
    def construct_location_url(self, location_id=None):
        
        if not location_id:
            output = "Unable to generate URL. Enter a location ID."
            return output

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
        new_fb_url = FACEBOOK_BASE_SEARCH_URL + f"{self.selected_type}" + f"?q={self.keyword}" + f"&epa=FILTERS&filters={encoded_filter}"
        return new_fb_url
    
    def construct_people_url(self, id, profile_id):
        profile_map = {
            "employer id":{"filter":"employer", "name":"users_employer"}, 
            "city id":{"filter":"city", "name":"users_location"}, 
            "school id":{"filter":"school", "name":"users_school"}
            }
        
        raw_filter = f'{{"{profile_map[id]["filter"]}":"{{\\"name\\":\\"{profile_map[id]["name"]}\\",\\"args\\":\\"{profile_id}\\"}}"}}'
        encoded_filter = encode(raw_filter)
        new_fb_url = FACEBOOK_BASE_SEARCH_URL + f"people/?q={self.keyword}" + f"&epa=FILTERS&filters={encoded_filter}"
        return new_fb_url
    
    def construct_places_url(self):
        new_fb_url = FACEBOOK_BASE_SEARCH_URL + f"places/?q={self.keyword}" 
        return new_fb_url
    
    def construct_username_url(self, username):
        information = uname_information.get().lower()
        if not information:
            output = "Select user information to search"
            return output
        else:
            new_fb_url = FACEBOOK_BASE_URL + f"{username}/" + f"{UNAME_INFORMATION_MAP[information]}"
            return new_fb_url
        

    def construct_url(self):
        id = id_types.get().lower()
        username = username_entry.get().lower()
        if id == "user id":
            user_id = id_entry.get()
            self._capture_keyword_and_year()
            new_fb_url = self.construct_user_url(user_id)
            return new_fb_url

        elif id == "location id":
            location_id = id_entry.get()
            self._capture_keyword_and_year()
            new_fb_url = self.construct_location_url(location_id)
            return new_fb_url
        
        elif id == "employer id" or id == "city id" or id == "school id":
            profile_id = id_entry.get()
            self._capture_keyword_and_year()
            new_fb_url = self.construct_people_url(id, profile_id)
            return new_fb_url
        
        elif username:
            new_fb_url = self.construct_username_url(username)
            return new_fb_url
        
        elif self.selected_type == "places":
            self._capture_keyword_and_year()
            new_fb_url = self.construct_places_url()
            return new_fb_url





def generate_url():
        output_label.config(text="")
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

        select_year.config(state="readonly")
        select_year.set("Top")

        #profile_entry.delete(0, tk.END)
        #profile_entry.config(state="disabled")
        
        username_entry.delete(0, tk.END)
        username_entry.config(state="disabled")
        
        uname_information.set("")
        uname_information.config(state="disabled")

    elif selected_type == "people":
        id_types.config(values=["Employer ID", "City ID", "School ID"], state="readonly")
        #profile_entry.config(state="normal")
        keyword_entry.config(state="normal")
        select_year.set("")
        select_year.config(state="disabled")

    elif selected_type == "places":
        keyword_entry.config(state="normal")
        id_types.set("")
        id_types.config(state="disabled")
        
        select_year.set("")
        select_year.config(state="disabled")
        
        username_entry.delete(0, tk.END)
        username_entry.config(state="disabled")
        
        uname_information.set("")
        uname_information.config(state="disabled")

    elif selected_type == "events":
        id_types.config(values=["Location ID"], state="readonly")
        select_year.set("")
        select_year.config(state="disabled")

        #profile_entry.delete(0, tk.END)
        #profile_entry.config(state="disabled")
        
        username_entry.delete(0, tk.END)
        username_entry.config(state="disabled")
        
        uname_information.set("")
        uname_information.config(state="disabled")

    elif selected_type == "user info":
        username_entry.config(state="normal")
        uname_information.config(state="readonly")
        id_entry.delete(0, tk.END)
        id_entry.config(state="disabled")
        keyword_entry.delete(0, tk.END)
        keyword_entry.config(state="disabled")
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
                            values=["Posts", "Photos", "Videos", "People", "Places", "Events", "User Info", "Search"],
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

#profile_label = tk.Label(root, text="Profile Name:")
#profile_label.grid(row=2, column=2, padx=10)
#profile_entry = tk.Entry(root, state="disabled")
#profile_entry.grid(row=2, column=3)

year_label = tk.Label(root, text="Year:")
year_label.grid(row=2, column=2, padx=10)
select_year = ttk.Combobox(root, values=["Top", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"],state="disabled")
select_year.grid(row=2, column=3)

username_label = tk.Label(root, text="Username:")
username_label.grid(row=3, column=0, padx=10, pady=15)
username_entry = tk.Entry(root, state="disabled")
username_entry.grid(row=3, column=1)

uname_information_label = tk.Label(root, text="Information:")
uname_information_label.grid(row=3, column=2, padx=10)
uname_information = ttk.Combobox(root,
                                 values=["Timeline", "About", "Employment", 
                                         "Education", "Locations", "Contact Info",
                                         "Basic Info", "Relationships", "Family",
                                         "Biography", "Life Events", "Friends",
                                         "Following", "Photos", "Photos Albums",
                                         "Videos", "Reels", "Check-ins", "Visits",
                                         "Recent Check-ins", "Sports", "Music",
                                         "Movies", "TV", "Books", "Apps & Games",
                                         "Likes", "Events", "Facts", "Reviews",
                                         "Reviews Given", "Reviews Written", "Notes"],
                                         state="disabled")
uname_information.grid(row=3, column=3)


output_frame = tk.Frame(root)
output_frame.grid(row=5, column=0, columnspan=4, sticky="w", padx=10)
output_label = tk.Label(output_frame, wraplength=500, justify="left", anchor="w")
output_label.pack(fill="x")


display_ids()
get_ids()


generate_button = tk.Button(root,
                            text="Generate URL",
                            command=generate_url)
generate_button.grid(row=4, column=0, padx=20, pady=25)







root.geometry("600x300")
root.mainloop()