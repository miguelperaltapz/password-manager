from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------------- COLORS ------------------------------------- #
BLACK = "#1B1A17"
GRAY = "#73777B"
ORANGE = "#D4483B"
WHITE = "#F1EEE9"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate_password():
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops:(", message="Please don't leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"There are the details entered : \nEmail: {email} "
                                                              f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                with open("passwords.json", "r") as file:
                    # Reading old data
                    data = json.load(file)
            except FileNotFoundError:
                with open("passwords.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("passwords.json", "w") as file:
                    # Saving updated data
                    json.dump(data, file, indent=4)
            finally:
                website_input.delete(0, "end")
                email_input.delete(0, "end")
                password_input.delete(0, "end")

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    website = website_input.get()
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg=BLACK)

canvas = Canvas(width=200, height=200, bg=BLACK, highlightthickness=0)

image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", bg=BLACK, fg=WHITE)
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:", bg=BLACK, fg=WHITE)
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", bg=BLACK, fg=WHITE)
password_label.grid(column=0, row=3)

# Entries
website_input = Entry(width=21, bg=GRAY)
website_input.grid(column=1, row=1, sticky="EW")
website_input.focus()
email_input = Entry(width=35, bg=GRAY)
email_input.grid(column=1, row=2, columnspan=2, sticky="EW")
password_input = Entry(width=21, bg=GRAY)
password_input.grid(column=1, row=3, sticky="EW")

# Buttons
generate_pass = Button(text="Generate Password", command=generate_password, bg=BLACK, fg=WHITE)
generate_pass.grid(column=2, row=3, sticky="EW")
add_button = Button(text="Add", width=36, command=save_password, bg=BLACK, fg=WHITE)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")
search_button = Button(text="Search", command=find_password, bg=BLACK, fg=WHITE)
search_button.grid(column=2, row=1, sticky="EW")

window.mainloop()
