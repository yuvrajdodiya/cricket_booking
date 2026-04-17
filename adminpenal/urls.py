from django.urls import path
from . import views
urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    path("dashboard/", views.admin_deshbord, name="admin_dashboard"),
    path("logout/", views.admin_logout, name="admin_logout"),


    path("grounds/", views.ground, name="grounds"),
    path("grounds/<int:post_id>/delete/", views.delete_post, name="delete_post"),
    path("tickets/<int:ticket_id>/delete/", views.delete_ticket_type, name="delete_ticket_type"),
    path("booking/", views.booking_list, name="booking_list"),
    path('users/', views.user_list, name='users'),

]
