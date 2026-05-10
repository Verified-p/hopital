from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Appointment
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from django.shortcuts import render, get_object_or_404
from .models import Doctor
from django.db.models import Q

from .models import Cart, CartItem, Medicine, ManualPayment
from django.http import JsonResponse
from .models import Payment
from .utils import initiate_stk_push
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from openai import OpenAI
import os
import json
import random

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import TestOrder


from .models import VaccinationAppointment


from django.contrib.auth.decorators import login_required


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout




from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required
from .models import PatientRecord
from .forms import PatientRecordForm

@login_required
def appointment(request):
    if request.method == 'POST':
        # Get data directly from POST request (matches your raw HTML names)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        doctor = request.POST.get('doctor')
        date = request.POST.get('date')
        message = request.POST.get('message', '')

        # Save to the database
        appointment = Appointment.objects.create(
            name=name,
            email=email,
            phone=phone,
            department=department,
            doctor=doctor,
            date=date,
            message=message
        )

        # Optional: send email confirmation
        try:
            send_mail(
                subject='Appointment Confirmation',
                message=f"Dear {name},\n\nYour appointment with {doctor} in {department} department on {date} has been booked successfully.\n\nThank you!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass  # just ignore email errors for now

        messages.success(request, "Your appointment request has been submitted. We’ll get in touch shortly!")
        return redirect('appointment')  # reload the page after submission

    return render(request, 'appointment.html')

@login_required
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_content = request.POST.get('message')

        # Save to database
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_content
        )

        # Optional: send email notification
        try:
            send_mail(
                subject=f"New Contact Message: {subject}",
                message=f"From: {name}\nEmail: {email}\n\nMessage:\n{message_content}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True
            )
        except Exception:
            pass  # ignore email sending errors for now

        messages.success(request, "Your message has been successfully sent. Thank you!")
        return redirect('contact')  # reload page after submission

    return render(request, 'contact.html')

@login_required
def doctors(request):
    search_query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '*')

    # Fetch all doctors from the database
    doctors = Doctor.objects.all()

    # Apply search filter
    if search_query:
        doctors = doctors.filter(
            Q(name__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(bio__icontains=search_query)
        )

    # Apply department filter
    if department_filter != '*' and department_filter:
        doctors = doctors.filter(department__iexact=department_filter)

    context = {
        'doctors': doctors,
        'search_query': search_query,
        'department_filter': department_filter,
    }
    return render(request, 'doctors.html', context)



# Create your views here.
def index(request):
    return render(request, 'index.html')
@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def department_details(request):
    return render(request, 'department_details.html')
@login_required
def department_details(request):
    return render(request, 'departments.html')
@login_required
def doctors(request):
    return render(request, 'doctors.html')
@login_required
def faq(request):
    return render(request, 'faq.html')
@login_required
def gallery(request):
    return render(request, 'gallery.html')
@login_required
def privacy(request):
    return render(request, 'privacy.html')
@login_required
def service_details(request):
    return render(request, 'service_details.html')
@login_required
def services(request):
    return render(request, 'services.html')
@login_required
def terms(request):
    return render(request, 'terms.html')
@login_required
def testimonials(request):
    return render(request, 'testimonials.html')

@login_required
def departments(request):
    return render(request, 'departments.html')



# Hardcoded doctor data (replace with actual details)
HARD_CODED_DOCTORS = {
    1: {
        'name': 'Dr. Amelia Brooks',
        'title': 'Cardiologist • MD, FACC',
        'bio': 'Specialist in heart disease prevention, diagnosis, and minimally invasive cardiac treatments.',
        'department': 'Cardiology',
        'photo': 'img/health/staff-3.webp',
        'available_this_week': True,
    },
    2: {
        'name': 'Dr. Noah Turner',
        'title': 'Pediatrician • DO',
        'bio': 'Dedicated to children’s health from infancy through adolescence with a focus on wellness and growth.',
        'department': 'Pediatrics',
        'photo': 'img/health/staff-7.webp',
        'available_this_week': True,
    },
    3: {
        'name': 'Dr. Sofia Bennett',
        'title': 'Dermatologist • MBBS, MD',
        'bio': 'Expert in skin care, acne treatment, cosmetic dermatology, and laser therapy.',
        'department': 'Dermatology',
        'photo': 'img/health/staff-12.webp',
        'available_this_week': False,
    },
    4: {
        'name': 'Dr. Ethan Cole',
        'title': 'Orthopedic Surgeon • MS, FRCS',
        'bio': 'Specializes in bone, joint, and spine surgery including sports injuries and trauma recovery.',
        'department': 'Orthopedics',
        'photo': 'img/health/staff-5.webp',
        'available_this_week': True,
    },
}
@login_required
def doctors(request):
    # If you want to get the list of doctors from a database, you can do that here. 
    # For now, we're using the hardcoded data.
    return render(request, 'doctors.html', {'doctors': HARD_CODED_DOCTORS})
@login_required
def doctor_profile(request, doctor_id):
    # Retrieve doctor data based on ID
    doctor = HARD_CODED_DOCTORS.get(doctor_id)
    if doctor:
        return render(request, 'doctor_profile.html', {'doctor': doctor})
    else:
        return render(request, '404.html')  # Return 404 if doctor not found
@login_required
def chemist(request):
    """Displays all medicines with search and filter options."""
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', 'All')

    medicines = Medicine.objects.all()

    # Apply search
    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )

    # Apply category filter
    if category_filter != 'All':
        medicines = medicines.filter(category__iexact=category_filter)

    context = {
        'medicines': medicines,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'chemist.html', context)

@login_required
def medicine_detail(request, medicine_id):
    # Fetch the medicine object from the database
    medicine = get_object_or_404(Medicine, id=medicine_id)
    
    # Render the template with the medicine object
    return render(request, 'medicine_detail.html', {'medicine': medicine})

@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if medicine is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)

    if not created:
        cart_item.quantity += 1  # If item already in cart, increase quantity
        cart_item.save()

    return redirect('chemist')  # Redirect to the chemist page


@csrf_exempt
def checkout(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None
    )
    total_amount = sum(item.item_total for item in cart.items.all())

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        # ======== Option 1: STK Push (Daraja Sandbox or Live) ========
        if payment_method == "stk_push":
            phone_number = request.POST.get("phone_number")

            if not phone_number:
                return render(
                    request,
                    "checkout.html",
                    {"cart": cart, "error": "Please enter a valid phone number.", "total": total_amount},
                )

            response = initiate_stk_push(phone_number, total_amount)

            if response.get("success"):
                message = "✅ Enter your M-Pesa PIN on your phone to complete payment."
                return render(
                    request,
                    "checkout_success.html",
                    {"message": message, "cart": cart, "total": total_amount},
                )
            else:
                message = response.get("message", "❌ Payment initiation failed. Try again.")
                return render(
                    request,
                    "checkout.html",
                    {"cart": cart, "error": message, "total": total_amount},
                )

        # ======== Option 2: Manual Payment ========
        elif payment_method == "manual":
            phone_number = request.POST.get("manual_phone_number")
            transaction_code = request.POST.get("transaction_code")

            if not phone_number or not transaction_code:
                return render(
                    request,
                    "checkout.html",
                    {
                        "cart": cart,
                        "error": "Please provide both phone number and transaction code.",
                        "total": total_amount,
                    },
                )

            # Save manual payment
            manual_payment = ManualPayment.objects.create(
                cart=cart,
                phone_number=phone_number,
                transaction_code=transaction_code,
                amount=total_amount,
                payment_date=timezone.now(),
            )

            # ✅ Auto verify the manual payment immediately
            verify_manual_payment(transaction_code)

            message = f"✅ Payment recorded and verified successfully! Transaction {transaction_code} marked as Paid."
            return render(
                request,
                "checkout_success.html",
                {"message": message, "cart": cart, "total": total_amount},
            )

    return render(request, "checkout.html", {"cart": cart, "total": total_amount})


def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    # Execute payment
    payment = Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Payment was successful
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Deduct stock based on items in the cart
        for item in cart.items.all():
            medicine = item.medicine
            medicine.stock_quantity -= item.quantity
            medicine.save()

        # Clear the cart after successful payment
        cart.items.all().delete()
        
        # Optionally, create an Order model here to save order details
        # Order.objects.create(user=request.user, total_amount=total_amount)

        return redirect('order_success')
    else:
        return JsonResponse({"error": "Payment execution failed"}, status=400)


def cancel_payment(request):
    # Redirect or show a cancel message
    return redirect('cart')  # Or any other page

def order_success(request):
    return render(request, 'order_success.html')


def cart(request):
    """ View to display the user's cart """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = sum(item.item_total for item in cart_items)
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def add_to_cart(request, medicine_id):
    """ View to add a medicine to the cart """
    medicine = Medicine.objects.get(id=medicine_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the medicine is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)
    if not created:
        # If item already exists, update quantity
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')  # Redirect to cart view

def remove_from_cart(request, medicine_id):
    """ View to remove a medicine from the cart """
    medicine = Medicine.objects.get(id=medicine_id)
    cart = Cart.objects.get(user=request.user)
    
    cart_item = CartItem.objects.filter(cart=cart, medicine=medicine).first()
    if cart_item:
        cart_item.delete()  # Remove the item from the cart
    
    return redirect('cart')


def clear_cart(request):
    """ View to clear all items from the cart """
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()  # Delete all items in the user's cart
    return redirect('cart')

def payment_history(request):
    # Show only the payments for the currently logged-in user
    payments = ManualPayment.objects.filter(cart__user=request.user).order_by("-payment_date")
    return render(request, "payment_history.html", {"payments": payments})

def verify_manual_payment(transaction_code):
    """
    Auto-verifies a manual payment entry.
    Later, you can extend this to confirm with M-Pesa API.
    """
    try:
        payment = ManualPayment.objects.get(transaction_code=transaction_code)
        payment.verified = True
        payment.verified_at = timezone.now()
        payment.save()
        return True
    except ManualPayment.DoesNotExist:
        return False


# Initialize client using .env API key
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def index(request):
    """Simple index page."""
    return render(request, "index.html")


def ai_analysis_page(request):
    """Loads the AI Health Analysis page."""
    return render(request, "ai_analysis.html")


# @csrf_exempt
# def ai_analysis(request):
#     """Handles both GET and POST for AI analysis."""
#     if request.method == "GET":
#         return render(request, "ai_analysis.html")

#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid request method."}, status=405)

#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         temperature = data.get("temperature")
#         heart_rate = data.get("heart_rate")
#         systolic = data.get("systolic")
#         diastolic = data.get("diastolic")
#         symptoms = data.get("symptoms")

#         if not all([temperature, heart_rate, systolic, diastolic]):
#             return JsonResponse({"error": "Please fill in all required fields."}, status=400)

#         prompt = f"""
#         The patient provided:
#         - Temperature: {temperature}°C
#         - Heart Rate: {heart_rate} bpm
#         - Blood Pressure: {systolic}/{diastolic} mmHg
#         - Symptoms: {symptoms}

#         As a virtual medical assistant:
#         1. Analyze these readings.
#         2. Explain what they might mean.
#         3. Suggest next steps or treatments.
#         4. Warn if the situation seems urgent.
#         """

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are a friendly and accurate AI medical assistant."},
#                 {"role": "user", "content": prompt}
#             ]
#         )

#         analysis = response.choices[0].message.content.strip()
#         return JsonResponse({"analysis": analysis})

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
@login_required
def schedule_shot(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        vaccine = request.POST.get('vaccine')
        date = request.POST.get('date')
        
        # Save vaccination appointment to the database
        appointment = VaccinationAppointment.objects.create(name=name, vaccine=vaccine, date=date)
        
        # Set the form_submitted flag to True in the context to trigger the success popup
        return render(request, 'schedule_shot.html', {'form_submitted': True, 'form_id': appointment.id})

    return render(request, 'schedule_shot.html')

def download_vaccine_form(request, vaccine_id):
    # Get the vaccination appointment from the database
    appointment = VaccinationAppointment.objects.get(id=vaccine_id)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vaccine_appointment_{appointment.id}.pdf"'
    
    # Create a PDF document
    c = canvas.Canvas(response, pagesize=letter)
    c.drawString(100, 750, f"Vaccination Appointment - {appointment.id}")
    c.drawString(100, 730, f"Name: {appointment.name}")
    c.drawString(100, 710, f"Vaccine: {appointment.vaccine}")
    c.drawString(100, 690, f"Appointment Date: {appointment.date}")
    c.drawString(100, 670, "Please go to vaccination room number 1 or 2.")
    c.drawString(100, 650, f"Date: {appointment.created_at}")
    
    c.save()
    return response

@login_required
def order_test(request):
    if request.method == 'POST':
        test_type = request.POST.get('test_type')
        email = request.POST.get('email')
        
        # Save the test order to the database
        test_order = TestOrder.objects.create(test_type=test_type, email=email)
        
        # Set the form_submitted flag to True in the context to trigger the success popup
        return render(request, 'order_test.html', {'form_submitted': True, 'form_id': test_order.id})

    return render(request, 'order_test.html')

def download_test_form(request, test_id):
    # Get the test order from the database
    test_order = TestOrder.objects.get(id=test_id)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="test_order_{test_order.id}.pdf"'
    
    # Create a PDF document
    c = canvas.Canvas(response, pagesize=letter)
    c.drawString(100, 750, f"Test Order Confirmation - {test_order.id}")
    c.drawString(100, 730, f"Test Type: {test_order.test_type}")
    c.drawString(100, 710, f"Email: {test_order.email}")
    c.drawString(100, 690, f"Please go to the laboratory for the {test_order.test_type} test.")
    c.drawString(100, 670, f"Date: {test_order.created_at}")
    
    c.save()
    return response

def download_test_form(request, test_id):
    # Get the test order from the database
    test_order = TestOrder.objects.get(id=test_id)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="test_order_{test_order.id}.pdf"'
    
    # Create a PDF document
    c = canvas.Canvas(response, pagesize=letter)
    c.drawString(100, 750, f"Test Order Confirmation - {test_order.id}")
    c.drawString(100, 730, f"Test Type: {test_order.test_type}")
    c.drawString(100, 710, f"Email: {test_order.email}")
    c.drawString(100, 690, f"Please go to the laboratory for the {test_order.test_type} test.")
    c.drawString(100, 670, f"Date: {test_order.created_at}")
    
    c.save()
    return response

def send_message(request):
    if request.method == 'POST':
        message = json.loads(request.body).get('message')
        # Save the message or handle it
        return JsonResponse({
            'status': 'Message received',
            'response': 'Thank you for your message! Our support team will get back to you soon.'
        })







# Signup View
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
        else:
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Account created successfully! You can now login.")
            return redirect('login')  # make sure your login URL name is 'login'

    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)  # Use the imported login function with alias
            return redirect('index')  # Replace with your homepage URL name
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')



# Signout View
def logout(request):
    logout(request)
    return redirect('login')





# Public list of records (anyone can view)
def records_list(request):
    records = PatientRecord.objects.all()
    return render(request, 'records_list.html', {'records': records})

# Admin/staff create record via frontend (alternatively use admin site)
@staff_member_required(login_url='signin')
def create_record(request):
    if request.method == 'POST':
        form = PatientRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_by = request.user
            record.time_in = timezone.now()
            record.save()
            messages.success(request, 'Patient record created successfully.')
            return redirect('records_list')
    else:
        form = PatientRecordForm()
    return render(request, 'create_record.html', {'form': form})

# Checkout (set time_out). Expect AJAX POST.
@login_required  # ensure some user is making the request; you can also require staff if desired
def checkout_record(request, pk):
    if request.method != 'POST':
        return HttpResponseForbidden('Only POST allowed')

    record = get_object_or_404(PatientRecord, pk=pk)

    # If already checked out, return current time_out
    if record.time_out:
        return JsonResponse({'status': 'already', 'time_out': record.time_out.isoformat()})

    record.time_out = timezone.now()
    record.save()

    # return the time_out to client (ISO string)
    return JsonResponse({'status': 'ok', 'time_out': record.time_out.isoformat()})
