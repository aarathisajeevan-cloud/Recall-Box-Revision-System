import customtkinter as ctk
from tkinter import messagebox

from django.core.serializers import python
from api_client import start_revision_session

def handle_start_revision():

    # Temporary test IDs
    user_id = 1
    topic_id = 1

    result = start_revision_session(user_id, topic_id)

    if "error" in result:
        messagebox.showerror(
            "Error",
            str(result["error"])
        )

    else:
        session_id = result["session"]["session_id"]

        messagebox.showinfo(
            "Success",
            f"Revision session started!\nSession ID: {session_id}"
        )
# ---------------- CONFIGURATION ----------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("RecallBox | Smart Revision System")
app.geometry("1200x750")
app.minsize(1000, 650)

# Colours
BG = "#F7F7FC"
SIDEBAR = "#FFFFFF"
PURPLE = "#6957D8"
LIGHT_PURPLE = "#EEEAFE"
TEXT = "#25243A"
MUTED = "#85849A"
WHITE = "#FFFFFF"

app.configure(fg_color=BG)

# ---------------- SIDEBAR ----------------

sidebar = ctk.CTkFrame(
    app,
    width=230,
    corner_radius=0,
    fg_color=SIDEBAR
)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

logo = ctk.CTkLabel(
    sidebar,
    text="✦ RecallBox",
    font=("Arial", 25, "bold"),
    text_color=PURPLE
)
logo.pack(pady=(35, 45))

menu_items = [
    "Dashboard",
    "Start Revision",
    "My Subjects",
    "Revision Schedule",
    "Revision History",
    "Analytics"
]

for item in menu_items:

    active = item == "Start Revision"

    button = ctk.CTkButton(
        sidebar,
        text="   " + item,
        height=45,
        corner_radius=10,
        anchor="w",
        fg_color=LIGHT_PURPLE if active else SIDEBAR,
        hover_color=LIGHT_PURPLE,
        text_color=PURPLE if active else MUTED,
        font=("Arial", 14, "bold" if active else "normal"),
        command=lambda name=item: show_page(name)
    )
    button.pack(fill="x", padx=18, pady=5)

# ---------------- MAIN CONTENT ----------------

main = ctk.CTkFrame(
    app,
    fg_color=BG,
    corner_radius=0
)
main.pack(side="left", fill="both", expand=True, padx=30, pady=25)


def clear_main():
    for widget in main.winfo_children():
        widget.destroy()


def show_page(page_name):

    clear_main()

    heading = ctk.CTkLabel(
        main,
        text=page_name,
        font=("Arial", 30, "bold"),
        text_color=TEXT
    )
    heading.pack(anchor="w", pady=(15, 5))

    subtitle = ctk.CTkLabel(
        main,
        text="Manage your learning and improve your memory.",
        font=("Arial", 14),
        text_color=MUTED
    )
    subtitle.pack(anchor="w", pady=(0, 25))

    if page_name == "Start Revision":
        show_revision_home()

    else:
        placeholder = ctk.CTkLabel(
            main,
            text=f"{page_name} page coming soon!",
            font=("Arial", 18),
            text_color=MUTED
        )
        placeholder.pack(pady=100)


def show_revision_home():

    # Welcome Card
    welcome = ctk.CTkFrame(
        main,
        fg_color=PURPLE,
        corner_radius=18,
        height=180
    )
    welcome.pack(fill="x", pady=(0, 25))
    welcome.pack_propagate(False)

    ctk.CTkLabel(
        welcome,
        text="Ready to strengthen your memory?",
        font=("Arial", 23, "bold"),
        text_color=WHITE
    ).pack(anchor="w", padx=25, pady=(20, 8))

    ctk.CTkLabel(
        welcome,
        text="Small revisions today lead to better learning tomorrow.",
        font=("Arial", 14),
        text_color="#E8E3FF"
    ).pack(anchor="w", padx=25)

    # Start Revision Button
    ctk.CTkButton(
        welcome,
        text="Start Revision",
        fg_color="#FFFFFF",
        text_color=PURPLE,
        hover_color="#E8E3FF",
        command=handle_start_revision
    ).pack(anchor="w", padx=25, pady=12)

    # Statistics
    stats = ctk.CTkFrame(
        main,
        fg_color="transparent"
    )
    stats.pack(fill="x", pady=5)

    cards = [
        ("Questions", "120", "Total questions"),
        ("Accuracy", "85%", "Overall performance"),
        ("Topics Due", "08", "Need revision"),
    ]

    for title, value, description in cards:

        card = ctk.CTkFrame(
            stats,
            fg_color=WHITE,
            corner_radius=15,
            height=125
        )
        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7
        )
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 14),
            text_color=MUTED
        ).pack(anchor="w", padx=18, pady=(15, 3))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 27, "bold"),
            text_color=PURPLE
        ).pack(anchor="w", padx=18)

        ctk.CTkLabel(
            card,
            text=description,
            font=("Arial", 11),
            text_color=MUTED
        ).pack(anchor="w", padx=18)


# ---------------- START APPLICATION ----------------

show_page("Start Revision")

app.mainloop()

def handle_start_revision():

    # Temporary test IDs
    user_id = 1
    topic_id = 1

    result = start_revision_session(user_id, topic_id)

    if "error" in result:
        messagebox.showerror(
            "Error",
            str(result["error"])
        )

    else:
        session_id = result["session"]["session_id"]

        messagebox.showinfo(
            "Success",
            f"Revision session started!\nSession ID: {session_id}"
        )