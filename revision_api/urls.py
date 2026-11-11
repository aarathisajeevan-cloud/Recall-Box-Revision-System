from django.urls import path
from . import views

urlpatterns = [
    path('start-session/',views.start_revision_session,name='start_revision_session'),
    path('save-questions/', views.save_questions, name='save_questions'),
    path('get-questions/',views.get_questions,name='get_questions'),
    path('save-answer/',views.save_answer_attempt,name='save_answer_attempt'),
    
]