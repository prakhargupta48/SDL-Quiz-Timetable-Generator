from django.urls import path
from django.shortcuts import redirect
from .views import UploadTimetableView, ViewTimetableView, DownloadQuizTimetableView

urlpatterns = [
    path('', lambda request: redirect('upload_timetable'), name='timetable_home'),  # Redirect to upload page
    path('upload/', UploadTimetableView.as_view(), name='upload_timetable'),
    path('view/<int:session_id>/', ViewTimetableView.as_view(), name='view_timetable'),
    path('download_quiz/<int:session_id>/', DownloadQuizTimetableView.as_view(), name='download_quiz_timetable'),
]

