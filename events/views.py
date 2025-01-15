from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Event, Booking
from .forms import RegisterForm, BookingForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.utils.timezone import now, make_aware



def home(request):
    events = Event.objects.all()
    return render(request, "events/home.html", {"events": events})


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event_details.html", {"event": event})


# @login_required
# def book_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     if event.available_tickets <= 0:
#         messages.error(request, "No tickets available for this event.")
#         return redirect("home")

#     if request.method == "POST":
#         Booking.objects.create(user=request.user, event=event)
#         event.available_tickets -= 1
#         event.save()
#         messages.success(request, f"Successfully booked a ticket for {event.name}.")
#         return redirect("booking_history")

#     return render(request, "events/book_event.html", {"event": event})

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if tickets are available
    if event.available_tickets <= 0:
        messages.error(request, "No tickets available for this event.")
        return redirect("home")
    
    # Handle booking session timeout
    booking_start_time = request.session.get("booking_start_time")
    if booking_start_time:
        # Convert the naive datetime from session to an aware datetime
        booking_start_time = make_aware(datetime.strptime(booking_start_time, "%Y-%m-%d %H:%M:%S"))

        if now() > booking_start_time + timedelta(minutes=5):
            # Clear session and redirect to home if booking expired
            del request.session["booking_start_time"]
            messages.error(request, "Booking time expired. Please try again.")
            return redirect("home")

    # Handle booking form submission
    if request.method == "POST":
        user_phone = request.POST.get("user_phone", "")
        Booking.objects.create(
            user=request.user,  # Link the booking to the logged-in user
            event=event,  # Associate the booking with the event
            user_name=request.user.get_full_name() if request.user.get_full_name() else request.user.username,
            user_email=request.user.email,  # Save the user's email
            user_phone=user_phone,
        )
        
        # Decrease the available tickets for the event
        event.available_tickets -= 1
        event.save()

        # Clear booking session after successful booking
        if "booking_start_time" in request.session:
            del request.session["booking_start_time"]
        
        # Send booking confirmation email
        subject = f"Booking Confirmation for {event.name}"
        message = (
            f"Hello {request.user.username},\n\n"
            f"Thank you for booking a ticket for {event.name}.\n\n"
            f"Event Details:\n"
            f"Name: {event.name}\n"
            f"Date: {event.date}\n"
            f"Time: {event.time}\n"
            f"Location: {event.location}\n"
            f"Price: ₹{event.price}\n\n"
            f"Enjoy the event!\n\n"
            f"Regards,\nTicket Booking Team"
        )
        recipient = request.user.email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

        # Display success message
        messages.success(request, f"Successfully booked a ticket for {event.name}.")
        
        # Redirect to booking history page
        return redirect("booking_history")
    
        # Save booking start time in session
    if "booking_start_time" not in request.session:
        request.session["booking_start_time"] = now().strftime("%Y-%m-%d %H:%M:%S")

    return render(request, "events/book_event.html", {"event": event})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "events/booking_history.html", {"bookings": bookings})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "events/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "events/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")

def user_booking_history(request):
    # Fetch bookings for the current user
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user_booking_history.html', {'bookings': bookings})
