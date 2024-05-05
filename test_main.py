import string
import pytest
import secrets
import requests

def generate_random_id():
    return ''.join(secrets.choice(string.digits) for _ in range(9))


def generate_random_user_key():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))


user_key_test = generate_random_user_key()
doctor_id_test = generate_random_id()

conversation_id = 0

def test_insert_new_doctor():
    try:        
        data = {
            "user_key": user_key_test,
            "doctor_id": doctor_id_test
        }
       
        url = "https://medinsightaudioweb.azurewebsites.net/insert_new_doctor"
       

        response = requests.post(url, data=data)
        assert response.status_code == 200
        
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")


def test_upload_voice_data():  
    global conversation_id 

    url = "https://medinsightaudioweb.azurewebsites.net/upload_voice_data"
    
    audio_file_path = "test_audio.wav"
    
    data = {
        "user_key": user_key_test,
        "doctor_id": doctor_id_test,
        "patient_id": "123456789",
        "topic": "Mononucleosis"
    }
   
    try:
        with open(audio_file_path, "rb") as audio_file:
            files = {"file": (audio_file_path, audio_file)}
            response = requests.post(url, files=files, data=data)        
        
        response_dict = response.json()        

        conversation_id = response_dict["conversation_id"]

        assert response.status_code == 200
        
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")


def test_get_doctor_conversations():
    try:
        
        url = "https://medinsightaudioweb.azurewebsites.net/get_doctor_conversations"
       
        params = {
            'user_key': user_key_test,
            'doctor_id': doctor_id_test
        }
        
        response = requests.get(url, params=params)

        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

def test_get_patient_conversations():
    try:
        
        url = "https://medinsightaudioweb.azurewebsites.net/get_patient_conversations"
       
        params = {
            'user_key': user_key_test,
            'doctor_id': doctor_id_test,
            'patient_id': '123456789'
        }
        
        response = requests.get(url, params=params)

        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

def test_get_topic_conversations():
    try:
        
        url = "https://medinsightaudioweb.azurewebsites.net/get_topic_conversations"
       
        params = {
            'user_key': user_key_test,
            'doctor_id': doctor_id_test,
            'topic': 'Mononucleosis'
        }
        
        response = requests.get(url, params=params)

        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

def test_get_id_conversations():
    try:
        global conversation_id
        url = "https://medinsightaudioweb.azurewebsites.net/get_id_conversations"
       
        params = {
            'user_key': user_key_test,
            'doctor_id': doctor_id_test,
            'conversation_id': conversation_id
        }
        
        response = requests.get(url, params=params)        

        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

def test_get_status_conversations():
    try:        
        url = "https://medinsightaudioweb.azurewebsites.net/get_status_conversations"
       
        params = {
            'user_key': user_key_test,
            'doctor_id': doctor_id_test,
            'status': 'under review'
        }
        
        response = requests.get(url, params=params)        

        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

def test_get_similar_tests():
    try:
        global conversation_id
        url = "https://medinsightaudioweb.azurewebsites.net/get_similar_tests"
       
        params = {
            'user_key': user_key_test,
            'doctor_id': doctor_id_test,
            'conversation_id': conversation_id
        }
        
        response = requests.get(url, params=params)        

        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

def test_update_status():
    try:   
        global conversation_id     
        data = {
            "user_key": user_key_test,
            "doctor_id": doctor_id_test,
            'conversation_id': conversation_id,
            'status': 'completed'
        }
       
        url = "https://medinsightaudioweb.azurewebsites.net/update_status"
       

        response = requests.post(url, data=data)
        assert response.status_code == 200
        
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

def test_get_statistics():
    try:        
        url = "https://medinsightaudioweb.azurewebsites.net/get_statistics"
       
        params = {
            'user_key': user_key_test,
            'doctor_id': doctor_id_test,            
        }
        
        response = requests.get(url, params=params)        

        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")
