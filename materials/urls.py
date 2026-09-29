from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'materials', CourseViewSet, basename='materials')

urlpatterns = [

] + router.urls