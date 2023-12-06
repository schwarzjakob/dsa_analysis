import tkinter as tk
from tkinter import filedialog
from shutil import copyfile
from datetime import datetime
import os
import json
import sys

# Assuming your script is in the parent directory of 'src/'
src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_dir)

import dsa_stats

# Global variables for widgets
upload_button = None
chatlog_menu = None
character_menu = None
category_menu = None
talent_menu = None
today = datetime.today().strftime('%y%m%d')
categories = ['talents']
category_var = None
talent_var = None

def center_window(root, width=300, height=200):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def load_users():
    with open('data/json/users.json', 'r') as file:
        users = json.load(file)
        return users["users"]


def upload_file():
    global upload_button, chatlog_menu
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        new_filename = f'{today}_chatlog.txt'
        new_filepath = os.path.join('data/chatlogs', new_filename)

        try:
            copyfile(filename, new_filepath)
            print("File copied to:", new_filepath)
            update_character_selection(load_users())
            # Hide the upload button and chatlog menu
            upload_button.pack_forget()
            chatlog_menu.pack_forget()
        except Exception as e:
            print(f"Error while copying file: {e}")

def on_chatlog_selected(*args):
    global upload_button, chatlog_menu
    selected_chatlog = chatlog_var.get()
    print(selected_chatlog)
    if selected_chatlog != "Select a Chatlog":
        chatlog_path = os.path.join('data/chatlogs', selected_chatlog)
        print("Selected chatlog:", chatlog_path)
        update_character_selection(load_users())
        # Hide the upload button and chatlog menu
        upload_button.pack_forget()
        chatlog_menu.grid(row = 0, column = 0, padx = 10, pady = 10)
    dsa_stats.DsaStats().main(selected_chatlog)

def get_chatlog_files():
    directory = 'data/chatlogs'
    return [f for f in os.listdir(directory) if f.endswith('.txt')]

def update_character_selection(characters):
    character_var.set("Select a Character")
    character_menu['menu'].delete(0, 'end')
    for character in characters:
        character_menu['menu'].add_command(label=character, command=tk._setit(character_var, character))
    character_menu.grid(row = 0, column = 0, padx = 10, pady = 10)

def on_character_selected(*args):
    selected_character = character_var.get()
    print("Selected character:", selected_character)
    update_category_selection()

def update_category_selection():
    category_var.set("Select a Category")
    category_menu['menu'].delete(0, 'end')
    for category in categories:
        category_menu['menu'].add_command(label=category, command=tk._setit(category_var, category))
    category_menu.grid(row = 1, column = 0, padx = 10, pady = 10)

def load_talents_from_json(category):
    with open('data/json/talents.json', 'r') as file:
        data = json.load(file)
        return data.get(category, [])

def on_category_selected(*args):
    selected_category = category_var.get()
    print("Selected category:", selected_category)
    talents = load_talents_from_json(selected_category)
    talent_var.set("Select a talent")
    talent_menu['menu'].delete(0, 'end')
    for talent in talents:
        talent_name = talent.get('talent') or talent.get('spell')  # assuming your JSON structure
        talent_menu['menu'].add_command(label=talent_name, command=tk._setit(talent_var, talent_name))
    talent_menu.grid(row = 2, column = 0, padx = 10, pady = 10)

def on_talent_selected(*args):
    selected_talent = talent_var.get()
    print("Selected talent:", selected_talent)
    # Add logic for talent selection here

root = tk.Tk()
root.title("DSA Chatlog Analysis")
center_window(root, 400, 300)

# File upload or select existing file
upload_button = tk.Button(root, text="Upload new Chatlog", command=upload_file)
upload_button.grid(row = 0, column = 0, padx = 10, pady = 10)

# Chatlog selection dropdown
chatlog_files = get_chatlog_files()
chatlog_var = tk.StringVar(root)
chatlog_var.set("Select an existing Chatlog")
chatlog_var.trace("w", on_chatlog_selected)
chatlog_menu = tk.OptionMenu(root, chatlog_var, *chatlog_files)
chatlog_menu.grid(row = 1, column = 0, padx = 10, pady = 10)

# Character selection
character_var = tk.StringVar(root)
character_var.trace("w", on_character_selected)
character_menu = tk.OptionMenu(root, character_var, "Select a Character")

# Create the category dropdown menu
category_var = tk.StringVar(root)
category_var.trace("w", on_category_selected)
category_menu = tk.OptionMenu(root, category_var, "Select a Category")

# Create the talent dropdown menu
talent_var = tk.StringVar(root)
talent_var.trace("w", on_talent_selected)
talent_menu = tk.OptionMenu(root, talent_var, "Select a Talent")

root.mainloop()
