from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
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
    selected_ground_id = request.GET.get('ground', '')
    selected_ground = None

    if selected_ground_id:
        selected_ground = Post.objects.filter(pk=selected_ground_id).first()

    return render(request, 'cart.html', {
        "posts": posts,
        "ticket_types": ticket_types,
        "selected_ground": selected_ground,
        "selected_ground_id": str(selected_ground.id) if selected_ground else '',
        "selected_ground_name": selected_ground.title if selected_ground else '',
    })

@login_required(login_url='user_login')
def checkout(request):
     if request.method == 'POST':
         ground_id = request.POST.get('ground')
         ticket_type_id = request.POST.get('ticket_type_id')

         if not ground_id or not ticket_type_id:
             return redirect('cart')

         ground = get_object_or_404(Post, pk=ground_id)
         ticket_type = get_object_or_404(TicketType, pk=ticket_type_id, is_active=True)

         try:
             quantity = int(request.POST.get('quantity', 1))
         except (TypeError, ValueError):
             quantity = 1
         quantity = max(1, min(quantity, 10))
         price = ticket_type.price
         total = price * quantity
         first_name = request.POST.get('first_name', '').strip()
         last_name = request.POST.get('last_name', '').strip()
         email = request.POST.get('email', '').strip() or request.user.email
         bill_note = request.POST.get('bill', '').strip()

         booking = Booking.objects.create(
             user=request.user,
             ground=ground,
             ticket_type=ticket_type,
             first_name=first_name,
             last_name=last_name,
             email=email,
             quantity=quantity,
             price_per_ticket=price,
             total_price=total,
         )

         full_name = f"{first_name} {last_name}".strip() or request.user.get_username()
         document = f"""
         <html>
         <head>
             <meta charset="utf-8">
             <title>Booking Details</title>
         </head>
         <body>
             <h1>Cricket Booking Details</h1>
             <p><strong>Booking ID:</strong> #{booking.id}</p>
             <p><strong>Name:</strong> {escape(full_name)}</p>
             <p><strong>Email:</strong> {escape(email)}</p>
             <p><strong>Ground:</strong> {escape(ground.title)}</p>
             <p><strong>Ticket Type:</strong> {escape(ticket_type.name)}</p>
             <p><strong>Tickets:</strong> {quantity}</p>
             <p><strong>Price Per Ticket:</strong> Rs. {price}</p>
             <p><strong>Total Bill:</strong> Rs. {total}</p>
             <p><strong>Total:</strong> Rs. {total}</p>
             <p><strong>Note:</strong> {escape(bill_note) if bill_note else 'No note'}</p>
         </body>
         </html>
         """
         response = HttpResponse(document, content_type='application/msword')
         response['Content-Disposition'] = f'attachment; filename="booking_{booking.id}_details.doc"'
         return response

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
