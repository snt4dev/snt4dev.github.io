from django.views.generic import RedirectView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime

import os
import uuid
import json
import io

from .utils import get_client_ip

class RedirectToHome(RedirectView):
    permanent = False
    query_string = True
    pattern_name = "home_view"
    
class HomeView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get(self, request, *args, **kwargs):
        return HttpResponse('Home Page')
    
class SubmissionView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get(self, request, *args, **kwargs):
        return HttpResponse('Get All Submission')
    
    def create_submission(self):
        submission_id = str(uuid.uuid4())
        return submission_id
    
    def save_data(self, submission_id, query_dict):
        now = datetime.now()
        try:
            ip = get_client_ip(self.request)
        except Exception as e:
            ip = 'N/A'
        query_dict_flattened = {
            'ipAddress': ip,
            'submissionDate': now.strftime("%d/%m/%Y %H:%M:%S"),
        }
        for key in query_dict.keys():
            value = query_dict.getlist(key)
            query_dict_flattened[key] = value if len(value) > 1 else value[0]
        json_data = json.dumps(query_dict_flattened, indent=4)
        json_bytes = json_data.encode('utf-8')
        json_file = io.BytesIO(json_bytes)
        location = settings.BASE_DIR / f'submissions/{submission_id}'
        fs = FileSystemStorage(location=location)
        fs.save(f'{submission_id}.json', json_file)
        
    def upload(self, submission_id, file):
        location = settings.BASE_DIR / f'submissions/{submission_id}'
        fs = FileSystemStorage(location=location) 
        fs.save(f'{submission_id}_{file.name}', file)
    
    def post(self, request, *args, **kwargs):
        submission_id = self.create_submission()
        self.save_data(submission_id, request.POST)
        for key in request.FILES.keys():
            files = request.FILES.getlist(key)
            for file in files:
                self.upload(submission_id, file)
        return redirect("http://127.0.0.1:8002/thank-you.html")

