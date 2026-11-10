from django.urls import path
from . import views

urlpatterns = [
    path('start-session/',views.start_revision_session,name='start_revision_session'),
    path('save-questions/', views.save_questions, name='save_questions'),
    
]