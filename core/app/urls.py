from django.urls import path,include
from . import views
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

router = SimpleRouter()
router.register('workouts', views.WorkoutViewSet, basename='workout')
router.register('gyms', views.GymViewSet, basename='gym')
workouts_router = routers.NestedSimpleRouter(router, 'gyms', lookup='gym')
workouts_router.register('workouts', views.WorkoutViewSet, basename='gym-workouts')


# urlpatterns = [a
#     path('gyms/<int:id>',views.gym_detail),
#     path('gyms/',views.gym_list),
#     path('', include(router.urls))
# ]

urlpatterns = router.urls + workouts_router.urls