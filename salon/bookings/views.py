from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Booking
from .forms import BookingForm
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def my_page(request):
    return render(request, 'bookings/my.html')

def base_page(request):
    return render(request, 'bookings/base.html')

def book_page(request):
    return render(request, 'bookings/book.html')

def list_masters(request):
    masters = User.objects.filter(groups__name='masters')
    return render(request, 'bookings/list_masters.html', {'masters': masters})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('my')

@login_required
def my_page(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user 
            booking.save()
            return redirect('my')
    else:
        form = BookingForm()

    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my.html', {'bookings': bookings, 'form': form})

@login_required
def my(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my.html', {'bookings': bookings})

@login_required
def book(request, master_id):
    from django.contrib.auth.models import User
    
    master = get_object_or_404(User, id=master_id)
    
    if request.method == 'POST':
        date_str = request.POST['date']
        time_str = request.POST['time']
        start_dt = timezone.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        start_dt = timezone.make_aware(start_dt)
        end_dt = start_dt + timedelta(hours=2)

        conflict = Booking.objects.filter(
            master=master,
            start_time__lt=end_dt,
            end_time__gt=start_dt,
        ).exists()

        if conflict:
            return render(request, 'bookings/book.html', {'error': 'Время занято', 'master': master})

        Booking.objects.create(
            user=request.user,
            master=master,
            start_time=start_dt,
            end_time=end_dt,
        )
        return redirect('my')
    
    return render(request, 'bookings/book.html', {'master': master})

@login_required
def cancel(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)
    booking.delete()
    return redirect('my')

# ТАБЛИЦА УМНОЖЕНИЯ
@csrf_exempt
def generate_mult_table(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        size = data.get('size', 10)
        
        # Генерация HTML таблицы умножения
        html = '<table border="1" cellpadding="5">'
        
        # Заголовки колонок
        html += '<tr><th></th>'
        for i in range(1, size + 1):
            html += f'<th>{i}</th>'
        html += '</tr>'
        
        # Строки таблицы
        for i in range(1, size + 1):
            html += f'<tr><th>{i}</th>'
            for j in range(1, size + 1):
                html += f'<td>{i * j}</td>'
            html += '</tr>'
        
        html += '</table>'
        
        return HttpResponse(html)
    else:
        return HttpResponse(status=405)
    
# в Django означает, что сервер получил запрос с методом, который не разрешён для данного ресурса