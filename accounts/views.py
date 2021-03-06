from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse

from quiz.models import Quiz
from .forms import SignUpForm


def handle_404(request, exception=None):
    template = loader.get_template('404.html')
    return HttpResponse(template.render({}, request), status=404)


@login_required(login_url='/login')
def home(request):
    quizzes = Quiz.objects.order_by('-total')[:10]
    template = loader.get_template('index.html')
    context = {
        'quizzes': quizzes
    }
    return HttpResponse(template.render(context, request))


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    template = loader.get_template('accounts/signup.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))
