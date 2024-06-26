from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
import logging
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import SignUpForm, CustomSetPasswordForm
from django.template.loader import render_to_string
from .artist_profileForm import (
    ArtistProfileForm, SongForm, PricingForm, PortfolioPictureForm, PortfolioVideoForm
)
from .artist_bookingForm import BookingRequest, BookingRequestForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Review, Song, Price, PortfolioPicture, PortfolioVideo, Booking, Payment, ClientReview, AcceptedGig, CanceledGig, Notification
from django.http import JsonResponse
from django.contrib import messages
from .models import Message
from .message_form import MessageForm


logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def portfolio(request):
    profile_info = request.user.profile

    # Retrieve notifications for the current user (artist) and order by created_at (latest first)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'profile_info': profile_info,
        'notifications': notifications,
    }
    return render(request, 'artist/artist-profile.html', context=context)
    

def contact(request):
    return render(request, 'contact.html')

def pricing(request):
    return render(request, 'pricing.html')

def terms_view(request):
    return render(request, 'terms.html')

def privacy_view(request):
    return render(request, 'privacy.html')

@require_POST
def subscribe_view(request):
    email = request.POST.get('email')
    print(f"New subscription: {email}")
    return HttpResponse('Thank you for subscribing!')


### Authentication and User Management

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.user_type = form.cleaned_data.get('user_type')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/sign-up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/log-in.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user

    if user.is_staff or user.is_superuser:
        return redirect('/admin/')  # Redirect admin users to the admin panel

    try:
        if user.profile.user_type == 'artist':
            profile = request.user.profile

            # Retrieve notifications for the current user (artist) and order by created_at (latest first)
            notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

            context = {
                'profile_info': profile,
                'notifications': notifications,
            }
            return render(request, 'artist/artist-dashboard.html', context=context)
        
        elif user.profile.user_type == 'client':
            # Retrieve notifications for the current user (client) and order by created_at (latest first)
            notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

            context = {
                'notifications': notifications,
            }
            return render(request, 'client/client-dashboard.html', context=context)
        
        else:
            return render(request, 'admin-dashboard.html')
    
    except Profile.DoesNotExist:
        return redirect('create_profile')  # Redirect to a profile creation view or some other fallback

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm


### Artist Views

def artist_home(request):
    return render(request, 'artist/artist-home.html')

@login_required
def settings_view(request):
    profile = request.user.profile

    # Retrieve notifications for the current user (artist) and order by created_at (latest first)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'profile_info': profile,
        'notifications': notifications,
    }

    return render(request, 'artist/settings.html', context)

@login_required
def edit_artist_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    price = get_object_or_404(Price, artist=profile.pricing_info)  # Access pricing_info related_name

    if request.method == 'POST':
        profile_form = ArtistProfileForm(request.POST, request.FILES, instance=profile)
        pricing_form = PricingForm(request.POST, instance=pricing)

        if profile_form.is_valid():
            profile_form.save()

        if pricing_form.is_valid():
            pricing_form.save()

        return redirect('edit_artist_profile')

    else:
        profile_form = ArtistProfileForm(instance=profile)
        pricing_form = PricingForm(instance=pricing)

    context = {
        'profile_form': profile_form,
        'pricing_form': pricing_form,
    }

    return render(request, 'artist/edit_profile.html', context)

@login_required
def artist_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    if request.method == 'POST':
        profile_form = ArtistProfileForm(request.POST, request.FILES, instance=profile)
        pricing_form = PricingForm(request.POST, instance=profile.pricing)

        if profile_form.is_valid():
            profile_form.save()

        if pricing_form.is_valid():
            pricing_form.save()

        return redirect('artist_profile', username=username)
    else:
        profile_form = ArtistProfileForm(instance=profile)
        pricing_form = PricingForm(instance=profile.pricing)

    reviews = Review.objects.filter(artist=profile)
    playlist = Song.objects.filter(artist=profile)
    portfolio_pictures = PortfolioPicture.objects.filter(artist=profile)
    portfolio_videos = PortfolioVideo.objects.filter(artist=profile)

    context = {
        'profile_info': profile,
        'reviews': reviews,
        'playlist': playlist,
        'portfolio_pictures': portfolio_pictures,
        'portfolio_videos': portfolio_videos,
        'profile_form': profile_form,
        'pricing_form': pricing_form,
        'picture_form': PortfolioPictureForm(),
        'video_form': PortfolioVideoForm(),
        'song_form': SongForm(),
    }

    return render(request, 'artist/artist_profile.html', context)


def full_artist_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    reviews = Review.objects.filter(artist=profile)
    playlist = Song.objects.filter(artist=profile)
    portfolio_pictures = PortfolioPicture.objects.filter(artist=profile)
    portfolio_videos = PortfolioVideo.objects.filter(artist=profile)
    
    context = {
        'profile_info': profile,
        'reviews': reviews,
        'playlist': playlist,
        'portfolio_pictures': portfolio_pictures,
        'portfolio_videos': portfolio_videos,
    }
    return render(request, 'client/full_artistProfile.html', context)

@login_required
def gig_view(request):
    profile = request.user.profile
    gig_requests = BookingRequest.objects.filter(artist=profile)
    accepted_gigs = AcceptedGig.objects.filter(artist=profile)
    canceled_gigs = CanceledGig.objects.filter(artist=profile)

    # Create notifications for new gig requests if they don't already exist
    for request_obj in gig_requests:
        Notification.objects.get_or_create(
            user=request_obj.artist.user,
            title="New Gig Request",
            content=f"You have received a new gig request for '{request_obj.event_name}' from {request_obj.user.username}.",
            defaults={'is_read': False}
        )

    # Retrieve notifications for the current user (artist) and order by created_at (latest first)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'gig_requests': gig_requests,
        'accepted_gigs': accepted_gigs,
        'canceled_gigs': canceled_gigs,
        'notifications': notifications,
    }

    return render(request, 'artist/gig-view.html', context)

@login_required
def accept_gig_request(request, request_id):
    booking_request = get_object_or_404(BookingRequest, id=request_id)
    
    # Create an AcceptedGig from the BookingRequest data
    accepted_gig = AcceptedGig.objects.create(
        artist=booking_request.artist,
        event_name=booking_request.event_name,
        event_date=booking_request.event_date,
        event_time=booking_request.event_time,
        event_location=booking_request.event_location,
        event_description=booking_request.event_description,
        client_username=booking_request.user.username,
        client_email=booking_request.user.email
    )
    
    # Notify the client about the accepted gig request
    Notification.objects.create(
        user=booking_request.user,  # Client who made the booking request
        title="Gig Request Accepted",
        content=f"Your gig request for '{booking_request.event_name}' has been accepted by {booking_request.artist.user.username}."
    )
    
    # Optionally delete the BookingRequest
    booking_request.delete()
    
    # Render HTML for the accepted gig
    accepted_gig_html = render_to_string('accepted_gig_template.html', {'gig': accepted_gig})
    
    # Return JSON response with accepted gig HTML
    return JsonResponse({'accepted_gig_html': accepted_gig_html})


@login_required
def reject_gig_request(request, request_id):
    booking_request = get_object_or_404(BookingRequest, id=request_id)
    
    # Create a CanceledGig from the BookingRequest data
    canceled_gig = CanceledGig.objects.create(
        artist=booking_request.artist,
        event_name=booking_request.event_name,
        event_date=booking_request.event_date,
        event_time=booking_request.event_time,
        event_location=booking_request.event_location,
        event_description=booking_request.event_description,
        client_username=booking_request.user.username,
        client_email=booking_request.user.email
    )
    
    # Notify the client about the rejected gig request
    Notification.objects.create(
        user=booking_request.user,  # Client who made the booking request
        title="Gig Request Rejected",
        content=f"Your gig request for '{booking_request.event_name}' has been rejected by {booking_request.artist.user.username}."
    )
    
    # Optionally delete the BookingRequest
    booking_request.delete()
    
    # Render HTML for the canceled gig
    canceled_gig_html = render_to_string('canceled_gig_template.html', {'gig': canceled_gig})
    
    # Return JSON response with canceled gig HTML
    return JsonResponse({'canceled_gig_html': canceled_gig_html})


### Client Views

@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'client/client-profile.html', context)

@login_required
def bookings_view(request):
    user = request.user

    # Fetch notifications for the current user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')

    # Fetch booking requests, accepted gigs, and canceled gigs for the current user
    booking_requests = BookingRequest.objects.filter(user=user)
    accepted_gigs = AcceptedGig.objects.filter(client_username=user.username)
    canceled_gigs = CanceledGig.objects.filter(client_username=user.username)

    # Prepare context to pass to the template
    context = {
        'notifications': notifications,
        'booking_requests': booking_requests,
        'accepted_gigs': accepted_gigs,
        'canceled_gigs': canceled_gigs,
        'user': user,
    }

    # Render the client bookings template with the context data
    return render(request, 'client/client-bookings.html', context)

@login_required
def payments_view(request):
    user = request.user
    payments = Payment.objects.filter(user=user)
    
    # Fetch notifications for the current user (client)
    notifications = Notification.objects.filter(user=user).order_by('-created_at')

    context = {
        'user': user,
        'payments': payments,
        'notifications': notifications,
    }
    return render(request, 'client/client-payments.html', context)

@login_required
def reviews_view(request):
    user = request.user
    reviews = ClientReview.objects.filter(user=user)
    
    # Fetch notifications for the current user (client)
    notifications = Notification.objects.filter(user=user).order_by('-created_at')

    context = {
        'user': user,
        'reviews': reviews,
        'notifications': notifications,
    }
    return render(request, 'client/client-reviews.html', context)

@login_required
def setting_clientsview(request):
    user = request.user
    
    # Fetch notifications for the current user (client)
    notifications = Notification.objects.filter(user=user).order_by('-created_at')

    context = {
        'user': user,
        'notifications': notifications,
    }
    return render(request, 'client/client-settings.html', context)

@login_required
def book_artist_view(request, username):
    artist = get_object_or_404(Profile, user__username=username)

    # Fetch notifications for the current user (client)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking_request = form.save(commit=False)
            booking_request.user = request.user
            booking_request.artist = artist
            booking_request.save()

            # Notify the artist about the booking request
            Notification.objects.create(
                user=artist.user,  # Artist who receives the booking request
                title="New Booking Request",
                content=f"You have a new booking request from {request.user.username} for an event."
            )

            return JsonResponse({'success': 'Booking request saved successfully'})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = BookingRequestForm()

    context = {
        'notifications': notifications,
        'artist': artist,
        'form': form,
    }
    return render(request, 'client/book_artist.html', context)



@login_required
def artist_profiles(request):
    user = request.user
    
    # Fetch notifications for the current user (client)
    notifications = Notification.objects.filter(user=user).order_by('-created_at')

    # Fetch all artists' profiles
    artists = Profile.objects.filter(user_type='artist')

    context = {
        'artists': artists,
        'notifications': notifications,
    }
    return render(request, 'client/artist_profiles.html', context)


@login_required
def update_pricing_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    price_instance, created = Price.objects.get_or_create(artist=profile.user)
    # Assuming Price model is linked to Profile via artist=profile.user

    if request.method == 'POST':
        pricing_form = PricingForm(request.POST, instance=price_instance)
        if pricing_form.is_valid():
            pricing_form.save()
            return redirect('artist_profile', username=username)
    else:
        pricing_form = PricingForm(instance=price_instance)

    context = {
        'pricing_form': pricing_form,
        'profile_info': profile,
    }

    return render(request, 'artist/artist-profile.html', context)

@login_required
def add_portfolio_picture(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    if request.method == 'POST':
        form = PortfolioPictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.artist = profile
            picture.save()
            return redirect('artist_profile', username=username)
    else:
        form = PortfolioPictureForm()

    context = {
        'form': form,
        'username': username,
    }
    return render(request, 'artist/add_portfolio_picture.html', context)


@login_required
def messages_view(request):
    user = request.user
    
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    received_messages = Message.objects.filter(recipient=user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=user).order_by('-timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.save()

            # Create a notification for the recipient
            Notification.objects.create(
                user=message.recipient,
                title=f'New Message from {user.username}',
                content=f'You have received a new message from {user.username}.'
            )
            
            return redirect('messages')  # Redirect back to the messages view after saving
    else:
        form = MessageForm()

    context = {
        'notifications': notifications,
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'form': form,
    }

    return render(request, 'messages.html', context)








#Others I might use--------------------------------------------------------------------------------------------------------------------------------------------- 

def contact(request):
        return render(request, 'contact.html')

def client_home(request):
    return render(request, 'client/client-home.html')

#Settings -artist
@login_required
def edit_profile(request):
    try:
        artist_profile = request.user.profile
    except Profile.DoesNotExist:
        # If the user doesn't have an associated Profile, create one
        artist_profile = Profile(user=request.user)
        artist_profile.save()

    if request.method == 'POST':
        form = ArtistProfileForm(request.POST, request.FILES, instance=artist_profile)
        if form.is_valid():
            form.save()
            return redirect('artist/artist_profile')
    else:
        form = ArtistProfileForm(instance=artist_profile)
    
    return render(request, 'artist/edit_profile.html', {'form': form})
#end of artist profile edit 

@login_required
def update_profile(request):
    print(request.user)  # Check which user is accessing the view
    print(request.user.is_authenticated)  # Check if the user is authenticated

    # Your view logic here
    return render(request, 'artist/update_profile.html')

@login_required
def update_account(request):
    print(request.user)  # Check which user is accessing the view
    print(request.user.is_authenticated)  # Check if the user is authenticated

    # Your view logic here
    return render(request, 'artist/update_account.html')

@login_required
def update_security(request):
    print(request.user)  # Check which user is accessing the view
    print(request.user.is_authenticated)  # Check if the user is authenticated

    # Your view logic here
    return render(request, 'artist/update_security.html')


#End of others




