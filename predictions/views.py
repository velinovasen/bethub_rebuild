from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import FormView

from predictions.forms import RegisterForm
from predictions.models import Prediction, BetsVolume, Game, AppUser


def make_prediction_view(request):
    context = {
        "all_games": Game.objects.filter(status='not played', time__gte=now(), date__gte=now()).order_by('date', 'time')
    }
    if request.POST:
        return render(request, 'make_prediction.html', context)
    else:
        return render(request, 'make_prediction.html', context)


def predictions_view(request):
    context = {
        "all_predictions": Prediction.objects.all()
    }
    return render(request, 'predictions.html', context)


def volume_view(request):
    context = {
        "all_volume": BetsVolume.objects.all()
    }
    return render(request, 'volume.html', context)


def results_view(request):
    context = {
        "all_results": Game.objects.filter(status='finished').order_by('-date', '-time')
    }
    return render(request, 'results.html', context)


def check_if_exists(username):
    return User.objects.filter(username=username).exists()


class RegisterView(FormView):
    def test_func(self):
        return not self.request.user.is_authenticated

    template_name = "users/register_form.html"
    form_class = RegisterForm
    success_url = reverse_lazy('predictions')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        messages = []
        flag = True

        if check_if_exists(username):
            messages.append("User already exists!!")
            flag = False
        if password != confirm_password:
            messages.append("Passwords dont match!!")
            flag = False

        if flag:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=email
                                            )
            AppUser.objects.create(user=user,
                                   cash=500
                                   )
        else:
            context = {"messages": messages,
                       "form": form
                       }
            return render(self.request, "users/register_form.html", context)
        return super(RegisterView, self).form_valid(form)
