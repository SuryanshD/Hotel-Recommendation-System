from django.contrib import admin

from booking.models import Hotel, Room, Booking, Review, SearchHistory

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(SearchHistory)
 