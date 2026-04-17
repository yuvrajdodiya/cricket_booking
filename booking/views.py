from urllib.parse import urlencode

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from adminpenal.models import Post, TicketType
from .models import Booking

def entry_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('user_login')

@login_required(login_url='user_login')
def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})

@login_required(login_url='user_login')
def cart(request):
        posts = Post.objects.all()
        ticket_types = TicketType.objects.filter(is_active=True)
        return render(request, 'cart.html', {
            "posts": posts,
            "ticket_types": ticket_types,
        })

@login_required(login_url='user_login')
def checkout(request):
     if request.method == 'POST':
         ground = get_object_or_404(Post, pk=request.POST.get('ground'))
         ticket_type = get_object_or_404(TicketType, pk=request.POST.get('ticket_type_id'), is_active=True)

         quantity = int(request.POST.get('quantity', 1))
         quantity = max(1, min(quantity, 10))
         price = ticket_type.price
         total = price * quantity

         booking = Booking.objects.create(
             user=request.user,
             ground=ground,
             ticket_type=ticket_type,
             first_name=request.POST.get('first_name', '').strip(),
             last_name=request.POST.get('last_name', '').strip(),
             email=request.POST.get('email', '').strip() or request.user.email,
             quantity=quantity,
             price_per_ticket=price,
             total_price=total,
         )

         params = urlencode({
             'success': 1,
             'ground': ground.id,
             'ground_name': ground.title,
             'ticket_type_id': ticket_type.id,
             'ticket_type': ticket_type.name,
             'quantity': quantity,
             'price': price,
             'total': total,
             'booking_id': booking.id,
         })
         return redirect(f"{reverse('checkout')}?{params}")

     ground_id = request.GET.get('ground', '')
     ground_name = request.GET.get('ground_name', 'Not selected')
     ticket_type_id = request.GET.get('ticket_type_id', '')
     ticket_type = request.GET.get('ticket_type', 'Not selected')
     quantity = request.GET.get('quantity', '0')
     price = request.GET.get('price', '0')
     total = request.GET.get('total', '0')

     context = {
         'selected_ground_id': ground_id,
         'selected_ground_name': ground_name,
         'selected_ticket_type_id': ticket_type_id,
         'selected_ticket_type': ticket_type,
         'selected_quantity': quantity,
         'selected_price': price,
         'selected_total': total,
         'first_name': request.user.first_name,
         'last_name': request.user.last_name,
         'email': request.user.email,
         'booking_success': request.GET.get('success') == '1',
         'booking_id': request.GET.get('booking_id', ''),
     }
     return render(request, 'checkout.html', context)
