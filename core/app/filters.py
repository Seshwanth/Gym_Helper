from django_filters.rest_framework import FilterSet
from .models import Workout

class WorkoutFilter(FilterSet):
    class Meta:
        model = Workout
        fields = {
            'activity__name':['exact'],
        }