from django.db import models

from django.db import models


class RevisionSession(models.Model):

    SESSION_STATUS = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ABANDONED', 'Abandoned'),
    ]

    SESSION_MODE = [
        ('SCHEDULED', 'Scheduled'),
        ('TOPIC_PRACTICE', 'Topic Practice'),
        ('MIXED', 'Mixed'),
    ]

    session_id = models.AutoField(primary_key=True)

    user_id = models.IntegerField()

    started_at = models.DateTimeField(auto_now_add=True)

    ended_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=SESSION_STATUS,
        default='IN_PROGRESS'
    )

    session_mode = models.CharField(
        max_length=20,
        choices=SESSION_MODE
    )

    topic_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Revision Session {self.session_id}"
# Create your models here.
