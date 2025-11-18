from django.urls import path, include
from rest_framework_nested import routers
from users.views import UserViewSet
from soldiers.views import SoldierViewSet
from fitness.views import FitnessRecordViewSet
from academics.views import AcademicRecordViewSet
from benchmarks.views import BenchmarkViewSet

# Main router
router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('soldiers', SoldierViewSet, basename='soldiers')
router.register('fitness', FitnessRecordViewSet, basename='fitness')
router.register('academics', AcademicRecordViewSet, basename='academics')
router.register('benchmarks', BenchmarkViewSet, basename='benchmarks')

# Nested routers for soldiers
soldier_router = routers.NestedDefaultRouter(router, 'soldiers', lookup='soldier')
soldier_router.register('fitness-records', FitnessRecordViewSet, basename='soldier-fitness')
soldier_router.register('academic-records', AcademicRecordViewSet, basename='soldier-academics')

# Nested router for fitness records (if needed for additional endpoints)
fitness_router = routers.NestedDefaultRouter(router, 'fitness', lookup='fitness')
# Add nested fitness endpoints here if needed

urlpatterns = [
    path('', include(router.urls)),
    path('', include(soldier_router.urls)),
    path('auth/', include('users.urls')),
]