from django.http import HttpResponse
from web.models import LectureNote, Example

def note_display(request, pk):
	r"""
	Displays the pdf LectureNote file with pk=pk
	"""
    note = LectureNote.objects.get(pk=pk)
    with open(note.file.path, 'r') as file:
        response = HttpResponse(file.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    file.closed
     
	 
def example_display(request, pk):
	r"""
	Displays the pdf Example file with pk=pk
	"""
    example = Example.objects.get(pk=pk)
    with open(example.file.path, 'r') as file:
        response = HttpResponse(file.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    file.closed
     