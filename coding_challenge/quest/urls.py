from django.urls import path
from quest import views

urlpatterns = [
    path('quests/', views.QuestList.as_view(), name='quest-list'),
    path('quests/<int:pk>/', views.QuestDetail.as_view(), name='quest-detail'),
    path('quests/<int:pk>/complete/', views.QuestCompletionList.as_view(), name='quest-complete'),
]
