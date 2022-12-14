"""
source:
https://www.youtube.com/watch?v=YXPyB4XeYLA&t=18272s
https://www.thepythoncode.com/article/text-editor-using-tkinter-python
https://stackoverflow.com/questions/44798950/how-to-display-a-dataframe-in-tkinter
"""

import tkinter
from pathlib import Path
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
import ctypes

import pandas as pd

from pandastable import Table, TableModel, config

database_path = "J:/my_dayli_targets_app/database.csv"

main_txt_file_path = "J:/my_dayli_targets_app/main.txt"
robota_txt_file_path = "J:/my_dayli_targets_app/robota.txt"
praca_txt_file_path = "J:/my_dayli_targets_app/praca.txt"
ksiazki_txt_file_path = "J:/my_dayli_targets_app/ksiazki.txt"


file_types = [("Text Files", "*.txt"), ("Markdown", "*.md")]
app_name = "my dayli targets app"
no_file_opened_string = "New File"


def main_file_drop_down_handeler(action):
    global main_txt_file_path
    # Opening a File
    if action == "open":
        file = filedialog.askopenfilename(filetypes=file_types)
        root.title(app_name + " - " + file)
        main_txt_file_path = file
        with open(file, "r") as f:
            txt.delete(1.0, tkinter.END)
            txt.insert(tkinter.INSERT, f.read())
    # Making a new File
    elif action == "new":
        main_txt_file_path = no_file_opened_string
        txt.delete(1.0, tkinter.END)
        root.title(app_name + " - " + main_txt_file_path)
        # Saving a file
    elif action == "save" or action == "saveAs":
        if main_txt_file_path == no_file_opened_string or action == "save_as":
            main_txt_file_path = filedialog.asksaveasfilename(filetypes=file_types)
        with open(main_txt_file_path, "w+") as f:
            f.write(txt.get("1.0", "end"))
        root.title(app_name + " - " + main_txt_file_path)


def autosave():
    main_file_drop_down_handeler("save")
    root.after(10000, autosave)


def text_change(event):
    root.title(app_name + " - *" + main_txt_file_path)


def robota_window():
    top = tkinter.Toplevel()
    top.title("robota_window")
    my_frame = tkinter.LabelFrame(top, text="dupa frame", padx=5, pady=5)
    my_frame.pack(padx=5, pady=5)


def praca_window():
    top = tkinter.Toplevel()
    top.title("praca_window")
    my_frame = tkinter.LabelFrame(top, text="dupa frame", padx=5, pady=5)
    my_frame.pack(padx=5, pady=5)


def ksiazki_window():
    top = tkinter.Toplevel()
    top.title("ksiazki_window")
    my_frame = tkinter.LabelFrame(top, text="dupa frame", padx=5, pady=5)
    my_frame.pack(padx=5, pady=5)


def historia_window():
    top = tkinter.Toplevel()
    top.title("historia_window")
    top.geometry("1000x600+200+100")
    df = load_database()
    pt = Table(top, dataframe=df, showtoolbar=True, showstatusbar=True)
    # set some options
    options = {"colheadercolor": "green", "floatprecision": 5}
    config.apply_options(options, pt)
    pt.show()


def nagroda_window():
    top = tkinter.Toplevel()
    top.title("nagroda_window")
    my_frame = tkinter.LabelFrame(top, text="dupa frame", padx=5, pady=5)
    my_frame.pack(padx=5, pady=5)


def save_dayli_data():
    global database_path
    data_dict = {
        "date": pd.Timestamp.now().to_period("D"),
        "cele": int(cele_var.get()),
        "praca_pomodorow_inna": praca_pomodorow_inna_var.get(),
        "szybkie_pisanie": szybkie_pisanie_var.get(),
        "space_repetition": space_repetition_var.get(),
        "medytacja": medytacja_var.get(),
        "cwiczenia": cwiczenia_var.get(),
        "rozciaganie": rozciaganie_var.get(),
        "czytanie_programowanie": czytanie_programowanie_var.get(),
        "czytanie_doskonalenie": czytanie_doskonalenie_var.get(),
    }
    # load db
    database = pd.read_csv(database_path)
    to_day_database = database[
        database["date"] == str(pd.Timestamp.now().to_period("D"))
    ]
    database = database[database["date"] != str(pd.Timestamp.now().to_period("D"))]
    # fill empty values
    if to_day_database.empty:
        return
    to_day_database_dict = to_day_database.to_dict("records")[0]
    new_data_dict = {}
    for key, data_value in data_dict.items():
        if data_value == 0 or data_value == "":
            if to_day_database_dict[key]:
                new_data_dict[key] = to_day_database_dict[key]
        else:
            new_data_dict[key] = data_value
    to_day_df = pd.DataFrame(pd.Series(new_data_dict)).T
    # save df
    database = pd.concat([database, to_day_df])
    database.to_csv(database_path, index=False)


def load_dayli_data():
    global database_path
    database = pd.read_csv(database_path)
    to_day_database = database[
        database["date"] == str(pd.Timestamp.now().to_period("D"))
    ]
    if to_day_database.empty:
        return {}
    return to_day_database.to_dict("records")[0]


def load_database():
    global database_path
    return pd.read_csv(database_path)


def load_txt_path(txt_path):
    txt_output = ""
    with open(txt_path) as f:
        lines = f.readlines()
    for line in lines:
        txt_output += line
    return txt_output


root = tkinter.Tk()
dayli_data = load_dayli_data()
root.title("main app window")
root.geometry("900x550")
my_frame = tkinter.LabelFrame(root, padx=5, pady=5)
my_frame.pack(padx=5, pady=5)
my_frame.grid(row=0, column=0)
# scrollbar = tkinter.Scrollbar(root)
# scrollbar.grid(row = 0, column = 1, sticky = tkinter.NS)
# Text Area
txt = tkinter.scrolledtext.ScrolledText(my_frame)
txt.grid(row=0, column=0, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
# Bind event in the widget to a function
txt.bind("<KeyPress>", text_change)
# return saved state
txt.insert(tkinter.INSERT, load_txt_path(main_txt_file_path))
# Menu
menu = tkinter.Menu(root)
file_dropdown = tkinter.Menu(menu, tearoff=False)
# Add Commands and and their callbacks
file_dropdown.add_command(
    label="New", command=lambda: main_file_drop_down_handeler("new")
)
file_dropdown.add_command(
    label="Open", command=lambda: main_file_drop_down_handeler("open")
)
# Adding a seperator between button types.
file_dropdown.add_separator()
file_dropdown.add_command(
    label="Save", command=lambda: main_file_drop_down_handeler("save")
)
file_dropdown.add_command(
    label="Save as", command=lambda: main_file_drop_down_handeler("saveAs")
)
menu.add_cascade(label="File", menu=file_dropdown)
# Set Menu to be Main Menu
root.config(menu=menu)

side_frame = tkinter.LabelFrame(my_frame, text="dzia??y")
side_frame.grid(row=0, column=1)
buttom1 = tkinter.Button(
    side_frame, text="robota", command=robota_window, bg="blue", fg="white"
)
buttom1.grid(row=1, column=0)
buttom2 = tkinter.Button(side_frame, text="praca", command=praca_window, bg="green")
buttom2.grid(row=2, column=0)
buttom3 = tkinter.Button(side_frame, text="ksiazki", command=ksiazki_window, bg="green")
buttom3.grid(row=3, column=0)
buttom4 = tkinter.Button(side_frame, text="histora", command=historia_window)
buttom4.grid(row=4, column=0)
buttom5 = tkinter.Button(side_frame, text="nagrody", command=nagroda_window, bg="red")
buttom5.grid(row=5, column=0)

dayli_task_frame = tkinter.LabelFrame(my_frame, text="codziennie")
dayli_task_frame.grid(row=0, column=2)

cele_var = tkinter.IntVar(value=dayli_data.get("cele", 0))
txt_cele = tkinter.Checkbutton(
    dayli_task_frame,
    text="spr ogolnych celi",
    variable=cele_var,
).grid(row=0, column=0)

praca_pomodorow_inna_label = tkinter.Label(
    dayli_task_frame, text="praca pomodorow inna"
).grid(row=1, column=0)
praca_pomodorow_inna_var = tkinter.StringVar(
    value=dayli_data.get("praca_pomodorow_inna", "")
)
txt_praca_pomodorow_inna = tkinter.Entry(
    dayli_task_frame, textvariable=praca_pomodorow_inna_var
).grid(row=2, column=0)

szybkie_pisanie_label = tkinter.Label(dayli_task_frame, text="szybkie pisanie").grid(
    row=3, column=0
)
szybkie_pisanie_var = tkinter.StringVar(value=dayli_data.get("szybkie_pisanie", ""))
txt_szybkie_pisanie = tkinter.Entry(
    dayli_task_frame, textvariable=szybkie_pisanie_var
).grid(row=4, column=0)

space_repetition_label = tkinter.Label(dayli_task_frame, text="space repetition").grid(
    row=5, column=0
)
space_repetition_var = tkinter.StringVar(value=dayli_data.get("space_repetition", ""))
txt_space_repetition = tkinter.Entry(
    dayli_task_frame, textvariable=space_repetition_var
).grid(row=6, column=0)

medytacja_label = tkinter.Label(dayli_task_frame, text="medytacja").grid(
    row=7, column=0
)
medytacja_var = tkinter.StringVar(value=dayli_data.get("medytacja", ""))
txt_medytacja = tkinter.Entry(dayli_task_frame, textvariable=medytacja_var).grid(
    row=8, column=0
)

cwiczenia_label = tkinter.Label(dayli_task_frame, text="cwiczenia").grid(
    row=9, column=0
)
cwiczenia_var = tkinter.StringVar(value=dayli_data.get("cwiczenia", ""))
txt_cwiczenia = tkinter.Entry(dayli_task_frame, textvariable=cwiczenia_var).grid(
    row=10, column=0
)

rozciaganie_label = tkinter.Label(dayli_task_frame, text="rozciaganie").grid(
    row=11, column=0
)
rozciaganie_var = tkinter.StringVar(value=dayli_data.get("rozciaganie", ""))
txt_rozciaganie = tkinter.Entry(dayli_task_frame, textvariable=rozciaganie_var).grid(
    row=12, column=0
)

czytanie_programowanie_label = tkinter.Label(
    dayli_task_frame, text="czytanie programowanie"
).grid(row=13, column=0)
czytanie_programowanie_var = tkinter.StringVar(
    value=dayli_data.get("czytanie_programowanie", "")
)
txt_czytanie_programowanie = tkinter.Entry(
    dayli_task_frame, textvariable=czytanie_programowanie_var
).grid(row=14, column=0)

czytanie_doskonalenie_label = tkinter.Label(
    dayli_task_frame, text="doskonalenie czytanie/przerobienie"
).grid(row=15, column=0)
czytanie_doskonalenie_var = tkinter.StringVar(
    value=dayli_data.get("czytanie_doskonalenie", "")
)
txt_czytanie_doskonalenie = tkinter.Entry(
    dayli_task_frame, textvariable=czytanie_doskonalenie_var
).grid(row=16, column=0)

buttom6 = tkinter.Button(
    dayli_task_frame, text="zapisz", command=save_dayli_data, bg="green"
)
buttom6.grid(row=20, column=0)


autosave()
root.mainloop()
