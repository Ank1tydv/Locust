# Locust script for SMS Analysis Stresming Server

import json
import uuid
from locust import HttpUser, task, between

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
            "Authorization": "Bearer eyJraWQiOiJqWXdqOXRZQU0ybksweUJBaHJ0Zlwvc3B5OTdMVTZ3cjI1XC90cWZNVlJqN1E9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI1cTg2aXFwY2Y4aTNsZ2JnaTA2bWY3MDkzOCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiY2xpZW50c1wvbm90aGluZyIsImF1dGhfdGltZSI6MTY5NzEwMzcyOSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoLTEuYW1hem9uYXdzLmNvbVwvYXAtc291dGgtMV9CcFVsUlZiSDYiLCJleHAiOjE2OTcxMjUzMjksImlhdCI6MTY5NzEwMzcyOSwidmVyc2lvbiI6MiwianRpIjoiNmYxMDRiZDYtNTEwMC00MTAwLTgxMWYtYzk2YTQyMzhmMDgwIiwiY2xpZW50X2lkIjoiNXE4NmlxcGNmOGkzbGdiZ2kwNm1mNzA5MzgifQ.k9kU32VEaNYzqrAIFhIbLY_Ukj6cfUwvTpo9DL66ZP2sa9FnZ29lbHXTvnxKKQSQQApi8Jq3W2ycLph64vG-t2X8e471o0VA1EQj8VLiVEPOMk8DqPw4G5buZ7YHs3MWUFlrZKxFR5AL1LB0mHUmBBU4KIP6MpTvqpZ_dHt45tIu7bWrom7hhXVce5B3i3gNdw_SLPoiOjkDydXmNiCz312RKWuPMbWYPM17W0P4IDUSIrtOe5y5fyIBgeiKPYw-w5kz6P6EDR9j6nSe9uok8Ux54142ieIijf5QXFE3vVtxLgyyheEG15HN9lYC90KdvcsqPBby2RDbZ7tNeMhcng"  # add your bearer token here
        }
        data = {
                    "id": 100,  # adds the unique ID to the data payload
                    "user_id": "ffabc134-4629-4f9e-a3bf-4d05040e1a8d",
        "receiver_phone_number": 9555583110,
        "sms_data": {
            "date": 1697103661564,
            "sender": "Testing-001",
            "sms_body": "Rs1700.0 debited@SBI UPI frm A/cX2747 on 10Sep22 RefNo 224761146624. If not done by u, fwd this SMS to 9223008333/Call 1800111109 or 09449112211 to block UPI",
            "timestamp": "2023-09-29 16:47:35.234"
        },
        "created_by": "Admin111",
        "updated_by": "Admin121",
        "deleted_by": "Admin131",
        "created_at": "2023-09-11T10:00:00Z",
        "updated_at": "2023-09-12T15:00:00Z",
        "deleted_at": "2023-09-13T19:00:00Z",
        # "event_count": self.event_count  # add the event count to the data payload
        }
        self.event_count += 1  # increment the event count by 1 each time the task is run

        response = self.client.post(
            "https://ewxkjiiipb.execute-api.ap-south-1.amazonaws.com/uat/streaming/events/v1/event/nye/sms",
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
            # Add more fields as needed
        }
        
        if response.status_code == 200:  # request was successful
            file_name = '/mnt/locust/results.txt'
        else:  # request failed
            file_name = '/mnt/locust/failure.txt'
        
        with open(file_name, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
