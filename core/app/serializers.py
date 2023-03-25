from .models import Activity, Gym, Profile, Workout
from rest_framework import serializers,status
# from rest_framework.views import APIView
# from rest_framework.viewsets import ModelViewSet

class GymSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['id','name']

class GymSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['name','description','address','phone']

class ActivityForWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['name']

class ProfileForWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name','last_name']

class WorkoutSerializerRead(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'time', 'gym', 'activity', 'profile']

    gym = GymSerializerGET()
    activity = ActivityForWorkoutSerializer()
    profile = ProfileForWorkoutSerializer(many=True)

class WorkoutSerializerWrite(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id','time','gym','activity','profile']
    
    gym = serializers.PrimaryKeyRelatedField(queryset=Gym.objects.all())
    activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=True)
