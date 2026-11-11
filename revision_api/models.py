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



class Question(models.Model):

    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('SHORT_ANSWER', 'Short Answer'),
        ('TRUE_FALSE', 'True or False'),
    ]

    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    question_id = models.AutoField(primary_key=True)

    topic_id = models.IntegerField()

    question_text = models.TextField()

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default='MCQ'
    )

    options_json = models.JSONField(
        null=True,
        blank=True
    )

    correct_answer = models.TextField()

    explanation = models.TextField(
        null=True,
        blank=True
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_LEVELS,
        default='Easy'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text[:50]


class AnswerAttempt(models.Model):

    attempt_id = models.AutoField(primary_key=True)

    user_id = models.IntegerField()

    session = models.ForeignKey(
        RevisionSession,
        on_delete=models.CASCADE,
        related_name='answer_attempts'
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answer_attempts'
    )

    selected_answer = models.TextField()

    is_correct = models.BooleanField()

    time_taken = models.FloatField(
        help_text="Time taken to answer in seconds"
    )

    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user_id} - Question {self.question_id}"