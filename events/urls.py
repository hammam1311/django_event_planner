from django.urls import path
# from .views import Login, Logout, Signup, home,event_list,event_detail
from events.views import *

urlpatterns = [
	path('',home, name='home'),

	#..............................................
	path('dashboard/', event_list, name='event-list'),
	path('events/<int:event_id>/', event_detail, name='event-detail'),
	path('events/<int:event_id>/update', event_update, name='event-update'),
	path('events/create', event_create, name='events-create'),
	path('events/<int:event_id>/<int:tickets_total>/book', book_event, name='event-book'),

	#...............................................
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
