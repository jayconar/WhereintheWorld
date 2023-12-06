from tkinter import Tk, Canvas, Button, PhotoImage, mainloop
import pandas as pd
from os import path
import textwrap
import random

BG = "#B1DDC6"
FONT = "Franklin Gothic Demi"
city = "Vienna"
state = "Austria"
cities_shown = set()

# Loading cities that have already been shown from a text file
try:
    with open("cities_shown.txt", "r") as file:
        cities_shown = set(line.strip() for line in file)
except FileNotFoundError:
    pass  # If the file doesn't exist, cities_shown will remain an empty set
data = pd.read_csv("data.csv")
screen = Tk()
screen.title("Where in the World")
screen.iconbitmap(path.abspath("art/icon.ico"))
screen.config(bg=BG, width=860, height=580, padx=37, pady=50)
card_front = PhotoImage(file=path.abspath("art/card_front.png"))
card_back = PhotoImage(file=path.abspath("art/card_back.png"))


def nxt():
    global city, state, data, cities_shown
    # Filtering the data to exclude cities already shown
    filtered_data = data[~data["City"].isin(cities_shown)]
    if not filtered_data.empty:
        city_row = random.choice(filtered_data.index)
        city = filtered_data.at[city_row, "City"]
        province = filtered_data.at[city_row, 'Subdivision']
        country = filtered_data.at[city_row, 'Country']
        # Text wrapping and formatting/adding comma
        state = textwrap.fill(f"{province + ', ' if pd.notna(province) else ''}{country}\n", width=28)
        canvas.itemconfig(display, text=city)
        canvas.itemconfig(title, text="Where in the world is")
        canvas.itemconfig(image, image=card_back)
        # Adding the newly shown city to the set
        cities_shown.add(city)

        # Saving the updated set of shown cities to the text file
        with open("cities_shown.txt", "w") as record:
            for name in cities_shown:
                record.writelines(f"{name}\n")


def answer():
    canvas.itemconfig(display, text=state)
    canvas.itemconfig(title, text=f"{city} is in")
    canvas.itemconfig(image, image=card_front)


canvas = Canvas(width=800, height=526, bg=BG, highlightthickness=0)
image = canvas.create_image(400, 263, image=card_back)
title = canvas.create_text(400, 72, text="Where in the world is", font=(FONT, 26))
display = canvas.create_text(400, 263, text=city, font=(FONT, 36, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

nxt()
answer_cl = Button(text="Answer", command=answer, width=18, bg="black", fg="white", font=(FONT, 18))
answer_cl.grid(column=1, row=1)
next_cl = Button(text="Next", command=nxt, width=18, bg="black", fg="white", font=(FONT, 18))
next_cl.grid(column=0, row=1)

mainloop()
