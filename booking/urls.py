from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    # Hotel search and listing
    path('', views.HotelSearchView.as_view(), name='search'),
    path('hotels/', views.HotelListView.as_view(), name='hotel_list'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel_detail'),
    path('recommended/', views.RecommendedHotelsView.as_view(), name='recommended_hotels'),
    
    # Booking
    path('book/<int:hotel_id>/<int:room_id>/', views.BookingCreateView.as_view(), name='booking_create'),
    path('booking/<int:booking_id>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/', views.BookingHistoryView.as_view(), name='booking_history'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    # Reviews
    path('review/<int:hotel_id>/', views.ReviewCreateView.as_view(), name='review_create'),
    
    # AJAX endpoints
    path('ajax/room-availability/', views.ajax_room_availability, name='ajax_room_availability'),
]
