class MedicalRecord:
    def __init__(self, user_key, doctor_id, patient_id, topic, conversation_id, transcription, chat_analysis):
        self.user_key = user_key
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.topic = topic
        self.conversation_id = conversation_id
        self.transcription = transcription
        self.chat_analysis = chat_analysis

    def get_all_data(self):
        return {
            "user_key": self._user_key,
            "doctor_id": self._doctor_id,
            "patient_id": self._patient_id, 
            "topic": self._topic,
            "conversation_id": self._conversation_id,           
            "transcription": self._transcription,
            "chat_analysis": self._chat_analysis
        }
    
    def set_all_data(self, data_dict):
        if "user_key" in data_dict and data_dict["user_key"] is not None:
            self._user_key = data_dict["user_key"]
        if "doctor_id" in data_dict and data_dict["doctor_id"] is not None:
            self._doctor_id = data_dict["doctor_id"]
        if "patient_id" in data_dict and data_dict["patient_id"] is not None:
            self._patient_id = data_dict["patient_id"]
        if "topic" in data_dict and data_dict["topic"] is not None:
            self._topic = data_dict["topic"]
        if "conversation_id" in data_dict and data_dict["conversation_id"] is not None:
            self._conversation_id = data_dict["conversation_id"]
        if "transcription" in data_dict and data_dict["transcription"] is not None:
            self._transcription = data_dict["transcription"]
        if "chat_analysis" in data_dict and data_dict["chat_analysis"] is not None:
            self._chat_analysis = data_dict["chat_analysis"]
    