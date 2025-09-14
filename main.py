import customtkinter as Ctk
import configparser
from tkinter import messagebox, simpledialog
from os import startfile

config = configparser.ConfigParser()

app = Ctk.CTk()
app.geometry("600x375")
app.title("Better Manager")

shortcutstitle = Ctk.CTkLabel(app, 100, 20, text="Shorcuts")
shortcutstitle.pack(pady=5, padx=5)
shortcutsgrid = Ctk.CTkScrollableFrame(app, 600, 20)
shortcutsgrid.pack(pady=10, padx=10, fill=None, expand=False)

utilstitle = Ctk.CTkLabel(app, 100, 20, text="Utilities")
utilstitle.pack(padx=5, pady=5)
addshortcutbtn = Ctk.CTkButton(app, 75, 20, text="Add/edit a shortcut", command=lambda: addShortcut())
addshortcutbtn.pack(padx=5, pady=5)
delshortcutbtn = Ctk.CTkButton(app, 75, 20, text="Delete a shortcut", command=lambda: delShortcut())
delshortcutbtn.pack(padx=5, pady=5)

def fixIni(msg="The ini file has a problem!\nWould you like to replace/create it?\n(If settings.ini exists, it will be replaced and all your settings will be lost!)"):
    try:
        if messagebox.askyesno("Better Manager", msg):
            config.clear()
            config.add_section("Shortcuts") 
            with open("settings.ini", "w") as file:
                config.write(file)

            loadShortcuts()

    except Exception as e:
        messagebox.showerror("Better Manager", "An error occured!\nError:\n", e)

def loadShortcuts():
    try:
        config.read("settings.ini")

        if not config.sections():
            fixIni()

        for btn in shortcutsgrid.winfo_children():
            btn.destroy()

        for i, shortcut in enumerate(config.items("Shortcuts")):
            try:
                Ctk.CTkButton(shortcutsgrid, 83, 20, text=shortcut[0], command=lambda path = shortcut[1]:startfile(path)).grid(row=i//6, column=i%6, pady=5, padx=5)
            except FileNotFoundError:
                messagebox.showwarning("Better Manager", "The path to the shortcut you are trying to open does not exist!")

    except FileNotFoundError:
        fixIni("The settings.ini file does not exist!\nWould you like to create it?")
    except Exception as e:
        messagebox.showerror("Better Manager", "An error occured!\nError:\n", e)

def addShortcut():
    try:
        name = simpledialog.askstring("Better Manager", "What would you like to name the shortcut?")
        if not name: return
        path = simpledialog.askstring("Better Manager", "What is the path to the shortcut?")
        if not path: return

        config["Shortcuts"][name] = path
        with open("settings.ini", "w") as file:
                config.write(file)
        messagebox.showinfo("Better Manager", "Succesfully added/edited shorcut!")
        loadShortcuts()
    except Exception as e:
        messagebox.showerror("Better Manager", "An error occured!\nError:\n", e)

def delShortcut():
    try:
        name = simpledialog.askstring("Better Manager", "What is the name of the shortcut you would like to delete?")
        if not name: return
        if not config.has_option("Shortcuts", name): return messagebox.showwarning("Better Manager", "That shortcut doesn't exist!")

        config.remove_option("Shortcuts", name)

        with open("settings.ini", "w") as file:
                config.write(file)
        messagebox.showinfo("Better Manager", "Succesfully deleted shorcut!")
        loadShortcuts()
    except Exception as e:
        messagebox.showerror("Better Manager", "An error occured!\nError:\n", e)

if __name__ == "__main__":
    loadShortcuts()
    app.mainloop()
