"""event_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api import views

urlpatterns = [
# ............................api .....................
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.Register.as_view(), name="register"),
    path('upcoming_list/', views.EventsList.as_view(), name="upcoming-list"),
    path('organizer_list/', views.EventOrganizersList.as_view(), name="organizer-list"),
    path('api/event/<int:event_id>/update', views.UpdateEvent.as_view(), name="update-event-api"),
    path('api/event/create', views.CreateEvent.as_view(), name="create-event-api"),
    path('api/event/book', views.BookEventView.as_view(), name="book-event-api"),
    path('api/event/<int:event_id>/booked', views.BookedList.as_view(), name="booked-event-api"),
    path('api/event/<int:event_id>/mybookers', views.MyBookers.as_view(), name="mybookers-event-api"),










# .....................................................
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
]


if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
