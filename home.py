# Home Page
import tkinter as tk
import re
import linecache

HEADER_FONT = re.sub('^.*?=', '', linecache.getline('config.txt' , 11)).strip()
PADX = re.sub('^.*?=', '', linecache.getline('config.txt', 2))
PADY = re.sub('^.*?=', '', linecache.getline('config.txt', 3))
BG = re.sub('^.*?=', '', linecache.getline('config.txt', 6)).strip()
FG = re.sub('^.*?=', '', linecache.getline('config.txt', 13)).strip()
BD = re.sub('^.*?=', '', linecache.getline('config.txt', 14)).strip()
RELIEF = re.sub('^.*?=', '', linecache.getline('config.txt', 15)).strip()


class Home():
    # USER ACCESS
    # Describe Software Information.
    def __init__(self, root, notebook):
        home_page = tk.Frame(notebook)
        notebook.add(home_page, text='Home')

        home_header = tk.Label(home_page, text='Welcome to the Library System!', font=HEADER_FONT)
        home_header.pack(fill=tk.X, side=tk.TOP)

        about_contacts = tk.Frame(home_page, bg=BG, relief=RELIEF, bd=BD)
        about_contacts.pack(fill=tk.X, side=tk.BOTTOM)

        software_info_container = tk.Frame(about_contacts, bg=BG, relief=RELIEF, bd=BD)
        software_info_container.pack(side=tk.LEFT, anchor=tk.W)

        author_client_info = tk.Label(software_info_container, text='Developed by Marco Fernandes\nfor Books4All Broadfield.', font=BG)
        author_client_info.pack(padx=PADX, pady=PADY)

        contact_info = tk.Label(software_info_container, text='Any Software Issues?\nContact the developer at marcoff2002@gmail.com\n\nQueries for the Library?\nContact the library at books4all.broadfield@gmail.com')
        contact_info.pack(padx=PADX, pady=PADY)

        updates_container = tk.Frame(home_page, bg=BG, relief=RELIEF, bd=BD)
        updates_container.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y, expand=True)

        events_container = tk.Frame(home_page, bg=BG, relief=RELIEF, bd=BD)
        events_container.pack(side=tk.LEFT, anchor=tk.CENTER, fill=tk.Y, expand=True)

        news_container = tk.Frame(home_page, bg=BG, relief=RELIEF, bd=BD)
        news_container.pack(side=tk.LEFT, anchor=tk.E, fill=tk.Y, expand=True)

        updates_header = tk.Label(updates_container, text='Updates', font=HEADER_FONT)
        updates_header.pack(padx=PADX, pady=PADY)

        events_header = tk.Label(events_container, text='Events', font=HEADER_FONT)
        events_header.pack(padx=PADX, pady=PADY)

        news_header = tk.Label(news_container, text='News', font=HEADER_FONT)
        news_header.pack(padx=PADX, pady=PADY)
