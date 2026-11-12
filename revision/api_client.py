import requests

BASE_URL = "http://127.0.0.1:8000/api/revision/"


def start_revision_session(user_id, topic_id, session_mode):

    url = BASE_URL + "start-session/"

    data = {
        "user_id": user_id,
        "topic_id": topic_id,
        "status": "IN_PROGRESS",
        "session_mode": session_mode
    }

    try:
        response = requests.post(url, json=data, timeout=10)

        if response.status_code == 201:
            return response.json()

        try:
            return {"error": response.json()}
        except ValueError:
            return {"error": response.text}

    except requests.RequestException as error:
        return {"error": str(error)}


def save_questions(questions):
    url = BASE_URL + "save-questions/"

    data = {
        "questions": questions
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=10
        )

        if response.status_code == 201:
            return response.json()

        try:
            return {"error": response.json()}
        except ValueError:
            return {"error": response.text}

    except requests.RequestException as error:
        return {"error": str(error)}


def get_questions(topic_id):

    url = BASE_URL + "get-questions/"

    params = {
        "topic_id": topic_id
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        try:
            return {"error": response.json()}
        except ValueError:
            return {"error": response.text}

    except requests.RequestException as error:
        return {"error": str(error)}

def save_answer_attempt(user_id, session_id, question_id, selected_answer, time_taken):

    url = BASE_URL + "save-answer/"

    data = {
        "user_id": user_id,
        "session": session_id,
        "question": question_id,
        "selected_answer": selected_answer,
        "time_taken": time_taken
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=10
        )

        if response.status_code == 201:
            return response.json()

        try:
            return {"error": response.json()}
        except ValueError:
            return {"error": response.text}

    except requests.RequestException as error:
        return {"error": str(error)}


def complete_revision_session(session_id):
    url = BASE_URL + "complete-session/"

    data = {
        "session_id": session_id
    }

    try:
        response = requests.post(url, json=data, timeout=10)

        if response.status_code == 200:
            return response.json()

        try:
            return {"error": response.json()}
        except ValueError:
            return {"error": response.text}

    except requests.RequestException as error:
        return {"error": str(error)}