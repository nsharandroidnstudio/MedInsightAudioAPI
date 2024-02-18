import string
import pytest
import secrets

import requests
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def generate_random_id():
    return ''.join(secrets.choice(string.digits) for _ in range(9))


def generate_random_user_key():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))


user_key_test = generate_random_user_key()
doctor_id_test = generate_random_id()



def test_insert_new_doctor():
    try:

        response = client.post(
            "/insert_new_doctor",
            data={"user_key": user_key_test, "doctor_id": doctor_id_test}
        )
        assert response.status_code == 200
        assert "new doctor user created successfully" in response.json()["message"]
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")


def test_upload_voice_data():
    try:
        # Assuming you have a test audio file named "test_audio.wav" in the same directory
        with open("test_audio.wav", "rb") as audio_file:
            response = client.post(
                "/upload_voice_data",
                files={"file": ("test_audio.wav", audio_file)},
                data={"user_key": user_key_test, "doctor_id": doctor_id_test, "patient_id": "123456789",
                      "topic": "Covid"}
            )
        assert response.status_code == 200

        # Print the actual response for debugging purposes
        print("Actual Response:", response.json())

        # Adjust the assertion to check a specific key in the response with an exact match
        assert 'Treatment recommendations: ' in response.json()
        assert 'conversation id:' in response.json()
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")


def test_get_doctor_conversations():
    try:

        url = "http://127.0.0.1:8000/get_doctor_conversations"

        # Define your parameters
        data = {
            'user_key': user_key_test,
            'doctor_id': doctor_id_test
        }

        # Define your headers
        headers = {
            'chunked': 'yes'
        }

        # Make the GET request
        response = requests.get(url, data=data, headers=headers)
        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

if __name__ == "__main__":
    pytest.main()
