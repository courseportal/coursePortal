from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import Assignment

def index(request):
    assignment_list = Assignment.objects.all()
    context = {'assignment_list': assignment_list}
    return render(request, 'assignment/index.html', context)

def detail(request, id):
    assignment = Assignment.objects.get(pk=id)
    question_list = assignment.questions.all()
    context = {
        'question_list': question_list,
        'assigned':assignment,
    }
    return render(request, 'assignment/detail.html', context)
