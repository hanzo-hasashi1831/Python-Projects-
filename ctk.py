import customtkinter as ctk
from tkinter import filedialog, font

class AllPhoebe(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AllPhoebe Text Editor")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.menu_frame = ctk.CTkFrame(self, fg_color='#2b2b2b', height=30)
        self.menu_frame.place(x=0, y=0, relwidth=1)

        self.file_menu_btn = ctk.CTkOptionMenu(self.menu_frame, values=["New", "Open", "Save", "Exit"], command=self.file_menu_action, width=60, height=25)
        self.file_menu_btn.set("File")
        self.file_menu_btn.pack(side='left', padx=2, pady=2)

        self.edit_menu_btn = ctk.CTkOptionMenu(self.menu_frame, values=["Undo", "Redo", "Cut", "Copy", "Paste", "Select All"], command=self.edit_menu_action, width=60, height=25)
        self.edit_menu_btn.set("Edit")
        self.edit_menu_btn.pack(side='left', padx=2, pady=2)

        self.format_menu_btn = ctk.CTkOptionMenu(self.menu_frame, values=["Word Wrap", "Font"], command=self.format_menu_action, width=80, height=25)
        self.format_menu_btn.set("Format")
        self.format_menu_btn.pack(side='left', padx=2, pady=2)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=1, padx=10, pady=(40, 10))  # Adjusted for menu height

        self.text_area = ctk.CTkTextbox(self.main_frame, wrap='word', undo=True, fg_color='#1e1e1e', text_color='#dcdcdc')
        self.text_area.grid(row=0, column=0, sticky='nsew')

        self.scrollbar = ctk.CTkScrollbar(self.main_frame, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def file_menu_action(self, choice):
        actions = {
            "New": self.new_file,
            "Open": self.open_file,
            "Save": self.save_file,
            "Exit": self.quit
        }
        if choice in actions:
            actions[choice]()

    def edit_menu_action(self, choice):
        actions = {
            "Undo": self.text_area.edit_undo,
            "Redo": self.text_area.edit_redo,
            "Cut": lambda: self.text_area.event_generate("<<Cut>>"),
            "Copy": lambda: self.text_area.event_generate("<<Copy>>"),
            "Paste": lambda: self.text_area.event_generate("<<Paste>>"),
            "Select All": lambda: self.text_area.event_generate("<<SelectAll>>")
        }
        if choice in actions:
            actions[choice]()

    def format_menu_action(self, choice):
        if choice == "Word Wrap":
            self.toggle_word_wrap()
        elif choice == "Font":
            self.choose_font()

    def new_file(self):
        self.text_area.delete(1.0, "end")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, "end")
                self.text_area.insert("end", file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, "end"))

    def toggle_word_wrap(self):
        wrap_mode = 'word' if self.text_area.cget('wrap') == 'none' else 'none'
        self.text_area.configure(wrap=wrap_mode)

    def choose_font(self):
        font_window = ctk.CTkToplevel(self)
        font_window.title("Choose Font")
        font_window.geometry("300x200")

        font_families = list(font.families())
        font_listbox = ctk.CTkComboBox(font_window, values=font_families)
        font_listbox.pack(pady=10)

        def apply_font():
            selected_font = font_listbox.get()
            self.text_area.configure(font=(selected_font, 12))
            font_window.destroy()

        ctk.CTkButton(font_window, text="Apply", command=apply_font).pack(pady=10)

if __name__ == "__main__":
    app = AllPhoebe()
    app.mainloop()
