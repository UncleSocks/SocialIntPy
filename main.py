import base64
import tkinter as tk
from tkinter import ttk
import pyperclip
from urllib.parse import quote


fb_url_base = "https://www.facebook.com/search/"


def encode(filter_string):
    string_bytes = filter_string.encode('ascii')
    baase64_bytes = base64.b64encode(string_bytes)
    base64_string = baase64_bytes.decode('ascii')
    return base64_string



def userid_url_const(type, user_id, query, selected_year):

    if not query:
        query = type
    else:
        query = quote(query)

    if selected_year == "top":
        raw_filter = f'{{"rp_author":"{{\\"name\\":\\"author\\",\\"args\\":\\"{user_id}\\"}}"}}'
    
    else:
        raw_filter = f'{{"rp_author":"{{\\"name\\":\\"author\\",\\"args\\":\\"{user_id}\\"}}","rp_creation_time":"{{\\"name\\":\\"creation_time\\",\\"args\\":\\"{{\\\\\\"start_year\\\\\\":\\\\\\"{selected_year}\\\\\\",\\\\\\"start_month\\\\\\":\\\\\\"{selected_year}-1\\\\\\",\\\\\\"end_year\\\\\\":\\\\\\"{selected_year}\\\\\\",\\\\\\"end_month\\\\\\":\\\\\\"{selected_year}-12\\\\\\",\\\\\\"start_day\\\\\\":\\\\\\"{selected_year}-1-1\\\\\\",\\\\\\"end_day\\\\\\":\\\\\\"{selected_year}-12-31\\\\\\"}}\\"}}"}}'


    encoded_filter = encode(raw_filter)
    print(encoded_filter)
    new_fb_url = fb_url_base + f"{type}" + f"?q={query}" + f"&epa=FILTERS&filters={encoded_filter}"
    return new_fb_url

def locationid_url_const(type, loc_id, query, selected_year):

    if not query:
        query = type
    else:
        query = quote(query)

    if type=="posts" and selected_year == "top":
        raw_filter = f'{{"rp_location":"{{\\"name\\":\\"location\\",\\"args\\":\\"{loc_id}\\"}}"}}'
    elif type == "posts" and selected_year != "top":
        raw_filter = f'{{"rp_location":"{{\\"name\\":\\"location\\",\\"args\\":\\"{loc_id}\\"}}","rp_creation_time":"{{\\"name\\":\\"creation_time\\",\\"args\\":\\"{{\\\\\\"start_year\\\\\\":\\\\\\"{selected_year}\\\\\\",\\\\\\"start_month\\\\\\":\\\\\\"{selected_year}-1\\\\\\",\\\\\\"end_year\\\\\\":\\\\\\"{selected_year}\\\\\\",\\\\\\"end_month\\\\\\":\\\\\\"{selected_year}-12\\\\\\",\\\\\\"start_day\\\\\\":\\\\\\"{selected_year}-1-1\\\\\\",\\\\\\"end_day\\\\\\":\\\\\\"{selected_year}-12-31\\\\\\"}}\\"}}"}}'
    
    elif type != "posts" and selected_year == "top":
        raw_filter = f'{{"rp_author":"{{\\"name\\":\\"location\\",\\"args\\":\\"{loc_id}\\"}}"}}'
    else:
        raw_filter = f'{{"rp_author":"{{\\"name\\":\\"location\\",\\"args\\":\\"{loc_id}\\"}}","rp_creation_time":"{{\\"name\\":\\"creation_time\\",\\"args\\":\\"{{\\\\\\"start_year\\\\\\":\\\\\\"{selected_year}\\\\\\",\\\\\\"start_month\\\\\\":\\\\\\"{selected_year}-1\\\\\\",\\\\\\"end_year\\\\\\":\\\\\\"{selected_year}\\\\\\",\\\\\\"end_month\\\\\\":\\\\\\"{selected_year}-12\\\\\\",\\\\\\"start_day\\\\\\":\\\\\\"{selected_year}-1-1\\\\\\",\\\\\\"end_day\\\\\\":\\\\\\"{selected_year}-12-31\\\\\\"}}\\"}}"}}'

    encoded_filter = encode(raw_filter)
    print(encoded_filter)
    new_fb_url = fb_url_base + f"{type}" + f"?q={query}" + f"&epa=FILTERS&filters={encoded_filter}"
    return new_fb_url
    

def button_clicked():
    selected_item = combo_box.get()
    selected_item = selected_item.lower()

    selected_id = id_combo_box.get()
    selected_id = selected_id.lower()

    id = id_entry.get()
    query = query_entry.get()
    selected_year = year_combo_box.get()
    selected_year = selected_year.lower()
    if selected_id == "user id":
        fb_url_filter = userid_url_const(selected_item, id, query, selected_year)
    else:
        fb_url_filter = locationid_url_const(selected_item, id, query, selected_year)

    pyperclip.copy(fb_url_filter)
    label.config(text=fb_url_filter)


root = tk.Tk()
root.title("SocMed OSINT Helper")

label = tk.Label(root, text="Selected Option: ")
label.pack(pady=10)

button = tk.Button(root,
                   text="Generate",
                   command=button_clicked,
                   width=25)

button.pack(side="bottom", padx=(5,20), pady=(10,50))

combo_box = ttk.Combobox(root, values=["Posts", "Photos", "Videos", "Profiles", "Events"], state="readonly")
combo_box.pack(padx=(5,20), pady=(10,50))
combo_box.set("Posts")

id_combo_box = ttk.Combobox(root, values=["User ID", "Location ID"], state="readonly")
id_combo_box.pack(padx=(5,25), pady=(10,50))
id_combo_box.set("User ID")

id_label = tk.Label(root, text="ID: ")
id_label.pack(padx=(5,20), pady=(20,50))
id_entry = tk.Entry(root)
id_entry.pack(padx=(10,20), pady=(20,50))

query_label = tk.Label(root, text="Keyword: ")
query_label.pack()
query_entry = tk.Entry(root)
query_entry.pack(padx=(10,20), pady=(20,50))

year_label = tk.Label(root, text="Year:")
year_label.pack()
year_combo_box = ttk.Combobox(root, values=["Top", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"])
year_combo_box.pack()
year_combo_box.set("Top")

root.mainloop()