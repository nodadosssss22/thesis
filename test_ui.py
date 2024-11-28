import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from tkinter.font import Font
from tkinter import ttk  # Import ttk

# IDE REGION

class SimpleIDE:
    def __init__(self, root, mode = "light"):

        self.root = root  # root is now the Tk instance

        # Editor
        self.editor = tk.Text(root, wrap=tk.WORD, font=("Consolas", 12), undo=True, bg="#FF0000", fg="#FF0000")
        self.editor.pack(fill=tk.BOTH, expand=1)
        self.editor.bind("<KeyRelease>", self.on_key_release)
        self.editor.bind("<Tab>", self.auto_complete)

        # Button Frame
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X)

        # Buttons
        self.open_button = tk.Button(self.button_frame, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.run_button = tk.Button(self.button_frame, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.mode = mode

        def switch_to_dark():
            self.editor.config(bg="#1e1e1e", fg="white", insertbackground="#ffffff")
            self.mode = "dark"
            self.setup_syntax_tags()
            self.apply_syntax_highlighting()

        def switch_to_light():
            self.editor.config(bg="#ffffff", fg="#000000", insertbackground="#000000")
            self.mode = "light"
            self.setup_syntax_tags()
            self.apply_syntax_highlighting()

        # Buttons for theme switching
        tk.Button(self.button_frame, text="Dark Mode", command=switch_to_dark).pack(side=tk.RIGHT, padx=10)
        tk.Button(self.button_frame, text="Light Mode", command=switch_to_light).pack(side=tk.RIGHT, padx=10)

        # Output
        self.output = scrolledtext.ScrolledText(root, height=6, wrap=tk.WORD, font=("Consolas", 12), bg="#f4f4f4")
        self.output.pack(fill=tk.BOTH, expand=1)
        self.output.config(state=tk.DISABLED)

        # Syntax Highlighting Tags
        self.setup_syntax_tags()

    def setup_syntax_tags(self):
        """Define syntax highlighting tags with appropriate fonts."""
        # Create a font for italic style (used for comments)
        italic_font = Font(self.editor, self.editor.cget("font"))
        italic_font.configure(slant="italic")

        # Syntax Highlighting Tags
        if self.mode == "light":
            self.editor.tag_configure("Keyword", foreground="blue")
            self.editor.tag_configure("String", foreground="green")
            self.editor.tag_configure("Comment", foreground="grey", font=italic_font)
        elif self.mode == "dark":
            self.editor.tag_configure("Keyword", foreground="#008080")
            self.editor.tag_configure("String", foreground="green")
            self.editor.tag_configure("Comment", foreground="orange", font=italic_font)

    def apply_syntax_highlighting(self, event=None):
        """Apply syntax highlighting to the editor's content."""
        text = self.editor.get("1.0", tk.END)
        self.editor.mark_set("range_start", "1.0")
        self.editor.mark_set("range_end", tk.END)
        self.editor.tag_remove("Keyword", "1.0", tk.END)
        self.editor.tag_remove("String", "1.0", tk.END)
        self.editor.tag_remove("Comment", "1.0", tk.END)
        self.editor.tag_remove("Default", "1.0", tk.END)

        for token, content in lex(text, PythonLexer()):
            start = self.editor.index("range_start")
            end = f"{start}+{len(content)}c"
            if token in Token.Keyword:
                self.editor.tag_add("Keyword", start, end)
            elif token in Token.Literal.String:
                self.editor.tag_add("String", start, end)
            elif token in Token.Comment:
                self.editor.tag_add("Comment", start, end)
            else:
                self.editor.tag_add("Default", start, end)
            self.editor.mark_set("range_start", end)

    def auto_complete(self, event):
        """Handle basic auto-completion for Python keywords."""
        current_line = self.editor.get("insert linestart", "insert lineend")
        cursor_index = self.editor.index("insert").split(".")[-1]
        prefix = current_line[:int(cursor_index)]
        suggestions = [kw for kw in self.keywords if kw.startswith(prefix)]

        if suggestions:
            self.editor.delete("insert linestart", "insert")
            self.editor.insert("insert", suggestions[0])
        return "break"  # Prevent the tab key's default action

    def on_key_release(self, event):
        """Trigger syntax highlighting on key release."""
        self.apply_syntax_highlighting()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", code)
            self.apply_syntax_highlighting()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.editor.get("1.0", tk.END))

    def run_code(self):
        code = self.editor.get("1.0", tk.END)
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        try:
            result = subprocess.run(["python", "-c", code], capture_output=True, text=True)
            self.output.insert(tk.END, result.stdout)
            self.output.insert(tk.END, result.stderr)
        except Exception as e:
            self.output.insert(tk.END, str(e))
        self.output.config(state=tk.DISABLED)

# GENERAL UI REGION

def create_ui():
    root = tk.Tk()
    root.title("")
    root.geometry("1500x500")
    root.configure(bg="#d9d9d9")

    # Style configuration using ttk
    style = ttk.Style()
    style.configure("TButton", background="#FF0000", foreground="white", font=("Arial", 12, "bold"), padding=10)
    style.map("TButton", background=[("active", "#2d302d")], foreground=[("active", "white")])

    style.configure("TLabel", background="#FF0000", foreground="white", font=("Arial", 12))
    style.configure("TFrame", background="#FF0000")

    # Window size
    window_width = 975
    window_height = 700

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    position_top = int(screen_height / 7 - window_height / 7)
    position_left = int(screen_width / 2 - window_width / 2)

    # Set the window geometry to center it
    root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
    
    root.configure(bg="#FF0000")

    # Sidebar
    sidebar = tk.Frame(root, width=100, bg="white", relief="raised", bd=0)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar Content
    tk.Label(sidebar, text="E-Learning System", bg="white", font=("Montserrat", 12, "bold")).pack(pady=10)

    # Profile Picture Placeholder (Round)
    profile_canvas = tk.Canvas(sidebar, width=100, height=100, bg="#bbb", bd=0, highlightthickness=0)
    profile_canvas.pack(pady=10)

    tk.Label(sidebar, text="Your Name", bg="white", font=("Arial", 12)).pack()

    # Using ttk.Button for styled buttons
    ttk.Button(sidebar, text="Edit", style="TButton").pack(pady=(10, 10))

    import ttkbootstrap as ttkb

    # Style configuration for the buttons
    style = ttkb.Style()
    style.configure(
        "Custom.TButton",
        font=("Roboto", 11, "bold"),
        background="white",
        foreground="black",
        borderwidth = 0,
        anchor = "w"
    )
    style.configure(
        "Custom.Highlighted.TButton",
        font=("Roboto", 11, "bold"),
        background="#008080",
        foreground="black",
        borderwidth = 0.5,
        anchor = "w"
    )

    style.configure(
        "Custom.TFrame",  # Style name
        background="white",  # Background color
        bordercolor="#1ABC9C",  # Border color
        borderwidth=0,  # Border width
    )

    # Button container (use Frame instead of Canvas)
    button_framer = ttkb.Frame(sidebar, style="Custom.TFrame", bootstyle="secondary")
    button_framer.pack(side="top", pady=5, padx=10, fill="x")

    button_frame = ttkb.Frame(button_framer, style="Custom.TFrame", bootstyle="secondary")
    button_frame.pack(side="left", pady=5, padx=10, fill="x")

    global previous_button
    global current_button

    current_button = None
    previous_button = None

    def on_button_click(button):
        global previous_button
        global current_button

        print (button)

        current_button = button

        button.config(style = "Custom.Highlighted.TButton")

        if previous_button:
            try:
                previous_button.config(style = "Custom.TButton")
            finally:
                print()

        if (previous_button != button):
            if str(button) == ".!frame.!frame.!frame.!button":
                print("Examination")

            if str(button) == ".!frame.!frame.!frame.!button2":
                print("Evaluation")

        previous_button = button

    # Initialize the SimpleIDE frame
    ide_frame = tk.Frame(content_area, bg="white")
    ide = SimpleIDE(root, content_area)  # Create SimpleIDE instance here

    # Function to switch to IDE view
    def show_ide():
        ide_frame.pack(fill=tk.BOTH, expand=True)  # Show the IDE frame
        ide.apply_syntax_highlighting()  # Apply highlighting, if necessary

    # Function to hide the IDE frame when switching to other sections
    def hide_ide():
        ide_frame.pack_forget()  # Hide the IDE frame

    # Add buttons with the custom style
    button0 = ttkb.Button(
        button_frame, text="Examination", style="Custom.TButton", width=17,command=lambda: on_button_click(button0)
    )
    button0.pack(pady=15, padx=5)

    button1 = ttkb.Button(
        button_frame, text="Evaluation", style="Custom.TButton", width=17,command=lambda: on_button_click(button1)
    )
    button1.pack(pady=15, padx=5)

    button2 = ttkb.Button(
        button_frame, text="Feedback", style="Custom.TButton", width=17,command=lambda: on_button_click(button2)
    )
    button2.pack(pady=15, padx=5)

    on_button_click(button0)

    # Log Out Button
    ttk.Button(sidebar, text="Log out", style="TButton", width=10).pack(side=tk.BOTTOM, pady=5, padx=10)

    # Main Content Area (IDE will go here)
    content_area = tk.Frame(root, bg="#FF0000")
    content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Initialize SimpleIDE in the content area

    SimpleIDE(root)

    # ide = SimpleIDE(root)  # Pass root, not content_area

    root.mainloop()

create_ui()