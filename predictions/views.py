from django.shortcuts import render

# Create your views here.
from predictions.models import Prediction, BetsVolume


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


