from django.urls import path
from . import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('verification/<int:id_ver>/<str:sec_email>/<str:recovery>', views.verification, name='verification'),
    path('registration_data/<int:id_ver>', views.registration_data, name='registration_data'),
    path('entrance', views.entrance, name='entrance'),
    path('recovery', views.recovery, name='recovery'),
    path('recovery_data/<int:id_ver>/<str:sec_email>', views.recovery_data, name='recovery_data'),
    path('page/<int:id_ver>', views.page, name='page'),
    path('error/<str:error_text>', views.error, name='error')
]