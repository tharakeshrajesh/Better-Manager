import customtkinter as Ctk
import configparser
from tkinter import messagebox

config = configparser.ConfigParser()

app = Ctk.CTk()
app.geometry("600x200")
app.title("Better Manager")

def checkIni():

    def fixIni(msg="The ini file has a problem!\nWould you like to replace/create it?\n(If settings.ini exists, it will be replaced and all your settings will be lost!)"):
        if messagebox.askyesno("Better Manager", msg):
            config.add_section("Startup")
            with open("settings.ini", "w") as file:
                config.write(file)
    try:
        config.read("settings.ini")

        if not config.sections():
            fixIni()
    except FileNotFoundError:
        fixIni("The settings.ini file does not exist!\nWould you like to create it?")

def startup():
    checkIni()
    # some other startup stuff here later
    

if __name__ == "__main__":
    startup()
    app.mainloop()
