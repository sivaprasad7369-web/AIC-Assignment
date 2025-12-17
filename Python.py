from owlready2 import get_ontology
from tkinter import * # type: ignore
from tkinter import ttk
from tkinter import messagebox

# Load the ontology
try:
    ontology_file = "MathAreaTutorOntology.owl"
    ontology = get_ontology(ontology_file).load()
except Exception as e:
    messagebox.showerror("Ontology Load Error", f"Could not load ontology: {e}\nPlease ensure '{ontology_file}' is in the same directory.") # type: ignore
    exit()

# =============================================================
# DARK THEME COLORS
# =============================================================
BG_DARK = "#1E1E1E"           # Main background
BG_CARD = "#2A2A2A"           # Frame background
BG_LIST = "#2F2F2F"           # Listbox background
FG_TEXT = "#E6E6E6"           # Primary text
FG_DIM = "#A6A6A6"            # Secondary text
ACCENT = "#4DA3FF"            # Accent blue
ACCENT_HOVER = "#1E8CFF"      # Hover blue

# =============================================================
# FUNCTIONS
# =============================================================
def fetch_classes():
    listbox.delete(0, "end")
    if not ontology.classes():
        listbox.insert("end", "No classes found in the ontology.")
        return
    for i, cls in enumerate(ontology.classes()): # type: ignore
        listbox.insert("end", f"Class: {cls.name}")

def fetch_individuals():
    listbox.delete(0, "end")
    if not ontology.individuals():
        listbox.insert("end", "No individuals found in the ontology.")
        return
    for i, individual in enumerate(ontology.individuals()): # type: ignore
        listbox.insert("end", f"Individual: {individual.name}")

def fetch_object_properties():
    listbox.delete(0, "end")
    if not ontology.object_properties():
        listbox.insert("end", "No object properties found in the ontology.")
        return
    for i, prop in enumerate(ontology.object_properties()): # type: ignore
        listbox.insert("end", f"Object Property: {prop.name}")

def fetch_data_properties():
    listbox.delete(0, "end")
    if not ontology.data_properties():
        listbox.insert("end", "No data properties found in the ontology.")
        return
    for i, prop in enumerate(ontology.data_properties()): # type: ignore
        listbox.insert("end", f"Data Property: {prop.name}")

def search_ontology():
    query = search_var.get().lower().strip()
    listbox.delete(0, "end")

    if not query:
        messagebox.showwarning("Search Error", "Please enter a search term.")
        return

    found = False

    def add(type_name, name): # type: ignore
        nonlocal found
        listbox.insert("end", f"{type_name}: {name}")
        found = True

    for cls in ontology.classes():
        if query in cls.name.lower():
            add("Class", cls.name)
    for ind in ontology.individuals():
        if query in ind.name.lower():
            add("Individual", ind.name)
    for prop in ontology.object_properties():
        if query in prop.name.lower():
            add("Object Property", prop.name)
    for prop in ontology.data_properties():
        if query in prop.name.lower():
            add("Data Property", prop.name)

    if not found:
        listbox.insert("end", f"No results found for '{query}'.")


# =============================================================
# GUI SETUP
# =============================================================
root = Tk()
root.title("Math Ontology Explorer - Dark Edition")
root.geometry("1000x750")
root.configure(bg=BG_DARK)

style = ttk.Style()
style.theme_use("clam")

# Global styling
style.configure("TFrame", background=BG_DARK)
style.configure("TLabel", background=BG_DARK, foreground=FG_TEXT)
style.configure("TButton",
                font=("Segoe UI", 12, "bold"),
                background=ACCENT,
                foreground="white",
                padding=8)

style.map("TButton",
          background=[("active", ACCENT_HOVER)],
          foreground=[("active", "white")])

style.configure("TEntry",
                fieldbackground=BG_CARD,
                foreground=FG_TEXT,
                padding=6,
                bordercolor="#444444",
                borderwidth=1)

# =============================================================
# HEADER
# =============================================================
header_frame = ttk.Frame(root)
header_frame.pack(fill=X, pady=(10, 15))

header_label = ttk.Label(header_frame,
                         text="Math Ontology Explorer",
                         font=("Segoe UI", 28, "bold"),
                         foreground=ACCENT,
                         background=BG_DARK)
header_label.pack()

# =============================================================
# SEARCH BAR
# =============================================================
search_frame = ttk.Frame(root)
search_frame.pack(fill=X, padx=20, pady=10)

search_var = StringVar()
search_entry = ttk.Entry(search_frame, textvariable=search_var, width=50)
search_entry.pack(side=LEFT, expand=True, fill=X, padx=(0, 10))

search_button = ttk.Button(search_frame, text="Search", command=search_ontology)
search_button.pack(side=LEFT)

# =============================================================
# BUTTON PANEL
# =============================================================
button_frame = ttk.Frame(root)
button_frame.pack(fill=X, padx=20, pady=10)

button_frame.columnconfigure((0, 1, 2, 3), weight=1)

ttk.Button(button_frame, text="Show Classes", command=fetch_classes).grid(row=0, column=0, padx=8, pady=8, sticky="ew")
ttk.Button(button_frame, text="Show Individuals", command=fetch_individuals).grid(row=0, column=1, padx=8, pady=8, sticky="ew")
ttk.Button(button_frame, text="Show Object Properties", command=fetch_object_properties).grid(row=0, column=2, padx=8, pady=8, sticky="ew")
ttk.Button(button_frame, text="Show Data Properties", command=fetch_data_properties).grid(row=0, column=3, padx=8, pady=8, sticky="ew")

# =============================================================
# RESULTS LISTBOX
# =============================================================
results_frame = ttk.Frame(root)
results_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

scrollbar = Scrollbar(results_frame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(results_frame,
                  yscrollcommand=scrollbar.set,
                  font=("Segoe UI", 13),
                  bg=BG_LIST,
                  fg=FG_TEXT,
                  relief="flat",
                  selectbackground=ACCENT,
                  selectforeground="white")
listbox.pack(fill=BOTH, expand=True)

scrollbar.config(command=listbox.yview) # type: ignore

# =============================================================
# FOOTER
# =============================================================
footer_frame = ttk.Frame(root)
footer_frame.pack(fill=X, pady=10)

footer_label = ttk.Label(
    footer_frame,
    text="© 2025 Math Ontology Explorer | Dark Mode Edition",
    font=("Segoe UI", 10),
    foreground=FG_DIM
)
footer_label.pack()

# =============================================================
# RUN
# =============================================================
root.mainloop()
