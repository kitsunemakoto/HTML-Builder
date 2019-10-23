import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from os import path, listdir


class Builder:
    def __init__(self, master):
        self.master = master
        #self.master.geometry("320x180")
        self.master.title("HTML/CSS Builder")

        self.checkBootstrap = IntVar()
        self.checkBootstrap.set(0)

        tk.Label(self.master, text="Welcome to KM's HTML/CSS Builder", fg="black", font="Arial 12 bold").grid(row=0, column=0)

        ttk.Separator(self.master, orient=HORIZONTAL).grid(row=1, column=0, columnspan=2, pady=15.0, sticky=NSEW)

        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=2, column=0, sticky=NSEW)
        self.page1 = tk.Frame(self.notebook)
        self.page2 = tk.Frame(self.notebook)
        self.notebook.add(self.page1, text="HTML")
        self.notebook.add(self.page2, text="CSS")

        ###                           ###
        ### -  -  - HTML PAGE -  -  - ###
        ###                           ###

        tk.Label(self.page1, text="HTML Filename:", fg="black", font="Arial 10 bold").grid(row=0, column=0, sticky=W)
        tk.Label(self.page1, text=".html", fg="black", font="Arial 10").grid(row=0, column=2, sticky=W)
        tk.Label(self.page1, text="HTML Title:", fg="black", font="Arial 10 bold").grid(row=1, column=0, sticky=W)

        self.HTMLName_TextBox = tk.Entry(self.page1, width=18, bg="white")
        self.HTMLName_TextBox.grid(row=0, column=1, sticky=E)
        self.HTMLTitle_TextBox = tk.Entry(self.page1, width=22, bg="white")
        self.HTMLTitle_TextBox.grid(row=1, column=1)

        tk.Button(self.page1, text="Create HTML", width=13, bg="darkblue", fg="white", command=self.CreateHTML).grid(row=2, column=0, columnspan=3, sticky=EW)

        ###                           ###
        ###  -  -  - CSS PAGE -  -  - ###
        ###                           ###

        tk.Label(self.page2, text="CSS Filename:", fg="black", font="Arial 10 bold").grid(row=0, column=0, sticky=W)
        tk.Label(self.page2, text=".css", fg="black", font="Arial 10").grid(row=0, column=2, sticky=W)
        tk.Label(self.page2, text="(Optional) Link this to:", fg="black", font="Arial 10 bold").grid(row=1, column=0, sticky=W)

        self.CSSName_TextBox = tk.Entry(self.page2, width=18, bg="white")
        self.CSSName_TextBox.grid(row=0, column=1, sticky=E)

        self.LinkToHTML_listbox = Listbox(self.page2, selectmode=SINGLE)
        self.LinkToHTML_listbox.grid(row=1, column=1, sticky=W)

        for file in listdir("."):
            if file.endswith(".html"):
                self.LinkToHTML_listbox.insert(END, file)

        self.bootstrap_Checkbox = Checkbutton(self.page2, variable=self.checkBootstrap, onvalue=1, offvalue=0, text="Use Bootstrap 4?")
        self.bootstrap_Checkbox.grid(row=2, column=0, sticky=W)

        tk.Button(self.page2, text="Create CSS", width=13, bg="darkblue", fg="white", command=self.CreateCSS).grid(row=3, column=0, columnspan=3, sticky=EW)


    def CreateHTML(self):
        html_str = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>%s</title>
    </head>
    <body>
        <p>Test HTML file. :)</p>
    </body>
</html>""" % (self.HTMLTitle_TextBox.get())

        if not path.isfile("%s.html" % (self.HTMLName_TextBox.get())):
            with open("%s.html" % (self.HTMLName_TextBox.get()), "w") as f:
                f.write(html_str)
        else:
            with open("%s.html" % (self.HTMLName_TextBox.get()), "a") as f:
                f.write(html_str)

        self.LinkToHTML_listbox.insert(END, "%s" % ("%s.html" % (self.HTMLName_TextBox.get())))
        tk.messagebox.showinfo("KM's HTML/CSS Builder", "All done!", parent=self.master)


    def CreateCSS(self):
        css_str = """p{
    color: red;
    font-size: large;
}"""

        if not path.isfile("%s.css" % (self.CSSName_TextBox.get())):
            with open("%s.css" % (self.CSSName_TextBox.get()), "w") as f:
                f.write(css_str)
        else:
            with open("%s.css" % (self.CSSName_TextBox.get()), "a") as f:
                f.write(css_str)

        if self.LinkToHTML_listbox.curselection():
            self.LinkCSSToHTML()
            print("Used")
        else:
            pass


    def LinkCSSToHTML(self):
        with open(self.LinkToHTML_listbox.get(self.LinkToHTML_listbox.curselection()), "r", encoding='utf-8') as in_file:
            buf = in_file.readlines()

        with open(self.LinkToHTML_listbox.get(self.LinkToHTML_listbox.curselection()), "w", encoding='utf-8') as out_file:
            for line in buf:
                if line.startswith("        <title>"):
                    print("found")
                    line = line + """        <link href="%s.css" rel="stylesheet" />\n""" % (self.CSSName_TextBox.get())
                out_file.write(line)
            tk.messagebox.showinfo("KM's HTML/CSS Builder", "CSS linked!", parent=self.master)

        if self.checkBootstrap.get() == 1:
            print("Active, wants Bootstrap")
            self.LinkBootStrapToCSS()


    def LinkBootStrapToCSS(self):
        with open(self.LinkToHTML_listbox.get(self.LinkToHTML_listbox.curselection()), "r", encoding='utf-8') as in_file:
            buf = in_file.readlines()

        with open(self.LinkToHTML_listbox.get(self.LinkToHTML_listbox.curselection()), "w", encoding='utf-8') as out_file:
            for line in buf:
                if line.startswith("""        <link href="%s.css" rel="stylesheet" />\n""" % (self.CSSName_TextBox.get())):
                    line = line + """        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">\n"""
                if line.startswith("    </body>"):
                    line = """        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    </body>\n"""
                out_file.write(line)

            tk.messagebox.showinfo("KM's HTML/CSS Builder", "Bootstrap added!", parent=self.master)


if __name__ == "__main__":
    root = tk.Tk()
    app = Builder(root)
    root.mainloop()