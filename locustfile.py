from locust import HttpUser, task, between

class StudentDropoutUser(HttpUser):
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks

    @task
    def predict_dropout(self):
        # Sample data matching your 13 features
        data = {
            "School": "MS",
            "Mother_Education": 2,
            "Father_Education": 3,
            "Final_Grade": 15,
            "Grade_1": 14,
            "Grade_2": 16,
            "Number_of_Failures": 0,
            "Wants_Higher_Education": "yes",
            "Study_Time": 2,
            "Weekend_Alcohol_Consumption": 1,
            "Weekday_Alcohol_Consumption": 1,
            "Address": "U",
            "Reason_for_Choosing_School": "course"
        }
        self.client.post("/predict", json=data)