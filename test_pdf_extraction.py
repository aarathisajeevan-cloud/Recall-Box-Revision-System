from revision.pdf_question_extractor import (
    extract_pdf_text,
    parse_questions
)

from tkinter import Tk, filedialog
import json

root = Tk()
root.withdraw()

pdf_path = filedialog.askopenfilename(
    title="Select Question Bank PDF",
    filetypes=[("PDF Files", "*.pdf")]
)

if pdf_path:

    result = extract_pdf_text(pdf_path)

    if result["success"]:

        extracted_text = result["text"]

        questions = parse_questions(extracted_text)

        print("\n===== EXTRACTED QUESTIONS =====\n")

        for question in questions:

            print("Question Number:", question["question_number"])
            print("Question:", question["question_text"])

            print("Options:")

            for key, value in question["options"].items():
                print(key, ":", value)

            print("Correct Answer:", question["correct_answer"])
            print("Explanation:", question["explanation"])

            print("-" * 50)

        # Save structured data as JSON
        with open(
            "parsed_questions.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                questions,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\nQuestions saved to parsed_questions.json")

    else:
        print("Error:", result["error"])

else:
    print("No PDF selected.")

root.destroy()