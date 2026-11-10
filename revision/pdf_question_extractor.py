import pymupdf
import re

def extract_pdf_text(pdf_path):

    try:
        document = pymupdf.open(pdf_path)

        extracted_text = ""

        for page_number, page in enumerate(document, start=1):
            page_text = page.get_text()

            extracted_text += f"\n--- Page {page_number} ---\n"
            extracted_text += page_text

        document.close()

        return {
            "success": True,
            "text": extracted_text
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }



def parse_questions(extracted_text):

    questions = []

    # Find each question block
    question_blocks = re.split(
        r'(?=Question\s+\d+\s*:)',
        extracted_text,
        flags=re.IGNORECASE
    )

    for block in question_blocks:

        if not re.search(r'Question\s+\d+\s*:', block, re.IGNORECASE):
            continue

        lines = block.strip().splitlines()

        question = {
            "question_number": None,
            "question_text": "",
            "options": {},
            "correct_answer": "",
            "explanation": ""
        }

        current_section = "question"

        for line in lines:

            line = line.strip()

            if not line or line.startswith("---"):
                continue

            # Extract question number and text
            match = re.match(
                r'Question\s+(\d+)\s*:\s*(.*)',
                line,
                re.IGNORECASE
            )

            if match:
                question["question_number"] = int(match.group(1))
                question["question_text"] = match.group(2)
                current_section = "question"
                continue

            # Extract options
            option_match = re.match(r'^([A-D])\.\s*(.*)$', line)

            if option_match:
                option_letter = option_match.group(1)
                option_text = option_match.group(2)

                question["options"][option_letter] = option_text
                current_section = "option_" + option_letter
                continue

            # Extract correct answer
            answer_match = re.match(
                r'Answer\s*:\s*(.*)',
                line,
                re.IGNORECASE
            )

            if answer_match:
                question["correct_answer"] = answer_match.group(1)
                current_section = "answer"
                continue

            # Extract explanation
            explanation_match = re.match(
                r'Explanation\s*:\s*(.*)',
                line,
                re.IGNORECASE
            )

            if explanation_match:
                question["explanation"] = explanation_match.group(1)
                current_section = "explanation"
                continue

            # Handle text continuing onto another line
            if current_section == "question":
                question["question_text"] += " " + line

            elif current_section.startswith("option_"):
                option_letter = current_section[-1]
                question["options"][option_letter] += " " + line

            elif current_section == "explanation":
                question["explanation"] += " " + line

        questions.append(question)

    return questions