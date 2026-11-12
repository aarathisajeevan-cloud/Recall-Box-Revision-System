import pymupdf
import pdfplumber
import re


# --------------------------------------------------
# 1. EXTRACT TEXT FROM PDF
# --------------------------------------------------

def extract_pdf_text(pdf_path):

    try:
        extracted_text = ""

        # First method: PyMuPDF
        document = pymupdf.open(pdf_path)

        for page_number, page in enumerate(document, start=1):

            page_text = page.get_text("text", sort=True)

            extracted_text += f"\n\n--- Page {page_number} ---\n"
            extracted_text += page_text

        document.close()

        # Fallback: pdfplumber
        if len(extracted_text.strip()) < 30:

            extracted_text = ""

            with pdfplumber.open(pdf_path) as pdf:

                for page_number, page in enumerate(pdf.pages, start=1):

                    page_text = page.extract_text() or ""

                    extracted_text += f"\n\n--- Page {page_number} ---\n"
                    extracted_text += page_text

        if not extracted_text.strip():

            return {
                "success": False,
                "error": "No readable text found in this PDF."
            }

        return {
            "success": True,
            "text": extracted_text
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


# --------------------------------------------------
# 2. CLEAN TEXT
# --------------------------------------------------

def clean_text(text):

    text = text.replace("\xa0", " ")
    text = text.replace("\uf0b7", " ")

    text = re.sub(r'[ \t]+', ' ', text)

    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


# --------------------------------------------------
# 3. EXTRACT ANSWER KEY
# --------------------------------------------------

def extract_answer_key(text):

    answer_key = {}

    patterns = [
        r'(?im)^\s*(\d{1,3})\s*[-.):]\s*([A-D])\s*$',
        r'(?im)^\s*(?:Q(?:uestion)?\s*)?(\d{1,3})\s*[:\-]\s*([A-D])\s*$'
    ]

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for number, answer in matches:

            answer_key[int(number)] = answer.upper()

    return answer_key


# --------------------------------------------------
# 4. FIND QUESTION BLOCKS
# --------------------------------------------------

def split_question_blocks(text):

    pattern = re.compile(
        r'(?im)^[ \t]*(?:question\s*|q\s*)?'
        r'(\d{1,3})[.)\:][ \t]+'
    )

    matches = list(pattern.finditer(text))

    blocks = []

    for index, match in enumerate(matches):

        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(text)

        number = int(match.group(1))

        block = text[start:end].strip()

        if block:
            blocks.append((number, block))

    return blocks


# --------------------------------------------------
# 5. EXTRACT OPTIONS
# --------------------------------------------------

def extract_options(block):

    option_pattern = re.compile(
        r'(?im)^[ \t]*(?:\(([A-D])\)|([A-D])[.)])[ \t]+'
    )

    matches = list(option_pattern.finditer(block))

    # Try inline options if line-based options are unavailable
    if len(matches) < 2:

        option_pattern = re.compile(
            r'(?i)(?:^|\s)(?:\(([A-D])\)|([A-D])[.)])\s+'
        )

        matches = list(option_pattern.finditer(block))

    if len(matches) < 2:
        return "", {}

    question_text = block[:matches[0].start()].strip()

    options = {}

    for index, match in enumerate(matches):

        letter = (match.group(1) or match.group(2)).upper()

        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(block)

        option_text = block[start:end].strip()

        # Remove answer and explanation sections
        option_text = re.split(
            r'(?im)^\s*(?:answer|correct answer|explanation|solution)\s*:',
            option_text
        )[0]

        options[letter] = clean_text(option_text)

    return clean_text(question_text), options


# --------------------------------------------------
# 6. EXTRACT CORRECT ANSWER
# --------------------------------------------------

def extract_correct_answer(block):

    pattern = re.compile(
        r'(?im)^\s*(?:correct\s+answer|answer|ans)'
        r'\s*[:\-]\s*(?:option\s*)?[\(\[]?([A-D])[\)\]]?'
    )

    match = pattern.search(block)

    if match:
        return match.group(1).upper()

    return ""


# --------------------------------------------------
# 7. EXTRACT EXPLANATION
# --------------------------------------------------

def extract_explanation(block):

    # Case 1: Explanation written separately
    pattern = re.compile(
        r'(?is)(?:explanation|solution|reason|'
        r'detailed explanation)\s*[:\-]\s*(.*)'
    )

    match = pattern.search(block)

    if match:
        explanation = match.group(1).strip()

        # Remove unwanted trailing sections
        explanation = re.split(
            r'(?im)^\s*(?:question|section)\s+\d+',
            explanation
        )[0]

        return clean_text(explanation)

    # Case 2: Explanation written after the answer
    answer_pattern = re.compile(
        r'(?im)^\s*(?:correct\s+answer|answer|ans)'
        r'\s*[:\-]\s*(.*)'
    )

    match = answer_pattern.search(block)

    if match:

        answer_text = match.group(1).strip()

        # Remove the answer option label
        answer_text = re.sub(
            r'^(?:option\s*)?[\(\[]?[A-D][\)\].]?\s*',
            '',
            answer_text,
            flags=re.IGNORECASE
        )

        # Find explanation separator
        separator = re.search(
            r'[—–−]|(?<!\w)\s-\s',
            answer_text
        )

        if separator:
            return clean_text(
                answer_text[separator.end():]
            )

    return ""

# --------------------------------------------------
# 8. MAIN MCQ PARSER
# --------------------------------------------------

def parse_questions(extracted_text):

    questions = []

    text = clean_text(extracted_text)

    answer_key = extract_answer_key(text)

    blocks = split_question_blocks(text)

    seen_questions = set()

    for number, block in blocks:

        # Extract options
        question_text, options = extract_options(block)

        # Ignore non-MCQ questions
        if len(options) < 2:
            continue

        # Extract answer
        correct_answer = extract_correct_answer(block)

        # Use answer key if inline answer is missing
        if not correct_answer:
            correct_answer = answer_key.get(number, "")

        # Extract explanation
        explanation = extract_explanation(block)

        # Remove duplicate options
        options = {
            key: value
            for key, value in options.items()
            if value.strip()
        }

        if len(options) < 2:
            continue

        # Validate question
        if not question_text:
            continue

        # Remove duplicate questions
        normalized = re.sub(
            r'\W+',
            '',
            question_text.lower()
        )

        if normalized in seen_questions:
            continue

        seen_questions.add(normalized)

        questions.append({

            "question_number": number,

            "question_text": question_text,

            "options": options,

            "correct_answer": correct_answer,

            "explanation": explanation

        })

    return questions