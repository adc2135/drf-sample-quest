from quest.models import Quest, QuestCompletion 
from quest.serializers import QuestSerializer, QuestCompletionSerializer 
from rest_framework import generics
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone


class QuestList(generics.ListCreateAPIView):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer 

    def get_queryset(self):
        """
        Return Quest if:
            - Quest is onetime AND:
                - was completed on requested day 
                OR
                - has not yet been completed
            OR
            - Quest is scheduled for requested day AND:
                - was completed on requested day 
                OR
                - has not yet been completed on requested day 
        """     
 
        date = self.request.query_params.get('date')
        date = datetime.strptime(date, '%Y-%m-%d') if date else datetime.today().date()

        search_year= date.year
        search_month = date.month
        search_week = date.isocalendar().week
        search_day = date.day
        search_weekday = date.isoweekday()

        onetime = Q(scheduled=False)
        currently_scheduled = ( 
            Q(quest_schedule__repeat_year=search_year) | Q(quest_schedule__repeat_year='*') &
            Q(quest_schedule__repeat_month=search_month) | Q(quest_schedule__repeat_month='*') &
            Q(quest_schedule__repeat_week=search_week) | Q(quest_schedule__repeat_week='*') &
            Q(quest_schedule__repeat_day=search_day) | Q(quest_schedule__repeat_day='*') &
            Q(quest_schedule__repeat_day=search_day) | Q(quest_schedule__repeat_day='*') &
            Q(quest_schedule__repeat_weekday=search_weekday) | Q(quest_schedule__repeat_weekday='*')
        )
        completed_today = Q(questcompletion__create_time__date=date)
        not_yet_completed  = Q(questcompletion__create_time__isnull=True)
        
        return Quest.objects.filter((onetime & (not_yet_completed | completed_today)) | 
                                    (currently_scheduled))


class QuestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer 


class QuestCompletionList(generics.CreateAPIView):
    serializer_class = QuestCompletionSerializer

    def perform_create(self, serializer):
        serializer.save(quest_id=self.kwargs.get('pk'))
 
