import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
from pdf_question_extractor import extract_pdf_text, parse_questions
from api_client import save_questions


# ---------------- CONFIGURATION ----------------

BG = "#F7F7FC"
PURPLE = "#6957D8"
LIGHT_PURPLE = "#EEEAFE"
TEXT = "#25243A"
MUTED = "#85849A"
WHITE = "#FFFFFF"


# ---------------- TEMPORARY SUBJECT STORAGE ----------------

subjects = []
selected_subject = None

next_subject_id = 1
next_topic_id = 1


# ---------------- MAIN MY SUBJECTS PAGE ----------------

def show_my_subjects(parent):

    global main

    main = parent

    clear_main()
    show_subjects_page()


def clear_main():

    for widget in main.winfo_children():
        widget.destroy()


# ---------------- DISPLAY SUBJECTS ----------------

def show_subjects_page():

    clear_main()

    heading = ctk.CTkLabel(
        main,
        text="My Subjects",
        font=("Arial", 30, "bold"),
        text_color=TEXT
    )
    heading.pack(anchor="w", pady=(15, 5))

    subtitle = ctk.CTkLabel(
        main,
        text="Organize your subjects and manage your learning topics.",
        font=("Arial", 14),
        text_color=MUTED
    )
    subtitle.pack(anchor="w", pady=(0, 25))

    ctk.CTkButton(
        main,
        text="+ Add Subject",
        width=160,
        height=40,
        fg_color=PURPLE,
        hover_color="#5544B8",
        command=add_subject
    ).pack(anchor="e", pady=(0, 20))

    subject_container = ctk.CTkFrame(
        main,
        fg_color="transparent"
    )
    subject_container.pack(fill="both", expand=True)

    if not subjects:

        ctk.CTkLabel(
            subject_container,
            text="No subjects added yet.\nClick '+ Add Subject' to get started.",
            font=("Arial", 17),
            text_color=MUTED
        ).pack(pady=100)

    else:

        for subject in subjects:

            subject_card = ctk.CTkFrame(
                subject_container,
                fg_color=WHITE,
                corner_radius=15,
                height=110
            )
            subject_card.pack(fill="x", pady=8)
            subject_card.pack_propagate(False)

            ctk.CTkLabel(
                subject_card,
                text=subject["name"],
                font=("Arial", 19, "bold"),
                text_color=TEXT
            ).pack(side="left", padx=25)

            ctk.CTkButton(
                subject_card,
                text="Open Subject →",
                width=140,
                fg_color=LIGHT_PURPLE,
                hover_color="#DCD4FF",
                text_color=PURPLE,
                command=lambda s=subject: show_subject_details(s)
            ).pack(side="right", padx=20)


# ---------------- ADD SUBJECT ----------------

def add_subject():

    dialog = ctk.CTkToplevel(main)
    dialog.title("Add Subject")
    dialog.geometry("400x230")
    dialog.resizable(False, False)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="Create New Subject",
        font=("Arial", 21, "bold"),
        text_color=TEXT
    ).pack(pady=(25, 15))

    subject_entry = ctk.CTkEntry(
        dialog,
        placeholder_text="Enter subject name",
        width=300,
        height=40
    )
    subject_entry.pack(pady=10)

    def save_subject():

        subject_name = subject_entry.get().strip()

        if not subject_name:
            messagebox.showwarning(
                "Input Required",
                "Please enter a subject name.",
                parent=dialog
            )
            return
        global next_subject_id

        subjects.append({
            "id": next_subject_id,
            "name": subject_name,
            "topics": []
        })

        next_subject_id += 1

        dialog.destroy()
        show_subjects_page()

    ctk.CTkButton(
        dialog,
        text="Save Subject",
        width=150,
        fg_color=PURPLE,
        hover_color="#5544B8",
        command=save_subject
    ).pack(pady=15)

# ---------------- SUBJECT DETAILS ----------------

# ---------------- SUBJECT DETAILS ----------------

def show_subject_details(subject):

    clear_main()

    # Back button
    ctk.CTkButton(
        main,
        text="← Back to Subjects",
        fg_color="transparent",
        text_color=PURPLE,
        hover_color=LIGHT_PURPLE,
        command=show_subjects_page
    ).pack(anchor="w", pady=(10, 15))

    # Subject title
    ctk.CTkLabel(
        main,
        text=subject["name"],
        font=("Arial", 28, "bold"),
        text_color=TEXT
    ).pack(anchor="w", pady=5)

    ctk.CTkLabel(
        main,
        text="Manage topics under this subject.",
        font=("Arial", 14),
        text_color=MUTED
    ).pack(anchor="w", pady=(0, 20))

    # Add Topic button
    ctk.CTkButton(
        main,
        text="+ Add Topic",
        fg_color=PURPLE,
        hover_color="#5544B8",
        command=lambda: add_topic(subject)
    ).pack(anchor="e", pady=10)

    # Display Topics
    if not subject["topics"]:

        ctk.CTkLabel(
            main,
            text="No topics added yet. Click '+ Add Topic' to get started.",
            font=("Arial", 15),
            text_color=MUTED
        ).pack(pady=50)

    else:

        for topic in subject["topics"]:

            topic_card = ctk.CTkFrame(
                main,
                fg_color=WHITE,
                corner_radius=12,
                height=80
            )

            topic_card.pack(fill="x", pady=7)
            topic_card.pack_propagate(False)

            ctk.CTkLabel(
                topic_card,
                text=topic["name"],
                font=("Arial", 17, "bold"),
                text_color=TEXT
            ).pack(side="left", padx=20)

            ctk.CTkButton(
                topic_card,
                text="Open Topic →",
                fg_color=LIGHT_PURPLE,
                hover_color="#DCD4FF",
                text_color=PURPLE,
                command=lambda t=topic, s=subject: show_topic_details(t, s)
            ).pack(side="right", padx=20)
# ---------------- ADD TOPIC ----------------

def add_topic(subject):

    global next_topic_id

    dialog = ctk.CTkToplevel(main)
    dialog.title("Add Topic")
    dialog.geometry("400x230")
    dialog.resizable(False, False)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text="Create New Topic",
        font=("Arial", 21, "bold"),
        text_color=TEXT
    ).pack(pady=(25, 15))

    topic_entry = ctk.CTkEntry(
        dialog,
        placeholder_text="Enter topic name",
        width=300,
        height=40
    )
    topic_entry.pack(pady=10)

    def save_topic():
        global next_topic_id

        topic_name = topic_entry.get().strip()

        if not topic_name:
            messagebox.showwarning(
                "Input Required",
                "Please enter a topic name.",
                parent=dialog
            )
            return

        subject["topics"].append({
            "id": next_topic_id,
            "name": topic_name,
            "pdf": None,
            "questions": []
        })

        next_topic_id += 1

        dialog.destroy()

        check_topic_ids()

        show_subject_details(subject)

    ctk.CTkButton(
        dialog,
        text="Save Topic",
        width=150,
        fg_color=PURPLE,
        hover_color="#5544B8",
        command=save_topic
    ).pack(pady=15)
    check_topic_ids()

# ---------------- TOPIC DETAILS ----------------

# ---------------- TOPIC DETAILS ----------------

def show_topic_details(topic, subject):

    clear_main()

    # Back button
    ctk.CTkButton(
        main,
        text="← Back to Subject",
        fg_color="transparent",
        text_color=PURPLE,
        hover_color=LIGHT_PURPLE,
        command=lambda: show_subject_details(subject)
    ).pack(anchor="w", pady=(10, 15))

    # Topic title
    ctk.CTkLabel(
        main,
        text=topic["name"],
        font=("Arial", 28, "bold"),
        text_color=TEXT
    ).pack(anchor="w", pady=5)

    ctk.CTkLabel(
        main,
        text="Manage your question bank for this topic.",
        font=("Arial", 14),
        text_color=MUTED
    ).pack(anchor="w", pady=(0, 25))

    # Upload Question Bank
    ctk.CTkButton(
        main,
        text="📄 Upload Question Bank PDF",
        width=230,
        height=45,
        fg_color=PURPLE,
        hover_color="#5544B8",
        command=lambda: upload_question_bank(topic, subject)
    ).pack(anchor="w", pady=10)

    # Preview Questions Button
    ctk.CTkButton(
        main,
        text="Preview Questions",
        fg_color=PURPLE,
        hover_color="#5745C5",
        text_color=WHITE,
        command=lambda: preview_questions(topic, subject)
    ).pack(pady=10)

    # Display uploaded PDF
    if topic["pdf"]:

        ctk.CTkLabel(
            main,
            text=f"Uploaded File: {os.path.basename(topic['pdf'])}",
            font=("Arial", 14),
            text_color=TEXT
        ).pack(anchor="w", pady=10)

        ctk.CTkLabel(
            main,
            text=f"Questions Extracted: {len(topic['questions'])}",
            font=("Arial", 14, "bold"),
            text_color=PURPLE
        ).pack(anchor="w", pady=10)

#preview questions
def preview_questions(topic, subject):

    clear_main()

    # Back Button
    ctk.CTkButton(
        main,
        text="← Back to Topic",
        fg_color="transparent",
        text_color=PURPLE,
        hover_color=LIGHT_PURPLE,
        command=lambda: show_topic_details(topic, subject)
    ).pack(anchor="w", pady=10)

    # Heading
    ctk.CTkLabel(
        main,
        text="Question Preview",
        font=("Arial", 28, "bold"),
        text_color=TEXT
    ).pack(anchor="w", pady=10)

    questions = topic.get("questions", [])

    if not questions:
        ctk.CTkLabel(
            main,
            text="No questions available. Please upload a PDF.",
            font=("Arial", 15),
            text_color=MUTED
        ).pack(pady=30)

        return

    ctk.CTkLabel(
        main,
        text=f"Total Questions: {len(questions)}",
        font=("Arial", 15, "bold"),
        text_color=PURPLE
    ).pack(anchor="w", pady=10)
    # Confirm & Save Button
    ctk.CTkButton(
        main,
        text="Confirm & Save",
        height=40,
        fg_color=PURPLE,
        hover_color="#5745C5",
        text_color=WHITE,
        command=lambda: confirm_and_save_questions(topic)
    ).pack(anchor="e", pady=10)

    # Scrollable Question Area
    question_frame = ctk.CTkScrollableFrame(
        main,
        fg_color=BG
    )

    question_frame.pack(
        fill="both",
        expand=True,
        pady=10
    )

    for index, question in enumerate(questions, start=1):

        card = ctk.CTkFrame(
            question_frame,
            fg_color=WHITE,
            corner_radius=12
        )

        card.pack(fill="x", padx=10, pady=8)

        # Edit Question Button

        ctk.CTkButton(
            card,
            text="Edit Question",
            width=110,
            height=30,
            fg_color=PURPLE,
            hover_color="#5745C5",
            command=lambda q=question: edit_question(q, topic, subject)
        ).pack(anchor="e", padx=15, pady=5)

        ctk.CTkLabel(
            card,
            text=f"Question {index}: {question['question_text']}",
            font=("Arial", 15, "bold"),
            text_color=TEXT,
            wraplength=800,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(15, 8))

        for option, value in question["options"].items():

            ctk.CTkLabel(
                card,
                text=f"{option}. {value}",
                font=("Arial", 13),
                text_color=MUTED,
                wraplength=750,
                justify="left"
            ).pack(anchor="w", padx=30, pady=3)

        ctk.CTkLabel(
            card,
            text=f"Answer: {question['correct_answer']}",
            font=("Arial", 13, "bold"),
            text_color=PURPLE
        ).pack(anchor="w", padx=15, pady=(8, 5))

        ctk.CTkLabel(
            card,
            text=f"Explanation: {question['explanation']}",
            font=("Arial", 12),
            text_color=MUTED,
            wraplength=800,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 15))

#confirm and save questions

def confirm_and_save_questions(topic):

    questions = topic.get("questions", [])

    if not questions:
        messagebox.showerror(
            "Error",
            "No questions available to save."
        )
        return

    formatted_questions = []

    for question in questions:

        answer = question["correct_answer"].strip().upper()

        # Convert answers like B. def into B
        answer = answer[0] if answer else ""

        if answer not in question["options"]:
            messagebox.showerror(
                "Invalid Question",
                f"Invalid correct answer for Question "
                f"{question['question_number']}."
            )
            return

        if not question["question_text"].strip():
            messagebox.showerror(
                "Invalid Question",
                "Question text cannot be empty."
            )
            return

        formatted_questions.append({
            "topic_id": topic.get("id", 1),
            "question_text": question["question_text"],
            "question_type": "MCQ",
            "options_json": question["options"],
            "correct_answer": answer,
            "explanation": question["explanation"],
            "difficulty": "Easy",
            "is_active": True
        })

    # Confirm before saving
    confirm = messagebox.askyesno(
        "Confirm & Save",
        f"Are you sure you want to save "
        f"{len(formatted_questions)} questions?"
    )

    if not confirm:
        return

    result = save_questions(formatted_questions)

    if "error" in result:

        messagebox.showerror(
            "Save Failed",
            str(result["error"])
        )

    else:

        messagebox.showinfo(
            "Success",
            f"{result['total_questions']} questions "
            "saved successfully to the database!"
        )


#edit question

def edit_question(question, topic, subject):

    clear_main()

    # Back Button
    ctk.CTkButton(
        main,
        text="← Back to Preview",
        fg_color="transparent",
        text_color=PURPLE,
        hover_color=LIGHT_PURPLE,
        command=lambda: preview_questions(topic, subject)
    ).pack(anchor="w", pady=5)

    # Heading
    ctk.CTkLabel(
        main,
        text="Edit Question",
        font=("Arial", 28, "bold"),
        text_color=TEXT
    ).pack(anchor="w", pady=10)

    # Scrollable Form
    form = ctk.CTkScrollableFrame(
        main,
        fg_color=BG
    )
    form.pack(fill="both", expand=True, pady=5)

    # Question Text
    ctk.CTkLabel(
        form,
        text="Question",
        text_color=TEXT
    ).pack(anchor="w")

    question_entry = ctk.CTkTextbox(form, height=80)
    question_entry.pack(fill="x", pady=5)
    question_entry.insert("1.0", question["question_text"])

    # Options
    option_entries = {}

    for option, value in question["options"].items():

        ctk.CTkLabel(
            form,
            text=f"Option {option}",
            text_color=TEXT
        ).pack(anchor="w")

        entry = ctk.CTkEntry(form, height=35)
        entry.pack(fill="x", pady=5)
        entry.insert(0, value)

        option_entries[option] = entry

    # Correct Answer
    ctk.CTkLabel(
        form,
        text="Correct Answer (A/B/C/D)",
        text_color=TEXT
    ).pack(anchor="w", pady=(10, 0))

    answer_entry = ctk.CTkEntry(form)
    answer_entry.pack(fill="x", pady=5)
    answer_entry.insert(0, question["correct_answer"])

    # Explanation
    ctk.CTkLabel(
        form,
        text="Explanation",
        text_color=TEXT
    ).pack(anchor="w")

    explanation_entry = ctk.CTkTextbox(form, height=80)
    explanation_entry.pack(fill="x", pady=5)
    explanation_entry.insert("1.0", question["explanation"])

    # Save Function
    def save_changes():

        new_answer = answer_entry.get().strip().upper()

# Accept formats such as B, B. DEF or B. DEF
        if new_answer:
            new_answer = new_answer[0]

        if new_answer not in option_entries:
            messagebox.showerror(
                "Invalid Answer",
                "Enter a valid option: A, B, C or D."
            )
            return

        new_question = question_entry.get("1.0", "end").strip()

        if not new_question:
            messagebox.showerror(
                "Error",
                "Question text cannot be empty."
            )
            return

        question["question_text"] = new_question

        for option, entry in option_entries.items():
            question["options"][option] = entry.get().strip()

        question["correct_answer"] = new_answer

        question["explanation"] = explanation_entry.get(
            "1.0", "end"
        ).strip()

        messagebox.showinfo(
            "Success",
            "Question updated successfully!"
        )

        preview_questions(topic, subject)

    # Save Changes Button
    ctk.CTkButton(
        form,
        text="Save Changes",
        height=45,
        fg_color=PURPLE,
        hover_color="#5745C5",
        text_color=WHITE,
        command=save_changes
    ).pack(pady=20)



# ---------------- PDF UPLOAD ----------------

def upload_question_bank(topic, subject):

    pdf_path = filedialog.askopenfilename(
        title="Select Question Bank PDF",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not pdf_path:
        return

    result = extract_pdf_text(pdf_path)

    if not result["success"]:
        messagebox.showerror(
            "Extraction Error",
            result["error"]
        )
        return

    questions = parse_questions(result["text"])

    if not questions:
        messagebox.showwarning(
            "No Questions Found",
            "No questions were detected in this PDF."
        )
        return

    topic["pdf"] = pdf_path
    topic["questions"] = questions

    messagebox.showinfo(
        "Success",
        f"PDF uploaded successfully!\n"
        f"Questions extracted: {len(questions)}"
    )

    show_topic_details(topic, subject)


def show_subjects_for_practice(parent, callback):

    global main
    main = parent

    clear_main()

    ctk.CTkLabel(
        main,
        text="Choose a Subject",
        font=("Arial", 28, "bold"),
        text_color=TEXT
    ).pack(anchor="w", pady=15)

    if not subjects:
        ctk.CTkLabel(
            main,
            text="No subjects available. Please add a subject first.",
            font=("Arial", 16),
            text_color=MUTED
        ).pack(pady=50)
        return

    for subject in subjects:

        ctk.CTkButton(
            main,
            text=subject["name"],
            height=50,
            fg_color=LIGHT_PURPLE,
            hover_color="#DCD4FF",
            text_color=PURPLE,
            command=lambda s=subject: show_topics_for_practice(
                s, callback
            )
        ).pack(fill="x", pady=8)


def show_topics_for_practice(subject, callback):

    clear_main()

    ctk.CTkButton(
        main,
        text="← Back to Subjects",
        fg_color="transparent",
        text_color=PURPLE,
        hover_color=LIGHT_PURPLE,
        command=lambda: show_subjects_for_practice(
            main, callback
        )
    ).pack(anchor="w", pady=10)

    ctk.CTkLabel(
        main,
        text=subject["name"] + " - Choose a Topic",
        font=("Arial", 26, "bold"),
        text_color=TEXT
    ).pack(anchor="w", pady=15)

    if not subject["topics"]:
        ctk.CTkLabel(
            main,
            text="No topics available in this subject.",
            font=("Arial", 16),
            text_color=MUTED
        ).pack(pady=50)
        return

    for topic in subject["topics"]:

        ctk.CTkButton(
            main,
            text=topic["name"],
            height=50,
            fg_color=LIGHT_PURPLE,
            hover_color="#DCD4FF",
            text_color=PURPLE,
            command=lambda t=topic: callback(t["id"])
        ).pack(fill="x", pady=8)


def check_topic_ids():

    print("\n--- SUBJECT AND TOPIC IDs ---")

    for subject in subjects:

        print("Subject:", subject["name"])

        for topic in subject["topics"]:

            print(
                "Topic:", topic["name"],
                "| Topic ID:", topic["id"]
            )