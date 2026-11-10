import requests

BASE_URL = "http://127.0.0.1:8000/api/revision/"


def start_revision_session(user_id, topic_id):

    url = BASE_URL + "start-session/"

    data = {
        "user_id": user_id,
        "topic_id": topic_id,
        "status": "IN_PROGRESS",
        "session_mode": "TOPIC_PRACTICE"
    }

    try:
        response = requests.post(url, json=data, timeout=10)

        if response.status_code == 201:
            return response.json()

        return {
            "error": response.json()
        }

    except requests.RequestException as error:
        return {
            "error": str(error)
        }

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