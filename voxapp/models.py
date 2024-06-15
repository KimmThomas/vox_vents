from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('artist', 'Artist'),
        ('client', 'Client'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    class_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    pricing = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Default Pricing')

    def __str__(self):
        return self.user.username


class GigRequest(models.Model):
    artist = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    event_name = models.CharField(max_length=100, blank=True, null=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255, blank=True, null=True)
    event_description = models.TextField()
    

    def __str__(self):
        return f"{self.event_name} on {self.event_date} by {self.user.username}"

    class Meta:
        verbose_name = "Gig Request"
        verbose_name_plural = "Gig Requests"


class AcceptedGig(models.Model):
    artist = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255, blank=True, null=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255, blank=True, null=True)
    event_description = models.TextField()
    client_username = models.CharField(max_length=150, blank=True, null=True)
    client_email = models.EmailField()

    def __str__(self):
        return f"{self.event_name} - Accepted"

   

class CanceledGig(models.Model):
    artist = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255, blank=True, null=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255, blank=True, null=True)
    event_description = models.TextField()
    client_username = models.CharField(max_length=150, blank=True, null=True)
    client_email = models.EmailField()

    def __str__(self):
        return f"{self.event_name} - Canceled"

    

class Review(models.Model):
    artist = models.ForeignKey(Profile, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    stars = models.IntegerField()

    def __str__(self):
        return f"Review for {self.artist.user.username} by {self.rating} stars"

class Song(models.Model):
    artist = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='songs/', blank=True, null=True)

    def __str__(self):
        return self.title

class Price(models.Model):
    artist = models.OneToOneField(Profile, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.artist.user.username} - {self.price}"
class PortfolioPicture(models.Model):
    artist = models.ForeignKey(Profile, related_name='portfolio_pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio_pics/')

    def __str__(self):
        return f"Picture for {self.artist.user.username}"

class PortfolioVideo(models.Model):
    artist = models.ForeignKey(Profile, related_name='portfolio_videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='portfolio_videos/')
    poster = models.ImageField(upload_to='video_posters/', blank=True, null=True)

    def __str__(self):
        return f"Video for {self.artist.user.username}"

class BookingRequest(models.Model):
    artist = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255)
    event_description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')

    def __str__(self):
        return f"{self.event_name} on {self.event_date} by {self.user.username}"
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_description = models.TextField()

    def __str__(self):
        return self.event_name

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.booking.event_name}"

class ClientReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.booking.event_name} by {self.user.username}"

    class Meta:
        unique_together = ['user', 'booking']
