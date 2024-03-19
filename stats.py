from db_service import MongoDBHandler
database = MongoDBHandler("SoundHealthDB")

class stats: 
 
    def get_topic_statistics(self):
        dictionary = {}
        all_conversations = database.get_db_size()
        topics = ['Mononucleosis', 'Hepatitis B Virus', 'Diabetes', 'Migraine', 'Coeliac', 'Kidney stones', 'Irritable Bowel Syndrome']
        for topic in topics:
            _, topic_num = database.get_conversations_by_element(topic, "topic") 
            if topic_num != 0:           
                percent = int((topic_num / all_conversations) * 100) 
            else:
                percent = 0
            dictionary[topic] = str(percent) + "%"
        
        return dictionary
    
    def get_status_statistics(self):
        dictionary = {}
        all_conversations = database.get_db_size()        
        statuses = ['under review', 'end of inspection', 'for further inspection']
        for status in statuses:
            _, status_num = database.get_conversations_by_element(status, "status")  
            if (all_conversations != 0):      
                percent = int((status_num / all_conversations) * 100) 
            else:
                percent = 0
            dictionary[status] = str(percent) + "%"
        
        return dictionary
    
    def get_topic_from_status_statistics(self):
        dictionary = {}        
        statuses = ['under review', 'end of inspection', 'for further inspection']
        topics = ['Mononucleosis', 'Hepatitis B Virus', 'Diabetes', 'Migraine', 'Coeliac', 'Kidney stones', 'Irritable Bowel Syndrome']        
        for status in statuses:
            status_list, status_num = database.get_conversations_by_element(status, "status") 
            for topic in topics:
                topic_list, _ = database.get_conversations_by_element(topic, "topic")
                intersection_list = [item for item in status_list if any(item.items() <= d.items() for d in topic_list)]                                           
                if (status_num != 0):
                    percent = int((len(intersection_list) / status_num) * 100)
                else: 
                    percent = 0
                dictionary[topic + ", " + status] = str(percent) + "%"

        return dictionary