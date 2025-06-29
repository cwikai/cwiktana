import logging
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import subprocess

logger = logging.getLogger(__name__)

def run_ollama_mistral(question):
    try:
        result = subprocess.run(
            ['ollama', 'run', 'mistral'],
            input=question,
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "Sorry, I couldn't get an answer right now."
    except Exception as e:
        logger.error(f"run_ollama_mistral error: {e}")
        return f"Error: {str(e)}"


@method_decorator(csrf_exempt, name='dispatch')
class SupportAPIView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = None

    def get(self, request):
        return JsonResponse({'message': 'Support API is live. Please POST a question.'})

    def post(self, request):
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip().lower()
            logger.info(f"Received question: {question}")

            if not question:
                return JsonResponse({'answer': "Please ask something."})

            FAQ_ANSWERS = {
                "how do i register": "To register, click the Register link on the homepage and fill out the form.",
                "how do i reset my password": "You can reset your password on the login page by clicking 'Forgot Password?'.",
                "what is marshalsync": "MarshalSync is your martial arts club management platform, helping you manage members, classes, gradings, and more.",
                "how do i contact support": "You can contact support by emailing support@marshalsync.com or using the chatbot here.",
            }

            if question in FAQ_ANSWERS:
                answer = FAQ_ANSWERS[question]
                logger.info(f"FAQ answer used: {answer}")
                return JsonResponse({'answer': answer})

            context = """
You are Bot Grand Master, the expert AI assistant for MarshalSync, a comprehensive martial arts club and membership management platform.

MarshalSync is designed to help martial arts clubs and instructors manage their entire club operations smoothly and efficiently. It offers these key features:

1. Member Management:
   - Register new members with secure profiles.
   - Track member details including personal info, contact, and membership status.
   - Manage member subscriptions, payments, and renewals.

2. Class Scheduling and Attendance:
   - Create and manage class schedules.
   - Track attendance for each class session.
   - Assign instructors and venues for classes.

3. Grading Management:
   - Record student gradings and belt promotions.
   - Generate grading sheets and certificates.
   - Keep a history of all gradings per member.

4. License Management:
   - Manage licenses and certifications for members and instructors.
   - Track expiry and renewal of licenses.

5. User Accounts and Security:
   - Secure login and user authentication.
   - Role-based access for instructors, admins, and members.
   - Two-factor authentication support.

6. Dashboards and Reporting:
   - Provide club admins with dashboard views of key metrics.
   - Generate reports on attendance, memberships, grading, and finances.

Your job is to answer questions about how to use MarshalSync features, troubleshoot common issues, and guide users on best practices for managing their martial arts club with MarshalSync.

Always provide clear, helpful, and friendly answers.
"""

            full_prompt = context + "\nUser asks: " + question

            result = subprocess.run(
                ['ollama', 'run', 'mistral'],
                input=full_prompt,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=120
            )

            if result.returncode != 0:
                logger.error(f"Ollama returned non-zero exit code: {result.returncode}")
                return JsonResponse({'answer': 'Bot Grand Master is having trouble thinking right now.'})

            output = result.stdout.strip()
            logger.info(f"AI response: {output}")
            return JsonResponse({'answer': output})

        except Exception as e:
            logger.error(f"SupportAPIView error: {e}")
            return JsonResponse({'answer': f'Error: {str(e)}'})
