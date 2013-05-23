from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import Assignment

def index(request):
    assignment_list = Assignment.objects.all()
    context = {'assignment_list': assignment_list}
    return render(request, 'assignment/index.html', context)
