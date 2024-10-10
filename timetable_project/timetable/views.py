

import cv2
import numpy as np
import pytesseract
from django.shortcuts import render, redirect
from django.views import View
from .models import UploadSession, Subject, Faculty, MainTimetableEntry, QuizTimetable
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from django.utils import timezone
    
class UploadTimetableView(View):
    def get(self, request):
        return render(request, 'upload_timetable.html')

    def post(self, request):
        if 'timetable_image' not in request.FILES:
            return render(request, 'upload_timetable.html', {'error': 'No file uploaded'})

        image_file = request.FILES['timetable_image']
        image_array = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        
        upload_session = UploadSession.objects.create(description=f"Upload on {timezone.now()}")

    
        main_timetable, subjects, faculty = self.extract_data_from_image(image)

        
        self.save_data_to_database(main_timetable, subjects, faculty, upload_session)

        
        self.generate_quiz_timetable(upload_session)

        return redirect('view_timetable', session_id=upload_session.id)

    def extract_data_from_image(self, image):
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        
        threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        
        text = pytesseract.image_to_string(threshold)

        
        lines = text.split('\n')

        
        main_timetable = []
        subjects = []
        faculty = []

        
        current_section = None
        for line in lines:
            if 'Main Timetable' in line:
                current_section = 'main_timetable'
            elif 'Subject Code Table' in line:
                current_section = 'subjects'
            elif 'Faculty List' in line:
                current_section = 'faculty'
            elif line.strip(): 
                if current_section == 'main_timetable':
                    main_timetable.append(line.split())
                elif current_section == 'subjects':
                    subjects.append(line.split())
                elif current_section == 'faculty':
                    faculty.append(line.split())

        return main_timetable, subjects, faculty

    def save_data_to_database(self, main_timetable, subjects, faculty, upload_session):
    
        for subject in subjects:
            if len(subject) >= 2:
                Subject.objects.create(
                    code=subject[0],
                    name=' '.join(subject[1:]),
                    upload_session=upload_session
                )

        
        for f in faculty:
            if len(f) >= 2:
                Faculty.objects.create(
                    short_name=f[0],
                    full_name=' '.join(f[1:]),
                    upload_session=upload_session
                )

        
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        for entry in main_timetable:
            if len(entry) >= 6:
                day = entry[0]
                time_slot = entry[1]
                subject_code = entry[2]
                faculty_short_name = entry[3]
                location = entry[4]
                batch = entry[5]

                subject = Subject.objects.filter(code=subject_code, upload_session=upload_session).first()
                faculty = Faculty.objects.filter(short_name=faculty_short_name, upload_session=upload_session).first()

                if subject and faculty and day in days:
                    MainTimetableEntry.objects.create(
                        day=day,
                        time_slot=time_slot,
                        subject=subject,
                        faculty=faculty,
                        location=location,
                        batch=batch,
                        upload_session=upload_session
                    )

    def generate_quiz_timetable(self, upload_session):
        
        subjects = Subject.objects.filter(upload_session=upload_session)
        faculty = Faculty.objects.filter(upload_session=upload_session)

        for i, subject in enumerate(subjects[:5]):  
            quiz_date = timezone.now() + timezone.timedelta(days=i)
            quiz_time = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)

            QuizTimetable.objects.create(
                subject=subject,
                date=quiz_date,
                time=quiz_time,
                invigilator1=faculty[i % len(faculty)],
                invigilator2=faculty[(i+1) % len(faculty)],
                upload_session=upload_session
            )



class ViewTimetableView(View):
    def get(self, request, session_id):
        upload_session = UploadSession.objects.get(id=session_id)
        main_timetable = MainTimetableEntry.objects.filter(upload_session=upload_session)
        subjects = Subject.objects.filter(upload_session=upload_session)
        faculty = Faculty.objects.filter(upload_session=upload_session)
        quiz_timetable = QuizTimetable.objects.filter(upload_session=upload_session)

        context = {
            'main_timetable': main_timetable,
            'subjects': subjects,
            'faculty': faculty,
            'quiz_timetable': quiz_timetable,
        }

        return render(request, 'view_timetable.html', context)

class DownloadQuizTimetableView(View):
    def get(self, request, session_id):
        upload_session = UploadSession.objects.get(id=session_id)
        quiz_timetable = QuizTimetable.objects.filter(upload_session=upload_session)

        
        data = []
        for quiz in quiz_timetable:
            data.append({
                'S.No.': quiz.id,
                'Subject': f"{quiz.subject.code} - {quiz.subject.name}",
                'Date': quiz.date,
                'Time': quiz.time,
                'Invigilator 1': quiz.invigilator1.full_name,
                'Invigilator 2': quiz.invigilator2.full_name,
            })

        df = pd.DataFrame(data)

       
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Quiz Timetable')

       
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=quiz_timetable_{session_id}.xlsx'
        response.write(output.getvalue())

        return response