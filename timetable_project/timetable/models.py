

from django.db import models

class UploadSession(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    upload_session = models.ForeignKey(UploadSession, on_delete=models.CASCADE)

class Faculty(models.Model):
    short_name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=255)
    upload_session = models.ForeignKey(UploadSession, on_delete=models.CASCADE)

class MainTimetableEntry(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
    ]
    
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    time_slot = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    batch = models.CharField(max_length=20)
    upload_session = models.ForeignKey(UploadSession, on_delete=models.CASCADE)

class QuizTimetable(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    invigilator1 = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='invigilator1')
    invigilator2 = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='invigilator2')
    upload_session = models.ForeignKey(UploadSession, on_delete=models.CASCADE)