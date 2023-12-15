# Django Rest Framework Example: Scheduled Quests

## Setup
### Create and Activate Virtual Environment
```python -m venv venv```

```source venv/bin/activate```
### Install requirements.txt
```pip install -r requirements.txt```

## Testing
### Run Unit Tests
```./manage.py test```

## Run Development Server
### Run Migrations
```./manage.py migrate```
### Start Development Server
```./manage.py runserver```

## Overview
### Creating Quests
You can create quests by making posts to the quests endpoint.  Quests can be either one-time or scheduled.  To create a one-time quest, post a quest object with an empty `quest_schedule` and `scheduled` set to false.  Scheduled quests can be created by posting a quest object with a `quest_schedule` array and `scheduled` set to true.  `quest_schedule` is an array of schedules. Schedules are described by 6 fields: `repeat_year` ('2023', '*', etc.), `repeat_month` ('1', '12', '*', etc.), `repeat_week` ('1', '5', '*', etc.), `repeat_day` ('4', '*', etc.), and `repeat_weekday` ('1', '7', etc.).  A curl request to create a quest that repeats every Friday in December would look like the following:
```
curl -d '{
    "title": "asdfasdfadsf",
    "description": "asdfasdfasdf",
    "scheduled": true,
    "quest_schedule": [
        {
            "repeat_year": "*",
            "repeat_month": "12",
            "repeat_week": "*",
            "repeat_day": "*",
            "repeat_weekday": "4"
        }
    ]
}' -H "Content-Type: application/json" -X POST localhost:8000/quests/ 
```

### Retrieving Quests
Retrieve quests from the quests endpoint with a get.  If the query parameter `date` is passed (e.g. '2023-01-01') quests that are scheduled or were completed on that date are returned.  If no date is passed the endpoint will default to the current date.  A curl request to get all quests active or completed on 2024-01-01 would look like the following:
```
curl "localhost:8000/quests/?date=2024-01-01"
```

 ### Completing Quests
 Quests can be completed by making an empty post to `quests/\<quest-id\>/complete/`` e.g.
 
 ```curl -X POST localhost:8000/quests/11/complete/```


