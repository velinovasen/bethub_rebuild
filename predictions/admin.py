from django.contrib import admin
import predictions.models as m
# Register your models here.

admin.site.register(m.Game)
admin.site.register(m.BetsVolume)
admin.site.register(m.Prediction)