from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin
from django.contrib import messages
from .models import Event , BookEvent,Profile
from .forms import EventForm , BookEventForm,ProfileForm
from datetime import datetime
from django.db.models import Q



# ..................................list...............
def event_list(request):
    events=Event.objects.all()
    date_check=Event.objects.filter(date__gte=datetime.today())
    booked=BookEvent.objects.filter(booker=request.user)
    passed=[]
    future=[]
    for book in booked :
        if book.event.date>datetime.today().date():
            future.append(book)
        if book.event.date<=datetime.today().date():
            passed.append(book)

    events=Event.objects.filter(date__gte=datetime.today())
    query = request.GET.get("q")
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
            ).distinct()
    context={
    "events":events,
    "passed":passed,
    "future":future


    }
    return render(request,"list.html",context)


# .....................................detail..............
def event_detail(request,event_id):
    event_obj = Event.objects.get(id=event_id)
    tickets = BookEvent.objects.filter(event= event_obj)
    numtic = 0
    for tic in tickets:
        numtic += tic.number_of_tickets
    if event_obj.event_type ==  "Comedy" :
        pic = "{% static 'img/wp-Comedy.jpg'%}"
    elif event_obj.event_type ==  "Educational" :
        pic = "{% static 'img/wp-Educational.jpg'%}"
    elif event_obj.event_type ==  "Musical" :
        pic = "{% static 'img/wp-Musical.jpg'%}"
    else:
        pic ="{% static 'img/wp-all.jpg'%}"

    context={
    "event":event_obj,
    "tickets":tickets,
    "total":numtic,
    "pic":pic
    }
    return render(request,"detail.html",context)


#Create
def event_create(request):
    form = EventForm()
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event-list')
    context = {
        "form":form,
    }
    return render(request, 'create.html', context)


# Unpdate
def event_update(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    if not request.user.is_staff and request.user != event_obj.organizer:
        return redirect("signup")

    form = EventForm(instance=event_obj)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event_obj)
        if form.is_valid():
            form.save()
            return redirect('event-detail',event_id)
    context = {
        "event_obj": event_obj,
        "form":form,
    }
    return render(request, 'update.html', context)


#book (buying tickets)
def book_event (request,event_id,tickets_total):
    form = BookEventForm()
    event_obj = Event.objects.get(id=event_id)
    bookers = BookEvent.objects.filter(event=event_obj)
    if tickets_total == event_obj.tickets:
        return redirect('event-detail',event_id)
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == "POST":
        form = BookEventForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            if ticket.number_of_tickets+tickets_total > event_obj.tickets:
                messages.warning(request, "not enough tickets sry :( ")
                return redirect('event-detail',event_id)
            for booker in bookers:
                if booker.booker == request.user:
                    booker.number_of_tickets+=ticket.number_of_tickets
                    booker.save()
                    messages.success(request, "Booked Successfully yaay!")
                    return redirect('event-detail',event_id)

            ticket.booker = request.user
            ticket.event = event_obj
            ticket.save()

            messages.success(request, "Booked Successfully yaay!")
            return redirect('event-detail',event_id)
    context = {
        "form":form,
        "event_obj":event_obj,
        "total":tickets_total
            }
    return render(request, 'book.html', context)




def create_profile(request):
    form = ProfileForm()
    temp = Profile.objects.filter(username=request.user)
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            if temp != [] :
                messages.warning(request, "you already have a profile !")
                return redirect('my-profile')
            profile.username = request.user
            profile.save()
            messages.success(request, "Created profile Successfully ! Welcome to our family")
            return redirect('my-profile')
    context = {
        "form":form,
    }
    return render(request, 'create_profile.html', context)

def myprofile (request):
    profile= Profile.objects.filter(username=request.user)
    context = {
            "profiles":profile,
    }
    return render(request, 'my_profile.html', context)


def event_list_wm(request):
    events=Event.objects.all()
    date_check=Event.objects.filter(date__gte=datetime.today())
    booked=BookEvent.objects.filter(booker=request.user)
    passed=[]
    future=[]
    for book in booked :
        if book.event.date>datetime.today().date():
            future.append(book)
        if book.event.date<=datetime.today().date():
            passed.append(book)

    events=Event.objects.filter(date__gte=datetime.today())
    query = request.GET.get("q")
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
            ).distinct()
    context={
    "events":events,
    "passed":passed,
    "future":future


    }
    return render(request,"wmlist.html",context)
#..................................................................
#..................................................................
#..................................................................

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('event-list')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Bye :'(")
        return redirect("login")



def home(request):
    return render(request, 'home.html')
