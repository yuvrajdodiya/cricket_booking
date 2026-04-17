from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Post, TicketType
from .forms import PostForm, TicketTypeForm
from booking.models import Booking

@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            return render(request,"adminpenal/login.html",{
                "error" : "Invalid username os password"
            })
        
    return render(request,'adminpenal/login.html')

def admin_logout(request):
    logout(request)
    return redirect("admin_login")

def admin_deshbord(request):
    context = {
        "total_users": User.objects.count(),
        "total_grounds": Post.objects.count(),
        "total_ticket_types": TicketType.objects.filter(is_active=True).count(),
        "total_bookings": Booking.objects.count(),
        "grounds": Post.objects.all(),
    }
    return render(request, "adminpenal/dashboard.html", context)
    

def ground(request):
    edit_post = None
    edit_ticket = None
    edit_id = request.GET.get("edit")
    edit_ticket_id = request.GET.get("edit_ticket")
    if edit_id:
        edit_post = get_object_or_404(Post, pk=edit_id)
    if edit_ticket_id:
        edit_ticket = get_object_or_404(TicketType, pk=edit_ticket_id)

    if request.method == "POST":
        form_type = request.POST.get("form_type", "post")
        if form_type == "ticket":
            ticket_id = request.POST.get("ticket_id")
            instance = get_object_or_404(TicketType, pk=ticket_id) if ticket_id else None
            ticket_form = TicketTypeForm(request.POST, instance=instance)
            if ticket_form.is_valid():
                ticket_form.save()
                return redirect('grounds')
            form = PostForm(instance=edit_post)
        else:
            post_id = request.POST.get("post_id")
            instance = get_object_or_404(Post, pk=post_id) if post_id else None
            form = PostForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                post = form.save(commit=False)
                if not post.author_id:
                    post.author = request.user if request.user.is_authenticated else None
                post.save()
                return redirect('grounds')
            ticket_form = TicketTypeForm(instance=edit_ticket)
    else:
        form = PostForm(instance=edit_post)
        ticket_form = TicketTypeForm(instance=edit_ticket)

    posts = Post.objects.all()
    ticket_types = TicketType.objects.all()
    return render(request, "adminpenal/ground.html", {
        "form": form,
        "ticket_form": ticket_form,
        "posts": posts,
        "ticket_types": ticket_types,
        "edit_post": edit_post,
        "edit_ticket": edit_ticket,
    })


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        post.delete()
    return redirect("grounds")


def delete_ticket_type(request, ticket_id):
    ticket_type = get_object_or_404(TicketType, pk=ticket_id)
    if request.method == "POST":
        ticket_type.delete()
    return redirect("grounds")



def user_list(request):
    users = User.objects.all()
    return render(request, 'adminpenal/user.html', {'users': users})


def booking_list(request):
    bookings = Booking.objects.select_related('user', 'ground', 'ticket_type').all()
    return render(request, 'adminpenal/booking.html', {
        'bookings': bookings,
    })
