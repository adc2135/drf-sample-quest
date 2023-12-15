from quest.models import Quest, QuestSchedule, QuestCompletion
from rest_framework import serializers

from django.db.models import Q
from datetime import datetime
from django.utils import timezone

class QuestCompletionSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestCompletion
        # TODO: figure out how to make posts with no payload
        fields = [] 


class QuestScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestSchedule
        fields = ['repeat_year', 'repeat_month', 'repeat_week', 'repeat_day', 'repeat_weekday'] 


class QuestSerializer(serializers.ModelSerializer):
    quest_schedule =  QuestScheduleSerializer(many=True)
    completed = serializers.SerializerMethodField()


    class Meta:
        model = Quest 
        fields = ['id', 'title', 'description', 'scheduled', 'quest_schedule', 'completed']

    def get_completed(self, obj):

        date = self.context['request'].query_params.get('date')
        date = datetime.strptime(date, '%Y-%m-%d') if date else timezone.now().today().date()

        if obj.questcompletion_set.count() == 0:
            return False
        elif obj.scheduled == True and obj.questcompletion_set.latest('create_time').create_time.date() != date:
            return False
        return True

    def create(self, validated_data):
        quest_schedule_data = validated_data.pop('quest_schedule')
        quest = Quest.objects.create(**validated_data)
        for qsd in quest_schedule_data:
            QuestSchedule.objects.create(quest=quest, **qsd)
        return quest 
