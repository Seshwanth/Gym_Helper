from django.shortcuts import render
from .models import Gym, Workout
from .serializers import GymSerializerGET, GymSerializerPOST, WorkoutSerializerRead, WorkoutSerializerWrite
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import WorkoutFilter
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(['GET','DELETE'])
def gym_detail(request, id):
    gym = get_object_or_404(Gym, pk=id)
    if request.method == 'GET':
        serializer = GymSerializerGET(gym)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        gym.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def gym_list(request):
    if request.method == 'GET':
        gym = Gym.objects.all()
        serializer = GymSerializerGET(gym, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GymSerializerPOST(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

@api_view()
def workout_list(request):
    workout = Workout.objects.annotate(num_participants=Count('profile_id')).filter(num_participants__gt=0)

class default_pagination(PageNumberPagination):
    page_size=2

class WorkoutViewSet(ModelViewSet):

    # def get(self, request):
    #     queryset = Workout.objects.select_related().prefetch_related().all()
    #     serializer = WorkoutSerializerRead(queryset, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = WorkoutSerializerWrite(data=request.data)
    #     serializers.is_valid(raise_exception=True)
    #     serializer.save()
    #     return(serializer.data, status.HTTP_201_CREATED)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = WorkoutFilter
    search_fields = ['activity__description']
    ordering_fields = ['gym__name', 'activity__name']
    pagination_class = default_pagination

    def get_queryset(self):
        if self.request.path == '/app/workouts/':
            queryset = Workout.objects.select_related().prefetch_related().all()
        else:
            queryset = Workout.objects.select_related().prefetch_related().filter(gym_id=self.kwargs['gym_pk'])
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkoutSerializerRead
        return WorkoutSerializerWrite
    
    def destroy(self, request, pk):
        workout = get_object_or_404(Workout, pk=pk)
        if workout.profile.count() > 0:
            return Response({'error':'Cannot delete workouts with Users.'})
        else:
            workout.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class GymViewSet(ModelViewSet):

    queryset = Gym.objects.select_related().prefetch_related().all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GymSerializerGET
        return GymSerializerPOST