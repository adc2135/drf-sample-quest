from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase
from quest.models import Quest 
from datetime import datetime, timedelta


class Tests(APITransactionTestCase):


    def test_complete_onetime_quest(self):
        quest_list_url = reverse('quest-list')

        data = {
            'title': 'Title',
            'description': 'Description',
            'scheduled': False,
            'quest_schedule': []
        }

        # create a quest
        response = self.client.post(quest_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json()['title'], 'Title')
        self.assertEqual(response.json()['description'], 'Description')
        self.assertEqual(response.json()['scheduled'], False)
        self.assertEqual(response.json()['quest_schedule'], [])
        self.assertEqual(response.json()['completed'], False)

        # retrieve a quest
        response = self.client.get(quest_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]['title'], 'Title')
        self.assertEqual(response.json()[0]['description'], 'Description')
        self.assertEqual(response.json()[0]['scheduled'], False)
        self.assertEqual(response.json()[0]['quest_schedule'], [])
        self.assertEqual(response.json()[0]['completed'], False)

        # complete a quest
        quest_complete_url = reverse('quest-complete', args=[response.json()[0]['id']])
        response = self.client.post(quest_complete_url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # retrieve a quest; verify quest was completed
        response = self.client.get(quest_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]['title'], 'Title')
        self.assertEqual(response.json()[0]['description'], 'Description')
        self.assertEqual(response.json()[0]['scheduled'], False)
        self.assertEqual(response.json()[0]['quest_schedule'], [])
        self.assertEqual(response.json()[0]['completed'], True)

    def test_complete_daily_scheduled_quest(self):
        quest_list_url = reverse('quest-list')

        data = {
            'title': 'Title',
            'description': 'Description',
            'scheduled': True,
            'quest_schedule': [ 
                {
                    'repeat_year': '*',
                    'repeat_month': '*',
                    'repeat_week': '*',
                    'repeat_day': '*', 
                    'repeat_weekday': '*'
                }
            ]
        }

        # create a quest
        response = self.client.post(quest_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json()['title'], 'Title')
        self.assertEqual(response.json()['description'], 'Description')
        self.assertEqual(response.json()['scheduled'], True)
        self.assertEqual(response.json()['quest_schedule'], data['quest_schedule'])
        self.assertEqual(response.json()['completed'], False)

        # retrieve today's quests
        today = datetime.now()
        response = self.client.get(quest_list_url, {'date': today.strftime('%Y-%m-%d')}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]['title'], 'Title')
        self.assertEqual(response.json()[0]['description'], 'Description')
        self.assertEqual(response.json()[0]['scheduled'], True)
        self.assertEqual(response.json()[0]['quest_schedule'], data['quest_schedule'])
        self.assertEqual(response.json()[0]['completed'], False)

        # complete a quest
        quest_complete_url = reverse('quest-complete', args=[response.json()[0]['id']])
        response = self.client.post(quest_complete_url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # retrieve a quest; verify quest was completed
        response = self.client.get(quest_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]['title'], 'Title')
        self.assertEqual(response.json()[0]['description'], 'Description')
        self.assertEqual(response.json()[0]['scheduled'], True)
        self.assertEqual(response.json()[0]['quest_schedule'], data['quest_schedule'])
        self.assertEqual(response.json()[0]['completed'], True)

        # verify yesterday's daily quest is still incomplete 
        yesterday = today - timedelta(days=1)
        response = self.client.get(quest_list_url, {'date': yesterday.strftime('%Y-%m-%d')}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]['title'], 'Title')
        self.assertEqual(response.json()[0]['description'], 'Description')
        self.assertEqual(response.json()[0]['scheduled'], True)
        self.assertEqual(response.json()[0]['quest_schedule'], data['quest_schedule'])
        self.assertEqual(response.json()[0]['completed'], False)

        # verify tomorrow's daily quest is still incomplete 
        tomorrow = today + timedelta(days=1)
        response = self.client.get(quest_list_url, {'date': tomorrow.strftime('%Y-%m-%d')}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]['title'], 'Title')
        self.assertEqual(response.json()[0]['description'], 'Description')
        self.assertEqual(response.json()[0]['scheduled'], True)
        self.assertEqual(response.json()[0]['quest_schedule'], data['quest_schedule'])
        self.assertEqual(response.json()[0]['completed'], False)

    def test_complete_weekday_scheduled_quest(self):
        quest_list_url = reverse('quest-list')
        today = datetime.now()

        data = {
            'title': 'Title',
            'description': 'Description',
            'scheduled': True,
            'quest_schedule': [ 
                {
                    'repeat_year': '*',
                    'repeat_month': '*',
                    'repeat_week': '*',
                    'repeat_day': '*', 
                    'repeat_weekday': str(today.isoweekday())
                }
            ]
        }

        # create a quest
        response = self.client.post(quest_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.json()['title'], 'Title')
        self.assertEqual(response.json()['description'], 'Description')
        self.assertEqual(response.json()['scheduled'], True)
        self.assertEqual(response.json()['quest_schedule'], data['quest_schedule'])
        self.assertEqual(response.json()['completed'], False)

        # retrieve yesterday's quests. there shouldn't be any
        yesterday = today - timedelta(days=1)
        response = self.client.get(quest_list_url, {'date': yesterday.strftime('%Y-%m-%d')}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
       
        # retrieve today's quests. there should be one 
        response = self.client.get(quest_list_url, {'date': today.strftime('%Y-%m-%d')}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]['title'], 'Title')
        self.assertEqual(response.json()[0]['description'], 'Description')
        self.assertEqual(response.json()[0]['scheduled'], True)
        self.assertEqual(response.json()[0]['quest_schedule'], data['quest_schedule'])
        self.assertEqual(response.json()[0]['completed'], False)

        # complete the quest
        quest_complete_url = reverse('quest-complete', args=[response.json()[0]['id']])
        response = self.client.post(quest_complete_url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # retrieve the quest; verify quest was completed
        response = self.client.get(quest_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.json()[0]['title'], 'Title')
        self.assertEqual(response.json()[0]['description'], 'Description')
        self.assertEqual(response.json()[0]['scheduled'], True)
        self.assertEqual(response.json()[0]['quest_schedule'], data['quest_schedule'])
        self.assertEqual(response.json()[0]['completed'], True)
