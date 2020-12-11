from django.contrib import admin
import predictions.models as m


# Register your models here.

class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'time', 'home_team', 'away_team', 'score', 'home_odd', 'draw_odd', 'away_odd',
                    'status', 'winner']


class BetsVolumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'day', 'time', 'home_team', 'away_team', 'final_bet', 'odds', 'amount']


class PredictionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'time', 'home_team', 'away_team', 'home_prob', 'draw_prob',
                    'away_prob', 'bet_sign', 'score_predict', 'avg_goals', 'odds_for_prediction',
                    'home_odd', 'draw_odd', 'away_odd', 'temp']


class AppUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'cash', 'percent_profit']


admin.site.register(m.Game, GameAdmin)
admin.site.register(m.BetsVolume, BetsVolumeAdmin)
admin.site.register(m.Prediction, PredictionsAdmin)
admin.site.register(m.AppUser, AppUserAdmin)