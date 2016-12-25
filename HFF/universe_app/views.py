from django.shortcuts import render
from django.views.generic.base import View


# Create your views here.
class IndexView(View):
    """This view-function implements display some block-href to differ block,
    such as pingjiao-block(or pingjiao app)
    """

    template_name = 'universe_app/welcome.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
