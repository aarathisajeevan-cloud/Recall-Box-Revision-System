
import customtkinter as ctk
from tkinter import messagebox
from api_client import start_revision_session, get_questions, save_answer_attempt, complete_revision_session
from my_subjects_ui import show_my_subjects
import time



# ---------------- REVISION FUNCTIONS ----------------

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

# revsion mode popup

def show_revision_mode_popup():

    popup = ctk.CTkToplevel(app)
    popup.title("Choose Revision Mode")
    popup.geometry("400x350")
    popup.resizable(False, False)
    popup.grab_set()

    ctk.CTkLabel(
        popup,
        text="Choose Your Revision Mode",
        font=("Arial", 22, "bold"),
        text_color=TEXT
    ).pack(pady=(25, 10))

    ctk.CTkLabel(
        popup,
        text="How would you like to revise today?",
        font=("Arial", 13),
        text_color=MUTED
    ).pack(pady=5)

    ctk.CTkButton(
        popup,
        text="Smart Revision",
        height=45,
        fg_color=PURPLE,
        command=lambda: select_revision_mode("SCHEDULED", popup)
    ).pack(fill="x", padx=35, pady=10)

    ctk.CTkButton(
        popup,
        text="Topic Practice",
        height=45,
        fg_color=PURPLE,
        command=lambda: select_revision_mode("TOPIC_PRACTICE", popup)
    ).pack(fill="x", padx=35, pady=10)

    ctk.CTkButton(
        popup,
        text="Mixed Revision",
        height=45,
        fg_color=PURPLE,
        command=lambda: select_revision_mode("MIXED", popup)
    ).pack(fill="x", padx=35, pady=10)

#select revision mode

def select_revision_mode(mode, popup):

    popup.destroy()

    if mode == "TOPIC_PRACTICE":
        from my_subjects_ui import show_subjects_for_practice

        show_subjects_for_practice(main, start_topic_practice)
        return

    # Select subject and topic for other modes
    from my_subjects_ui import show_subjects_for_practice

    show_subjects_for_practice(
        main,
        lambda topic_id: start_selected_revision(topic_id, mode)
    )

# Start Smart Revision and Mixed Revision
def start_selected_revision(topic_id, mode):

    user_id = 1

    # Create revision session
    result = start_revision_session(
        user_id,
        topic_id,
        mode
    )

    if "error" in result:
        messagebox.showerror("Error", str(result["error"]))
        return

    session_id = result["session"]["session_id"]

    # Get questions for selected topic
    question_result = get_questions(topic_id)

    if "error" in question_result:
        messagebox.showerror("Error", str(question_result["error"]))
        return

    questions = question_result.get("questions", [])

    if not questions:
        messagebox.showinfo(
            "No Questions",
            "No questions available for this topic."
        )
        return

    # Display questions
    show_question_screen(
        questions,
        session_id,
        mode
    )

    
# Start Topic Practice
def start_topic_practice(topic_id):

    user_id = 1
    mode = "TOPIC_PRACTICE"

    # Create revision session
    result = start_revision_session(
        user_id,
        topic_id,
        mode
    )

    if "error" in result:
        messagebox.showerror("Error", str(result["error"]))
        return

    session_id = result["session"]["session_id"]

    # Retrieve questions for selected topic
    question_result = get_questions(topic_id)

    if "error" in question_result:
        messagebox.showerror(
            "Error",
            str(question_result["error"])
        )
        return

    questions = question_result.get("questions", [])

    if not questions:
        messagebox.showinfo(
            "No Questions",
            "No questions available for this topic."
        )
        return

    # Open question screen
    show_question_screen(
        questions,
        session_id,
        mode
    )

# Fetch questions and show question screen
def show_question_screen(questions, session_id, mode):

    if not questions:
        messagebox.showinfo(
            "No Questions",
            "No questions are available for this revision."
        )
        show_page("Start Revision")
        return

    current_index = 0
    score = 0
    total_questions = len(questions)

    question_start_time = time.time()
    user_id = 1  # Temporary test user ID

    selected_answer = ctk.StringVar(value="")

    def clear_main():
        for widget in main.winfo_children():
            widget.destroy()

    # DISPLAY QUESTION
    def display_question():

        nonlocal question_start_time

        clear_main()

        question = questions[current_index]

        selected_answer.set("")
        question_start_time = time.time()

        ctk.CTkLabel(
            main,
            text=mode.replace('_', ' ').title(),
            font=("Arial", 16, "bold"),
            text_color=PURPLE
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            main,
            text=f"Question {current_index + 1} of {total_questions}",
            font=("Arial", 20, "bold"),
            text_color=TEXT
        ).pack(pady=15)

        ctk.CTkLabel(
            main,
            text=question["question_text"],
            font=("Arial", 18),
            text_color=TEXT,
            wraplength=750
        ).pack(pady=20)

        options = question.get("options_json") or {}

        for letter, option_text in options.items():

            ctk.CTkRadioButton(
                main,
                text=f"{letter}. {option_text}",
                variable=selected_answer,
                value=letter,
                font=("Arial", 15),
                text_color=TEXT
            ).pack(anchor="w", padx=100, pady=10)

        ctk.CTkButton(
            main,
            text="Submit Answer",
            fg_color=PURPLE,
            hover_color="#5745C5",
            height=40,
            command=submit_answer
        ).pack(pady=25)

    # SUBMIT ANSWER
    def submit_answer():

        nonlocal score

        answer = selected_answer.get()

        if not answer:
            messagebox.showwarning(
                "Select Answer",
                "Please select an answer first."
            )
            return

        question = questions[current_index]

        time_taken = round(
            time.time() - question_start_time, 2
        )

        # Save answer through Django
        result = save_answer_attempt(
            user_id,
            session_id,
            question["question_id"],
            answer,
            time_taken
        )

        # Handle API errors
        if "error" in result:
            messagebox.showerror(
                "Save Error",
                f"Could not save your answer:\n{result['error']}"
            )
            return

        # Get correctness from Django
        is_correct = result["is_correct"]

        if is_correct:
            score += 1
            feedback = "Correct Answer!"
            feedback_color = "#2EAD63"

        else:
            feedback = "Incorrect Answer!"
            feedback_color = "#E5484D"

        correct_answer = question["correct_answer"].strip()

        clear_main()

        # Feedback
        ctk.CTkLabel(
            main,
            text=feedback,
            font=("Arial", 24, "bold"),
            text_color=feedback_color
        ).pack(pady=25)

        # Correct answer
        ctk.CTkLabel(
            main,
            text=f"Correct Answer: {correct_answer}",
            font=("Arial", 16, "bold"),
            text_color=TEXT
        ).pack(pady=10)

        # Explanation
        ctk.CTkLabel(
            main,
            text=question.get("explanation") or
                 "No explanation available.",
            font=("Arial", 15),
            text_color=TEXT,
            wraplength=750
        ).pack(pady=20)

        # Next question
        ctk.CTkButton(
            main,
            text="Next Question",
            fg_color=PURPLE,
            hover_color="#5745C5",
            height=40,
            command=next_question
        ).pack(pady=25)

    # NEXT QUESTION
    def next_question():

        nonlocal current_index

        current_index += 1

        if current_index < total_questions:
            display_question()

        else:
            show_revision_result()

    # FINAL RESULT
    def show_revision_result():
        completion_result = complete_revision_session(session_id)

        if "error" in completion_result:
            messagebox.showerror(
                "Error",
                str(completion_result["error"])
            )
            return

        clear_main()

        accuracy = (score / total_questions) * 100

        ctk.CTkLabel(
            main,
            text="Revision Completed!",
            font=("Arial", 28, "bold"),
            text_color=PURPLE
        ).pack(pady=30)

        ctk.CTkLabel(
            main,
            text=f"Session ID: {session_id}",
            font=("Arial", 15),
            text_color=MUTED
        ).pack(pady=10)

        ctk.CTkLabel(
            main,
            text=f"Total Questions: {total_questions}",
            font=("Arial", 18),
            text_color=TEXT
        ).pack(pady=10)

        ctk.CTkLabel(
            main,
            text=f"Correct Answers: {score}",
            font=("Arial", 18, "bold"),
            text_color="#2EAD63"
        ).pack(pady=10)

        ctk.CTkLabel(
            main,
            text=f"Incorrect Answers: {total_questions - score}",
            font=("Arial", 18, "bold"),
            text_color="#E5484D"
        ).pack(pady=10)

        ctk.CTkLabel(
            main,
            text=f"Accuracy: {accuracy:.1f}%",
            font=("Arial", 22, "bold"),
            text_color=PURPLE
        ).pack(pady=20)

        # Back to Home
        ctk.CTkButton(
            main,
            text="Back to Home",
            fg_color=PURPLE,
            hover_color="#5745C5",
            height=45,
            width=180,
            command=lambda: show_page("Start Revision")
        ).pack(pady=25)

    display_question()

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


# Store sidebar buttons
sidebar_buttons = {}


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

    sidebar_buttons[item] = button


# ---------------- MAIN CONTENT ----------------

main = ctk.CTkFrame(
    app,
    fg_color=BG,
    corner_radius=0
)

main.pack(
    side="left",
    fill="both",
    expand=True,
    padx=30,
    pady=25
)


def clear_main():

    for widget in main.winfo_children():
        widget.destroy()


# ---------------- SIDEBAR NAVIGATION ----------------

def update_sidebar(selected_page):

    for item, button in sidebar_buttons.items():

        if item == selected_page:

            button.configure(
                fg_color=LIGHT_PURPLE,
                text_color=PURPLE,
                font=("Arial", 14, "bold")
            )

        else:

            button.configure(
                fg_color=SIDEBAR,
                text_color=MUTED,
                font=("Arial", 14, "normal")
            )


# ---------------- PAGE NAVIGATION ----------------

def show_page(page_name):

    # Update selected sidebar button
    update_sidebar(page_name)

    clear_main()

    if page_name == "My Subjects":

        show_my_subjects(main)

    elif page_name == "Start Revision":

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

        show_revision_home()

    else:

        heading = ctk.CTkLabel(
            main,
            text=page_name,
            font=("Arial", 30, "bold"),
            text_color=TEXT
        )

        heading.pack(anchor="w", pady=(15, 5))

        placeholder = ctk.CTkLabel(
            main,
            text=f"{page_name} page coming soon!",
            font=("Arial", 18),
            text_color=MUTED
        )

        placeholder.pack(pady=100)


# ---------------- START REVISION HOME ----------------

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
        command=show_revision_mode_popup
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
