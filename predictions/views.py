from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import FormView

from predictions.forms import RegisterForm, UserPredictionForm, UpdateUserPredictionForm
from predictions.models import Prediction, BetsVolume, Game, AppUser, UserPrediction


def make_prediction_view(request):
    context = {
        "all_games": Game.objects.filter(status='not played', time__gte=now(), date__gte=now()).order_by('date', 'time')
    }
    if request.POST:
        form = UserPredictionForm(request.POST)
        print('gore da')
        if form.is_valid():
            print('i vutre da')
            game_id = form.cleaned_data['game_id']
            game = Game.objects.filter(pk=game_id)[0]
            creator = AppUser.objects.get(user=request.user)
            date_time = str(game).split(' | ')[0]
            date, time = date_time.split(' ')
            home_team = form.cleaned_data['home_team']
            away_team = form.cleaned_data['away_team']
            sign = form.cleaned_data['sign']
            odd = form.cleaned_data['odd']
            thoughts = form.cleaned_data['thoughts']
            print('VSICHKO 6')
            UserPrediction.objects.create(game=game, creator=creator, home_team=home_team,
                                          away_team=away_team, sign=sign, odd=odd, thoughts=thoughts)
        else:
            print(form.errors)
        return render(request, 'make_prediction.html', context)

    else:
        return render(request, 'make_prediction.html', context)


def my_predictions_view(request):
    creator = AppUser.objects.get(user=request.user)
    context = {
        "all_predictions": UserPrediction.objects.filter(creator=creator)
    }
    if request.POST:
        form = UpdateUserPredictionForm(request.POST)
        print('gore da')
        if form.is_valid():
            print(form)
            my_prediction = UserPrediction.objects.filter(pk=form.cleaned_data['game_id'])[0]
            print(my_prediction)
            my_prediction.thoughts = form.cleaned_data['thoughts']
            my_prediction.save()
            return render(request, 'my_predictions.html', context)

    return render(request, 'my_predictions.html', context)


def delete_prediction_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(UserPrediction, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/my_predictions/")

    return render(request, "my_predictions.html", context)


def guest_view(request):
    context = {
        "all_games": Game.objects.filter(status='not played', time__gte=now(), date__gte=now()).order_by('date', 'time')
    }
    return render(request, 'guest_home.html', context)


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
