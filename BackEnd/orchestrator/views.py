from django.shortcuts import render



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests



from django.http import JsonResponse
from django.views import View
from .wrapper import *
from .fayeemai import *

# Create your views here.

BACKEND3_BASE_URL = "http://192.168.0.106:8000/"



from rest_framework.views import APIView
from rest_framework.response import Response
from .services import handle_custom_course_creation, handle_chat

from .backend1_client import *


class CustomCourseView(APIView):
    def post(self, request):
        return Response(handle_custom_course_creation(request))

class ChatView(APIView):
    def post(self, request):
        return Response(handle_chat(request))



class StudentCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id  # The logged-in user's ID (primary key)

        try:
            # Make request to backend1 to fetch this student's courses
            backend1_url = f"http://<BACKEND1_IP>:<PORT>/get"
            response = requests.get(backend1_url)

            # If backend1 returns success, forward the data
            if response.status_code == 200:
                return Response(response.json(), status=200)
            else:
                return Response({"error": "Failed to get courses from backend1"}, status=response.status_code)

        except requests.exceptions.RequestException:
            return Response({"error": "Connection to backend1 failed"}, status=500)
        

from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .models import StudentProfile






class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        print(password)

        auth_url = f'{BACKEND3_BASE_URL}auth/jwt/create/'
        response = requests.post(auth_url, json={"username": username, "password": password})

        if response.status_code == 200:
            return Response({
                "message": "Login successful",
                "token": response.json().get("access")
            }, status=200)
        else:
            return Response({"error": "Invalid credentials"}, status=response.status_code)


class RegisterView(APIView):
    def post(self, request):
        # Extract user details from the request
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Make a request to the registration service
        register_url = f'{BACKEND3_BASE_URL}auth/users/'
        response = requests.post(register_url, json={"username": username, "password": password, "email": email})

        if response.status_code == 201:
            auth_url = f'{BACKEND3_BASE_URL}auth/jwt/create/'
            response = requests.post(auth_url, json={"username": username, "password": password})

            if response.status_code == 200:
                return Response({
                    "message": "Registration successful. You are now logged in.",
                    "token": response.json().get("access")
                }, status=200)

            # return Response({"message": "Registration successful"}, status=201)
        else:
            return Response({"error": "Registration failed"}, status=response.status_code)
        
class StudentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username  # The logged-in user's username
        userid = request.user.id

        
        print(f"Authenticated student's username: {username}")
        print(f"Authenticated student's ID: {userid}")
        res = get_course_list("user123")
        print(f"Course list: {res.json()}")
        return Response({"username": username}, status=200)
    
    def post(self, request):
        user_id = request.user.id
        username = request.user.username
        email = request.user.email

        # course_id = request.data.get('courseId')
        # score = request.data.get('score')
        # print(f"User ID: {user_id}, Course ID: {course_id}, Score: {score}")

        # Filter the StudentProfile model using the username
        student_profile = StudentProfile.objects.filter(user=request.user).first()

        if not student_profile:
            return Response({"error": "Student profile not found"}, status=404)

        # Perform any additional operations with the student_profile instance here
        # Update the email and level fields of the student_profile
        # new_email = request.data.get('email')
        new_level = request.data.get('class')
        new_name = request.data.get('name')
        # new_points = request.data.get('points')

        if new_name:
            student_profile.name = new_name
        if new_level:
            student_profile.level = int(new_level)
        # if new_points:
        #     student_profile.points = int(new_points)

        # Save the updated student_profile
        student_profile.save()

        return Response({"message": "Score submitted successfully"}, status=200)
    


class AddCourseView(APIView):
    permission_classes = [IsAuthenticated]

    
        

    def post(self, request):
        username = request.user.username  # The logged-in user's username
        user_id = request.user.id  # The logged-in user's ID (primary key)
        thisstudent = StudentProfile.objects.filter(user=request.user).first()


        course_name = request.data.get('title')  # Assuming the course data is sent in the request body
        # course_description = request.data.get('description')
        course_description = ""
        course_subject = request.data.get('subject')

        try:
            # Make request to backend1 to store this student's course
            

            airesponse = course_generator(cl = thisstudent.level, title = course_name, subject=course_subject)
            response = send_course(user_id, str(thisstudent.coursenumber), airesponse)

            thisstudent.coursenumber += 1
            thisstudent.save()

            # backend1_url = f"http://<BACKEND1_IP>:<PORT>/courses/"
            # response = requests.post(backend1_url, json={
            #     "userId": user_id,
            #     "course": course_data
            # })
            # print(airesponse)
            # airesponse_text = airesponse.get('text', 'No response text available')
            # print(f"AI Response Text: {airesponse_text}")

            

            # If backend1 returns success, forward the data
            if response.status_code == 200:
                level = thisstudent.level
                print(f"Student's level: {level}")
                print(f"Course name: {course_name}")
                # airesponse = creating_time_course_generation([course_name],level)
                # print(airesponse)

                return Response(response.json(), status=200)
            else:
                return Response({"error": "Failed to add course in backend1"}, status=response.status_code)
        except requests.exceptions.RequestException:
            return Response({"error": "Connection to backend1 failed"}, status=500)




class CoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        user_id = request.user.id

        # Find the course with the matching ID
        response = get_course_spec(user_id=user_id, course_id=course_id)
        if response.status_code == 200:
            course_data = response.json()
            print(course_data)
            # Assuming the course data is in a field called 'course'
            return JsonResponse(course_data, safe=False)
        else:
            # Handle the case where the course is not found
            return Response({"error": "Course not found"}, status=response.status_code)
        
    def get(self, request, *args, **kwargs):
        user_id = request.user.id  # The logged-in user's ID (primary key)


        course_id = kwargs.get("course_id")
        if course_id:
            response = get_course_spec(user_id=user_id, course_id=str(course_id))
            if response.status_code == 200:
                course_data = response.json()
                course_data = course_data['course']['parent']
                course_data = json.loads(course_data)
                print(course_data)
                # Assuming the course data is in a field called 'course'
                return JsonResponse(course_data, safe=False)
            else:
                # Handle the case where the course is not found
                return Response({"error": "Course not found"}, status=response.status_code)

        response = get_course_list(user_id)
        objectt = response.json()  # Convert the response to a Python object (dictionary or list)
        objectt = objectt['courses']

        
        objects = []

        # objects.append(json.loads(objectt[0]['parent']))
        # objects.append(json.loads(objectt[1]['parent']))
        # print(len(objectt))

        for i in range(len(objectt)):
            objectt[i]['parent'] = json.loads(objectt[i]['parent'])
        
        
        objectt2 = [
            {
                "name":11,
                "subject": "Math",
                "title": "Calculus",
                "description": "An introduction to derivatives, integrals, and the foundational concepts of calculus."
            },{
                "name":12,
                "subject": "Math",
                "title": "Calculus",
                "description": "An introduction to derivatives, integrals, and the foundational concepts of calculus."
            },{
                "name":13,
                "subject": "Math",
                "title": "Calculus",
                "description": "An introduction to derivatives, integrals, and the foundational concepts of calculus."
            },
            
            {

                "name":14,
                "subject": "Science",
                "title": "Physics",
                "description": "Covers motion, forces, energy, and basic mechanics."
            },{
                "name":15,
                "subject": "Science",
                "title": "Physics",
                "description": "Covers motion, forces, energy, and basic mechanics."
            },{
                "name":16,
                "subject": "Science",
                "title": "Physics",
                "description": "Covers motion, forces, energy, and basic mechanics."
            },
            
            
            {

                "name":17,      
                "subject": "Computer Science",
                "title": "Data Structures",
                "description": "Learn about arrays, linked lists, trees, stacks, queues, and more."
            },{
                "name":18,
                "subject": "Computer Science",
                "title": "Data Structures",
                "description": "Learn about arrays, linked lists, trees, stacks, queues, and more."
            },{
                "name":19,
                "subject": "Computer Science",
                "title": "Data Structures",
                "description": "Learn about arrays, linked lists, trees, stacks, queues, and more."
            },

            {

"name":20,                "subject": "English",
                "title": "Creative Writing",
                "description": "Explore storytelling, poetry, and developing your own voice as a writer."
            },{
                "name":21,
                "subject": "English",
                "title": "Creative Writing",
                "description": "Explore storytelling, poetry, and developing your own voice as a writer."
            },{
                "name":22,
                "subject": "English",
                "title": "Creative Writing",
                "description": "Explore storytelling, poetry, and developing your own voice as a writer."
            },

            {

"name":23,                "subject": "History",
                "title": "World War II",
                "description": "A detailed look into the causes, events, and consequences of WWII."
            },{
                "name":24,
                "subject": "History",
                "title": "World War II",
                "description": "A detailed look into the causes, events, and consequences of WWII."
            },{
                "name":25,
                "subject": "History",
                "title": "World War II",
                "description": "A detailed look into the causes, events, and consequences of WWII."
            },
            {
                "name":26,
                "subject": "Biology",
                "title": "Cell Biology",
                "description": "Study the structure and function of cells and cellular components."
            },{
                "name":27,
                "subject": "Biology",
                "title": "Cell Biology",
                "description": "Study the structure and function of cells and cellular components."
            },{
                "name":28,
                "subject": "Biology",
                "title": "Cell Biology",
                "description": "Study the structure and function of cells and cellular components."
            },
            {
                "name":29,
                "subject": "Chemistry",
                "title": "Organic Chemistry",
                "description": "Focus on the structure, properties, and reactions of organic compounds."
            },{
                "name":30,
                "subject": "Chemistry",
                "title": "Organic Chemistry",
                "description": "Focus on the structure, properties, and reactions of organic compounds."
            },{
                "name":31,
                "subject": "Chemistry",
                "title": "Organic Chemistry",
                "description": "Focus on the structure, properties, and reactions of organic compounds."
            },
            {
                "name":32,
                "subject": "Economics",
                "title": "Microeconomics",
                "description": "Introduction to supply and demand, consumer behavior, and market structures."
            },{
                "name":33,
                "subject": "Economics",
                "title": "Microeconomics",
                "description": "Introduction to supply and demand, consumer behavior, and market structures."
            },{
                "name":34,
                "subject": "Economics",
                "title": "Microeconomics",
                "description": "Introduction to supply and demand, consumer behavior, and market structures."
            },
            {
                "name":35,
                "subject": "Philosophy",
                "title": "Ethics",
                "description": "Explore moral theories and ethical dilemmas in modern society."
            },{
                "name":36,
                "subject": "Philosophy",
                "title": "Ethics",
                "description": "Explore moral theories and ethical dilemmas in modern society."
            },{
                "name":37,
                "subject": "Philosophy",
                "title": "Ethics",
                "description": "Explore moral theories and ethical dilemmas in modern society."
            },
            
            
            {

"name":37,                "subject": "Programming",
                "title": "Python Basics",
                "description": "Start programming with Python: syntax, variables, loops, and functions."
            },{
                "name":138,
                "subject": "Programming",
                "title": "Python Basics",
                "description": "Start programming with Python: syntax, variables, loops, and functions."
            },{
                "name":639,
                "subject": "Programming",
                "title": "Python Basics",
                "description": "Start programming with Python: syntax, variables, loops, and functions."
            },
        ]
        return JsonResponse(objectt, safe=False)
    

    
class ChatConvo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id  # The logged-in user's ID (primary key)
        message = request.data.get('message')

        receiver = "ai"
        # timestamp = request.data.get('timestamp')

        # Call the send_chat function from wrapper.py
        response = send_chat(user_id, receiver, message)

        contexts = get_chats(user_id, receiver, 5)
        contexts = contexts.json()
        contexts = contexts['messages']

        message_of_ai = chat_bot(contexts, message)

        receiver = user_id

        response = send_chat(user_id, receiver, message_of_ai)

        airesponse = {
            "message": message_of_ai,
            "sender": "ai",
            "receiver": user_id,
            "timestamp": response.json().get('timestamp')
        }



        if response.status_code == 200:
            return Response(airesponse, status=200)
        else:
            return Response({"error": "Failed to send chat"}, status=response.status_code)

