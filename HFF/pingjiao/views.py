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

    def get(self, request, *args, **kwargs):
        """At this function, handle the get-method request

        Data: load a form in context
        """
        form = PostUserData()
        context = {self.pj_form_name: form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """At this function, handle the post-method request

        Valid the students' id and their password
        """
        form = PostUserData(resquest.POST)
        if form.is_valid():
            # do pingjiao action, and display the processing in the template
            return HttpResponse('Success!')
        else:
            context = {self.pj_form_name: form}
            return render(request, self.template_name, context)
