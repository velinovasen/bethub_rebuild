from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from bethub import settings

UserModel = get_user_model()


class Prediction(models.Model):
    date = models.DateField()
    time = models.TimeField()
    home_team = models.CharField(max_length=40)
    away_team = models.CharField(max_length=40)
    home_prob = models.IntegerField()
    draw_prob = models.IntegerField()
    away_prob = models.IntegerField()
    bet_sign = models.CharField(max_length=1)
    score_predict = models.CharField(max_length=10)
    avg_goals = models.FloatField()
    odds_for_prediction = models.FloatField()
    home_odd = models.FloatField()
    draw_odd = models.FloatField()
    away_odd = models.FloatField()
    temp = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.home_team} - {self.away_team} ' \
               f'{self.home_prob} {self.draw_prob} {self.away_prob} --- ' \
               f'{self.bet_sign}'


class BetsVolume(models.Model):
    day = models.CharField(max_length=15)
    time = models.TimeField()
    home_team = models.CharField(max_length=60)
    away_team = models.CharField(max_length=60)
    final_bet = models.CharField(max_length=1)
    odds = models.FloatField()
    amount = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.home_team} - {self.away_team} - ' \
               f'{self.final_bet} - {self.odds} - {self.amount}'


class Game(models.Model):
    date = models.DateField()
    time = models.TimeField()
    home_team = models.CharField(max_length=70)
    away_team = models.CharField(max_length=70)
    score = models.CharField(max_length=7, default='-')
    home_odd = models.FloatField()
    draw_odd = models.FloatField()
    away_odd = models.FloatField()
    status = models.CharField(max_length=30, default='not played')
    winner = models.CharField(max_length=3, default='-')

    def __str__(self):
        return f'{self.date} {self.time} | {self.home_team} {self.away_team}' \
               f'( {self.score} ) | {self.home_odd} {self.draw_odd} {self.away_odd} |' \
               f' {self.status} {self.winner}'


class AppUser(models.Model):
    cash = models.DecimalField(validators=[MinValueValidator(0.00)],
                               max_digits=6, decimal_places=2)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    percent_profit = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user} - {self.cash} - {self.percent_profit}'


class UserPrediction(models.Model):
    game = models.ForeignKey(Game, related_name='game_predicted', on_delete=models.CASCADE)
    creator = models.ForeignKey(AppUser, related_name='creator', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='pending')
    home_team = models.CharField(max_length=70)
    away_team = models.CharField(max_length=70)
    sign = models.CharField(max_length=10)
    odd = models.FloatField()
    thoughts = models.TextField()
    score = models.CharField(max_length=7, default='-')


BET_CHOICES = ((1, 1),
               (2, 2),
               (0, 0)
               )


class Bet(models.Model):
    BET_RESULTS = ((0, "LOST"),
                   (1, "WON"),
                   (2, "PENDING"))
    bet_user = models.ForeignKey(AppUser, related_name='bet_user', on_delete=models.CASCADE)
    bet_amount = models.DecimalField(validators=[MinValueValidator(1.00)],
                                     max_digits=8, decimal_places=2)
    game = models.ForeignKey(Game, related_name='bet_game', on_delete=models.CASCADE)
    bet_sign = models.CharField(max_length=10)
    bet_odd = models.FloatField()
    score = models.CharField(max_length=7, default='-')
    status = models.IntegerField(default=2, blank=True, choices=BET_RESULTS)