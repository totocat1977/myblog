from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from db.models import MyUser
from .forms import MyUserCreationForm
from django.http import JsonResponse, HttpResponseRedirect
from captcha.models import CaptchaStore
from db.models import MyUser
from captcha.helpers import captcha_image_url
from django.urls import reverse_lazy


# Create your views here.
class_left_side = "col-sm-5"
class_right_side = "col-sm-5 col-sm-offset-2"


def get_side_class():
    return {'left_side':class_left_side,
            'right_side':class_right_side
    }


'''
def user_create(request, template_name='user/user_reg.html'):
    form = UserForm(request.POST or None)
    
    context = {}
    context['form'] = form 
    title = "SignUp - William's Blog"
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    
    context['title'] = title
    context['hashkey'] = hashkey
    context['image_url'] = image_url
    context['side_class'] = get_side_class()
        
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('articles:index'))
    return render(request, template_name, context)
'''


class UserCreation(CreateView):
    # model = MyUser
    template_name = 'user/user_reg.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('articles:index')

    def get_context_data(self, *args, **kwargs):
        context = super(UserCreation, self).get_context_data(**kwargs)
        title = "SignUp - William's Blog"
        # hashkey = CaptchaStore.generate_key()
        # image_url = captcha_image_url(hashkey)

        context['title'] = title
        # context['hashkey'] = hashkey
        # context['image_url'] = image_url
        context['side_class'] = get_side_class()

        return context


'''
    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")
'''


def ajax_val(request):
    if request.is_ajax():
        fieldflag = request.GET['field']
        if fieldflag == "captcha":
            cs = CaptchaStore.objects.filter(response=request.GET['response'], hashkey=request.GET['hashkey'])
        elif fieldflag == "username":
            cs = MyUser.objects.filter(username=request.GET['username'])
        elif fieldflag == "email":
            cs = MyUser.objects.filter(mbu_email=request.GET['email'])

        if cs:
            json_data = {'status': 1}
        else:
            json_data = {'status': 0}

        return JsonResponse(json_data)
    else:
        # raise Http404
        json_data = {'status': 0}
        return JsonResponse(json_data)


'''
def ajax_check_user(request):
    if request.is_ajax():
        check = MyUser.objects.filter(username=request.GET['username'])
        if check:
            json_data = {'status': 1}
        else:
            json_data = {'status': 0}

        return JsonResponse(json_data)
    else:
        json_data = {'status': 0}
        return JsonResponse(json_data)
'''


