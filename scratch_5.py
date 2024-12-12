import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from tkinter.scrolledtext import ScrolledText


# Main Application Class
class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enhanced File Editor")
        self.minsize(width=600, height=400)
        self.maxsize(width=800, height=600)
        self.filename = None
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # ScrolledText Widget for Text Editing
        self.text = ScrolledText(self, wrap=tk.WORD, font=("Courier", 12), undo=True)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.bind("<KeyRelease>", self.on_key_release)

    def create_menu(self):
        # Menu bar with File Options
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save As", command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.text.edit_undo)
        editmenu.add_command(label="Redo", command=self.text.edit_redo)
        menubar.add_cascade(label="Edit", menu=editmenu)

        self.config(menu=menubar)

    def new_file(self):
        """Create a new file."""
        if self.confirm_unsaved_changes():
            self.text.delete(1.0, tk.END)
            self.filename = None
            self.title("Untitled - Enhanced File Editor")

    def open_file(self):
        """Open an existing file."""
        if self.confirm_unsaved_changes():
            file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                   filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, 'r', encoding="utf-8") as file:
                    content = file.read()
                    self.text.delete(1.0, tk.END)
                    self.text.insert(tk.END, content)
                    self.filename = file_path
                    self.title(f"{file_path} - Enhanced File Editor")

    def save_file(self):
        """Save the current file."""
        if self.filename is None:
            self.save_as()
        else:
            with open(self.filename, 'w', encoding="utf-8") as file:
                content = self.text.get(1.0, tk.END)
                file.write(content.rstrip())
            self.title(f"{self.filename} - Enhanced File Editor")

    def save_as(self):
        """Save the file with a new name."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.filename = file_path
            self.save_file()

    def confirm_unsaved_changes(self):
        """Ask the user to save before losing changes."""
        if self.text.get(1.0, tk.END).strip() != "" and self.filename:
            response = messagebox.askyesnocancel("Unsaved Changes",
                                                 "You have unsaved changes. Do you want to save them?")
            if response == None:
                return False
            elif response:
                self.save_file()
        return True

    def on_key_release(self, event):
        """Highlight syntax as text is typed."""
        self.syntax_highlight()

    def syntax_highlight(self):
        """Basic syntax highlighting for Python."""
        code = self.text.get(1.0, tk.END)

        # Clear previous tags
        self.text.tag_remove("keyword", 1.0, tk.END)
        self.text.tag_remove("string", 1.0, tk.END)

        keywords = ["def", "class", "import", "return", "if", "else", "for", "while", "try", "except"]
        strings = ['"', "'"]

        for keyword in keywords:
            start_idx = 1.0
            while True:
                start_idx = self.text.search(r'\b' + keyword + r'\b', start_idx, stopindex=tk.END)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(keyword)}c"
                self.text.tag_add("keyword", start_idx, end_idx)
                start_idx = end_idx

        # Highlight strings
        for string in strings:
            start_idx = 1.0
            while True:
                start_idx = self.text.search(string, start_idx, stopindex=tk.END)
                if not start_idx:
                    break
                end_idx = self.text.search(string, start_idx + "+1c", stopindex=tk.END)
                if not end_idx:
                    break
                self.text.tag_add("string", start_idx, end_idx)
                start_idx = end_idx

        self.text.tag_configure("keyword", foreground="blue", font=("Courier", 12, "bold"))
        self.text.tag_configure("string", foreground="green", font=("Courier", 12))


# Run the application
if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()
