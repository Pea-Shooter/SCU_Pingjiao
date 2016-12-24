from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic.base import View
from .forms import PostUserData


# Create your views here.
class PJView(View):
    """Show the pingjiao's main page
    """

    template_name = 'pingjiao/mainpage.html'
    pj_form_name = 'pj_form'
    introduce = '''
    This is a simple Ping Jiao system, you just need enter your 
    stuent id and password, then you can finish your comment task at 
    a momment of one-click!
    '''
    courses = ['Math', 'Computer Networks', 'Database System Principle']
    context = {'introduce': introduce}

    def get(self, request, *args, **kwargs):
        """At this function, handle the get-method request

        Data: load a form in context
        """
        form = PostUserData()
        self.context[self.pj_form_name] = form
        self.context['course_list'] = self.courses
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        """At this function, handle the post-method request

        Valid the students' id and their password
        """
        form = PostUserData(request.POST)
        if form.is_valid():
            # do pingjiao action, and display the processing in the template
            return HttpResponse('Success!')
        else:
            self.context[self.pj_form_name] = form
            return render(request, self.template_name, self.context)
