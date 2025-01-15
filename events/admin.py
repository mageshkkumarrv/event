from django.contrib import admin
from .models import Event, Booking

# Inline display of bookings in the Event admin page
class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0  # No extra blank rows
    fields = ('user_name', 'user_email', 'booking_date')
    readonly_fields = ('user_name', 'user_email', 'booking_date')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date', 'location', 'price', 'available_tickets')
    list_filter = ('category', 'date', 'location')
    search_fields = ('name', 'location', 'description')
    inlines = [BookingInline]  # Include bookings as inline inside event details

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_phone', 'event', 'booking_date')  
    list_filter = ('event', 'user', 'booking_date')  
    search_fields = ('user_name', 'user_email', 'user_phone', 'event__name')  
    readonly_fields = ('user_name', 'user_email', 'user_phone', 'event', 'booking_date')  

