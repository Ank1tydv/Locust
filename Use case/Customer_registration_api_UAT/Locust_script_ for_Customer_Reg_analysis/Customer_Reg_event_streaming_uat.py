# Locust script for Customer Registration Analysis Streaming Server
import json
import uuid
import pytz  # Import the pytz library
from locust import HttpUser, task, between
from datetime import datetime


class MyUser(HttpUser):
    wait_time = between(1, 3)  # wait time between requests

    def __init__(self, *args, **kwargs):
        super(MyUser, self).__init__(*args, **kwargs)
        self.user_id = str(uuid.uuid4())
        self.event_count = 0  # initialize the event count to 0 for each user 

    @task  # marks this function as a task in Locust
    def send_event_single_user(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJraWQiOiJqWXdqOXRZQU0ybksweUJBaHJ0Zlwvc3B5OTdMVTZ3cjI1XC90cWZNVlJqN1E9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI1cTg2aXFwY2Y4aTNsZ2JnaTA2bWY3MDkzOCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiY2xpZW50c1wvbm90aGluZyIsImF1dGhfdGltZSI6MTY5ODkyMTA2MywiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoLTEuYW1hem9uYXdzLmNvbVwvYXAtc291dGgtMV9CcFVsUlZiSDYiLCJleHAiOjE2OTg5NDI2NjMsImlhdCI6MTY5ODkyMTA2MywidmVyc2lvbiI6MiwianRpIjoiNjQ2NWNiNDQtYWVkYS00MDdjLTkwMWQtZDBhNTI3ZjJiYTljIiwiY2xpZW50X2lkIjoiNXE4NmlxcGNmOGkzbGdiZ2kwNm1mNzA5MzgifQ.Q3OhOa1LwUc-TARC3cQsWkAf3cGeOVanTsGrQqiYpDjulDX6hYIWev86I_mcgfzUTr8bfCeVTHwXaC7Me_4vkcGylREabXRms2rgS_q5aY54vkzpPUh_Dd6xArIBP4TtQubEhG54IBuWOXZyZa3dw3p4Gp8L2K2tUAxxaPHUUvuVeu-2pxTWALSrGcwXLqIvJC_fo5ZOrbD_9O4YSlzwR_3UoXGzqz88rRCvrbfTzvflvo6KF0INRlYDq1K0HtNWFgNdE_xSaR3alSYT7g65wQ_wbrmn-WH8GbKPTtaF8uUZmZvruIWCnmdG0kf7mZo-lj59XZ_ky5h2HkV3qHdjcA"  # add your bearer token here
        }

        # Generate a new timestamp for each event in IST timezone
         # Convert the current UTC time to IST (Indian Standard Time)
        current_time = datetime.now(pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
        self.timestamp = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')  # Format the datetime object without timezone offset



        data = {
                    "eventId": 100006,
                    "auditId": "AUD-20230920-001",
                    "deviceDescription": "Moto 10 plus",
                    "identifierValue": "IDV-56789",
                    "ip": "192.168.1.100",
                    "latitude": "34.0522",
                    "longitude": "-118.2437",
                    "identifierType": "TypeA",
                    "applicationName": "MyApp",
                    "mobileNumber": "+1234567890",
                    "emailId": "sample1@email.com",
                    "accountState": "Active",
                    "deviceType": "Mobile",
                    "deviceId": "DEV-001",
                    "nyeAppVersion": "v1.0.0",
                    "createdTimeStamp":  self.timestamp   # Use the user's unique timestamp here
                    
     }
        self.event_count += 1  # increment the event count by 1 each time the task is run

        response = self.client.post(
            "https://ewxkjiiipb.execute-api.ap-south-1.amazonaws.com/uat/streaming/events/v1/event/auth/100006",
            json=data,
            headers=headers,
            name="Send Event"
        )
        # Save the response, user ID, event count, and other relevant data as a JSON object
        log_entry = {
            "userID": self.user_id,
            "eventCount": self.event_count,
            "responseData": response.text,
            "responseStatus": response.status_code,
            "createdTimeStamp":  self.timestamp
            # Add more fields as needed
        }
        
        if response.status_code == 200:  # request was successful
            file_name = '/mnt/locust/results.txt'
        else:  # request failed
            file_name = '/mnt/locust/failure.txt'
        
        with open(file_name, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
