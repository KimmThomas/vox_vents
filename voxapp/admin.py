from django.contrib import admin
from .models import Profile, Review, Song, Price,PortfolioPicture, PortfolioVideo, BookingRequest, Booking, Payment, ClientReview, AcceptedGig, CanceledGig


admin.site.register(Profile)
admin.site.register(AcceptedGig)
admin.site.register(CanceledGig)
admin.site.register(Review)
admin.site.register(Song)
admin.site.register(Price)
admin.site.register(PortfolioPicture)
admin.site.register(PortfolioVideo)
admin.site.register(BookingRequest)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(ClientReview)
