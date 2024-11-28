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
    def __init__(self, root, content_area, mode="light"):
        self.root = root  # root is now the Tk instance
        self.content_area = content_area  # Pass the content_area for frame swapping
        self.mode = mode

        self.frame = tk.Frame(content_area, bg="white")  # Create a frame for IDE
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Editor
        self.editor = tk.Text(self.frame, wrap=tk.WORD, font=("Consolas", 12), undo=True, bg="white", fg="black")
        self.editor.pack(fill=tk.BOTH, expand=1)
        self.editor.bind("<KeyRelease>", self.on_key_release)
        self.editor.bind("<Tab>", self.auto_complete)

        # Button Frame
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(fill=tk.X)

        # Buttons
        self.open_button = tk.Button(self.button_frame, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.run_button = tk.Button(self.button_frame, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)

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
        self.output = scrolledtext.ScrolledText(self.frame, height=6, wrap=tk.WORD, font=("Consolas", 12), bg="#f4f4f4")
        self.output.pack(fill=tk.BOTH, expand=1)
        self.output.config(state=tk.DISABLED)

        # Syntax Highlighting Tags
        self.setup_syntax_tags()

    def setup_syntax_tags(self):
        """Define syntax highlighting tags with appropriate fonts."""
        italic_font = Font(self.editor, self.editor.cget("font"))
        italic_font.configure(slant="italic")

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
    root.configure(bg="#f4f4f4")

    # Style configuration using ttk
    style = ttk.Style()
    style.configure("TButton", background="white", foreground="black", font=("Montserrat", 11, "bold"), pady=20,padx=30)
    style.map("TButton", background=[("active", "white")], foreground=[("active", "white")])

    style.configure("TLabel", background="#f4f4f4", foreground="black", font=("Arial", 12))
    style.configure("TFrame", background="#f4f4f4")

    # Window size
    window_width = 975
    window_height = 625
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 7 - window_height / 7)
    position_left = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
    
    root.configure(bg="#f4f4f4")

    # Sidebar
    sidebar = tk.Frame(root, width=500, bg="white", relief="raised", bd=0)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar Content
    tk.Label(sidebar, text="E-Learning System", bg="white", font=("Montserrat", 10, "bold")).pack(pady=10)

    # Profile Picture Placeholder (Round)
    profile_canvas = tk.Canvas(sidebar, width=100, height=100, bg="#bbb", bd=0, highlightthickness=0)
    profile_canvas.pack(pady=10)

    tk.Label(sidebar, text="Your Name", bg="white", font=("Arial", 12)).pack()

    # Using ttk.Button for styled buttons
    ttk.Button(sidebar, text="Edit", style="TButton").pack(pady=(10, 10))

    

    # Button container for different sections
    button_frame = ttk.Frame(sidebar,)
    button_frame.pack(side="top", pady=7, padx=10, fill="x")

    # Function for switching between frames
    def show_frame(frame):

        for widget in content_area.winfo_children():
            widget.pack_forget()
        frame.pack(fill=tk.BOTH, expand=True)

        if str(frame) == ".!frame2.!frame":
            SimpleIDE(root, content_area)

    # Button to switch frames
    button_ide = ttk.Button(button_frame, text="Examination", style="TButton", command=lambda: show_frame(ide_frame))
    button_ide.pack(pady=12,fill=tk.X)

    button_exam = ttk.Button(button_frame, text="Evaluation", style="TButton", command=lambda: show_frame(eval_frame))
    button_exam.pack(pady=12,fill=tk.X)

    button_eval = ttk.Button(button_frame, text="Feedback", style="TButton", command=lambda: show_frame(feed_frame))
    button_eval.pack(pady=12,fill=tk.X)

    # Frame container for main content
    content_area = tk.Frame(root, bg="white")
    content_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Frame for IDE
    ide_frame = tk.Frame(content_area, bg="white")
    ide_frame.pack(fill=tk.X, pady=2)

    # Frame for Examination
    exam_frame = tk.Frame(content_area, bg="white")
    exam_label = tk.Label(exam_frame, text="This is the Examination Frame", font=("Arial", 18))
    exam_label.pack()

    # Frame for Examination
    eval_frame = tk.Frame(content_area, bg="white")
    eval_label = tk.Label(eval_frame, text="This is the Evaluation Frame", font=("Arial", 18))
    eval_label.pack()

    # Frame for Evaluation
    feed_frame = tk.Frame(content_area, bg="white")
    feed_label = tk.Label(feed_frame, text="This is the Feedback Frame", font=("Arial", 18))
    feed_label.pack()

    root.mainloop()

create_ui()