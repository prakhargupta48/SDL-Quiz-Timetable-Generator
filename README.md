Django Class Timetable to Quiz Timetable Project
Overview
This Django project allows users to upload a class timetable in image format. The timetable consists of three tables:

Main Timetable (Monday to Saturday): Each cell includes:
Subject Code
Faculty Name (short form)
Class/Lab Location
Batch Names (e.g., A1, A2, B1, B2)
Subject Code Table: Maps subject codes to subject names.
Faculty List: Maps short-form faculty names to full names.
The system extracts this data from the image, stores it in the database, and generates a quiz timetable based on the class timetable. Quizzes are scheduled to take place on a single day with specific constraints on the number of quizzes per day, their duration, and the allocation of invigilators.

Features
Data Extraction: Extracts data from an image using Tesseract OCR and other image-processing libraries.
Data Storage: Stores the extracted timetable data using Django models for future retrieval.
Multiple Uploads: Tracks and manages multiple timetable uploads using an UploadSession model.
Quiz Timetable Creation: Generates a quiz timetable with the following details:
S.No.: Serial number of the quiz.
Subject: Concatenated subject code and name.
Quiz Date: Date of the quiz.
Quiz Time: Time of the quiz (quizzes last 15 minutes).
Invigilators: Names of two invigilators who do not have classes during the quiz time.
Project Setup
Prerequisites
Python 3.x
Django 4.x
Virtual environment (for dependency isolation)
Required libraries: opencv-python, numpy, pytesseract, pandas, openpyxl, Pillow
Installation Steps
Clone the Repository:


git clone <repository-url>
cd <project-folder>
Set Up Virtual Environment:
python -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate

Install Dependencies:
pip install -r requirements.txt

Run Migrations:
python manage.py migrate

Run the Django Development Server:
python manage.py runserver
Access the Application: Open a browser and go to http://127.0.0.1:8000/.

Usage

Uploading Timetables:
Navigate to the upload page.
Upload a class timetable image (in JPG/PNG format) containing the Main Timetable, Subject Code Table, and Faculty List.
The system will process the image and store the extracted data.

Generating the Quiz Timetable:
Once the timetable data is processed, navigate to the quiz scheduling page.
Enter the required details (such as the quiz date).
The system will generate a quiz timetable, ensuring that no more than 5 quizzes are scheduled per day, and each quiz is 15 minutes long.
The timetable will also list two invigilators for each quiz, ensuring they are free during the quiz time.
Models
MainTimetableEntry: Stores each entry from the Main Timetable (subject code, faculty name, class location, etc.).
Subject: Stores subject codes and their corresponding names.
Faculty: Stores faculty short names and their full names.
UploadSession: Tracks each upload session to manage multiple timetable uploads.
Constraints
Quiz Duration: Each quiz lasts for 15 minutes.
Max Quizzes per Day: No more than 5 quizzes can be scheduled per day.
Invigilator Assignment: Invigilators are chosen from faculty members who do not have any classes during the quiz time.
Tech Stack
Backend: Django (Python)
Database: SQLite (default, can be changed to PostgreSQL or MySQL)
Image Processing: Tesseract OCR, OpenCV, Pillow
Dependencies
Django
OpenCV
Tesseract OCR
Numpy
Pandas
Openpyxl
Pillow
