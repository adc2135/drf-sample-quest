from django.db import models


class Quest(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(max_length=100)
    description = models.TextField(max_length=150, null=True)
    scheduled = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)


class QuestSchedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    quest = models.ForeignKey(Quest, related_name='quest_schedule',
                              on_delete=models.RESTRICT)
    repeat_year = models.CharField(default='*', max_length=10)
    repeat_month = models.CharField(default='*', max_length=10)
    repeat_week = models.CharField(default='*', max_length=10)
    repeat_day = models.CharField(default='*', max_length=10)
    repeat_weekday = models.CharField(default='*', max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)


class QuestCompletion(models.Model):
    id = models.BigAutoField(primary_key=True)
    quest = models.ForeignKey(Quest, on_delete=models.RESTRICT)
    create_time = models.DateTimeField(auto_now_add=True)
