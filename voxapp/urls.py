from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from .views import CustomPasswordResetConfirmView, logout_view


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('terms/', views.terms_view, name='terms'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('contact', views.contact, name='contact'),
    path('artist-home', views.artist_home, name='artist_home'),
    path('client-home', views.client_home, name='client_home'),
    path('sign-up/', views.signup, name='signup'),
    path('log-in/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings-view/', views.settings_view, name='settings_view'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-account/', views.update_account, name='update_account'),
    path('update-security/', views.update_security, name='update_security'),
    path('profile-view/', views.profile_view, name='profile_view'),
    path('bookings-view/', views.bookings_view, name='bookings_view'),
    path('book-artist/', views.book_artist_view, name='book_artist'),
    path('payments-view/', views.payments_view, name='payments_view'),
    path('reviews-view/', views.reviews_view, name='reviews_view'),
    path('setting-clientsview/', views.setting_clientsview, name='setting_clientsview'),
    # gig system
    path('gig-view/', views.gig_view, name='gig_view'),
    path('accept_gig_request/<int:request_id>/', views.accept_gig_request, name='accept_gig_request'),
    path('reject_gig_request/<int:request_id>/', views.reject_gig_request, name='reject_gig_request'),

    path('artist-profiles/', views.artist_profiles, name='artist_profiles'),
    path('artist_profiles/<str:username>/', views.full_artist_profile, name='full_artist_profile'),
    path('book_artist/<str:username>/', views.book_artist_view, name='book_artist_view'),

    path('artist-profile/', views.artist_profile, name='artist_profile'),
    path('update-pricing/<str:username>/', views.update_pricing_view, name='update_pricing'),
    path('add_portfolio_picture/<str:username>/', views.add_portfolio_picture, name='add_portfolio_picture'),
    
    
    path('logout/', logout_view, name='logout'),
    
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             form_class=CustomPasswordResetForm,
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt'
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             form_class=CustomSetPasswordForm
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
