from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os
import json

from .models import (
    Appointment,
    ContactMessage,
    Doctor,
    Cart,
    CartItem,
    Medicine,
    ManualPayment,
    Payment,
    TestOrder,
    VaccinationAppointment,
    PatientRecord,
)

from .forms import PatientRecordForm
from .utils import initiate_stk_push


# =========================================================
# HOME
# =========================================================

def index(request):
    return render(request, "index.html")


# =========================================================
# STATIC PAGES
# =========================================================

def about(request):
    return render(request, "about.html")


def departments(request):
    return render(request, "departments.html")


def department_details(request):
    return render(request, "department_details.html")


def faq(request):
    return render(request, "faq.html")


def gallery(request):
    return render(request, "gallery.html")


def privacy(request):
    return render(request, "privacy.html")


def service_details(request):
    return render(request, "service_details.html")


def services(request):
    return render(request, "services.html")


def terms(request):
    return render(request, "terms.html")


def testimonials(request):
    return render(request, "testimonials.html")


# =========================================================
# APPOINTMENT
# =========================================================

@login_required
def appointment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        department = request.POST.get("department")
        doctor = request.POST.get("doctor")
        date = request.POST.get("date")
        message_text = request.POST.get("message", "")

        Appointment.objects.create(
            name=name,
            email=email,
            phone=phone,
            department=department,
            doctor=doctor,
            date=date,
            message=message_text,
        )

        try:
            send_mail(
                subject="Appointment Confirmation",
                message=(
                    f"Dear {name},\n\n"
                    f"Your appointment with {doctor} "
                    f"in {department} department on {date} "
                    f"has been booked successfully."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(request, "Appointment booked successfully.")
        return redirect("appointment")

    return render(request, "appointment.html")


# =========================================================
# CONTACT
# =========================================================

@login_required
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message_content = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_content,
        )

        messages.success(request, "Message sent successfully.")
        return redirect("contact")

    return render(request, "contact.html")


# =========================================================
# DOCTORS
# =========================================================

HARD_CODED_DOCTORS = {
    1: {
        "name": "Dr. Amelia Brooks",
        "title": "Cardiologist • MD, FACC",
        "bio": "Heart disease specialist.",
        "department": "Cardiology",
        "photo": "img/health/staff-3.webp",
    },
    2: {
        "name": "Dr. Noah Turner",
        "title": "Pediatrician • DO",
        "bio": "Children health specialist.",
        "department": "Pediatrics",
        "photo": "img/health/staff-7.webp",
    },
    3: {
        "name": "Dr. Sofia Bennett",
        "title": "Dermatologist • MBBS, MD",
        "bio": "Skin care specialist.",
        "department": "Dermatology",
        "photo": "img/health/staff-12.webp",
    },
    4: {
        "name": "Dr. Ethan Cole",
        "title": "Orthopedic Surgeon • MS, FRCS",
        "bio": "Bone and joint specialist.",
        "department": "Orthopedics",
        "photo": "img/health/staff-5.webp",
    },
}


@login_required
def doctors(request):
    search_query = request.GET.get("search", "")
    department_filter = request.GET.get("department", "")

    doctors_queryset = Doctor.objects.all()

    if search_query:
        doctors_queryset = doctors_queryset.filter(
            Q(name__icontains=search_query)
            | Q(title__icontains=search_query)
            | Q(bio__icontains=search_query)
        )

    if department_filter:
        doctors_queryset = doctors_queryset.filter(
            department__icontains=department_filter
        )

    context = {
        "doctors": doctors_queryset,
        "hardcoded_doctors": HARD_CODED_DOCTORS,
    }

    return render(request, "doctors.html", context)


@login_required
def doctor_profile(request, doctor_id):
    doctor = HARD_CODED_DOCTORS.get(doctor_id)

    if not doctor:
        return render(request, "404.html")

    return render(request, "doctor_profile.html", {"doctor": doctor})


# =========================================================
# CHEMIST / PHARMACY
# =========================================================

@login_required
def chemist(request):
    medicines = Medicine.objects.all()

    search_query = request.GET.get("search", "")
    category_filter = request.GET.get("category", "")

    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(manufacturer__icontains=search_query)
        )

    if category_filter:
        medicines = medicines.filter(category__icontains=category_filter)

    return render(
        request,
        "chemist.html",
        {
            "medicines": medicines,
        },
    )


@login_required
def medicine_detail(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    return render(request, "medicine_detail.html", {"medicine": medicine})


# =========================================================
# CART
# =========================================================

@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        medicine=medicine,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.item_total for item in cart_items)

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total_price": total_price,
        },
    )


@login_required
def remove_from_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    cart = get_object_or_404(Cart, user=request.user)

    cart_item = CartItem.objects.filter(
        cart=cart,
        medicine=medicine,
    ).first()

    if cart_item:
        cart_item.delete()

    return redirect("cart")


@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)

    cart.items.all().delete()

    return redirect("cart")


# =========================================================
# CHECKOUT
# =========================================================

@login_required
@csrf_exempt
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    total_amount = sum(item.item_total for item in cart.items.all())

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        if payment_method == "stk_push":
            phone_number = request.POST.get("phone_number")

            response = initiate_stk_push(phone_number, total_amount)

            if response.get("success"):
                return render(
                    request,
                    "checkout_success.html",
                    {
                        "message": "STK Push sent successfully.",
                    },
                )

            return render(
                request,
                "checkout.html",
                {
                    "cart": cart,
                    "total": total_amount,
                    "error": response.get("message"),
                },
            )

        elif payment_method == "manual":
            phone_number = request.POST.get("manual_phone_number")
            transaction_code = request.POST.get("transaction_code")

            ManualPayment.objects.create(
                cart=cart,
                phone_number=phone_number,
                transaction_code=transaction_code,
                amount=total_amount,
                payment_date=timezone.now(),
            )

            return render(
                request,
                "checkout_success.html",
                {
                    "message": "Manual payment submitted successfully.",
                },
            )

    return render(
        request,
        "checkout.html",
        {
            "cart": cart,
            "total": total_amount,
        },
    )


def execute_payment(request):
    return JsonResponse({"message": "Payment executed successfully."})


def cancel_payment(request):
    return redirect("cart")


@login_required
def payment_history(request):
    payments = ManualPayment.objects.filter(
        cart__user=request.user
    ).order_by("-payment_date")

    return render(
        request,
        "payment_history.html",
        {
            "payments": payments,
        },
    )


# =========================================================
# AI ANALYSIS
# =========================================================

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)


def ai_analysis_page(request):
    return render(request, "ai_analysis.html")


@csrf_exempt
def ai_analysis(request):
    if request.method == "GET":
        return render(request, "ai_analysis.html")

    try:
        client = get_openai_client()

        if not client:
            return JsonResponse(
                {"error": "OpenAI API key missing."},
                status=500,
            )

        data = json.loads(request.body)

        prompt = f"""
        Temperature: {data.get('temperature')}
        Heart Rate: {data.get('heart_rate')}
        Blood Pressure: {data.get('systolic')}/{data.get('diastolic')}
        Symptoms: {data.get('symptoms')}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return JsonResponse(
            {
                "analysis": response.choices[0].message.content
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# =========================================================
# TESTS
# =========================================================

@login_required
def order_test(request):
    if request.method == "POST":
        test_type = request.POST.get("test_type")
        email = request.POST.get("email")

        test_order = TestOrder.objects.create(
            test_type=test_type,
            email=email,
        )

        return render(
            request,
            "order_test.html",
            {
                "form_submitted": True,
                "form_id": test_order.id,
            },
        )

    return render(request, "order_test.html")


@login_required
def download_test_form(request, test_id):
    test_order = get_object_or_404(TestOrder, id=test_id)

    response = HttpResponse(content_type="application/pdf")

    response[
        "Content-Disposition"
    ] = f'attachment; filename="test_order_{test_order.id}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    pdf.drawString(100, 750, f"Test Order #{test_order.id}")
    pdf.drawString(100, 730, f"Test Type: {test_order.test_type}")
    pdf.drawString(100, 710, f"Email: {test_order.email}")

    pdf.save()

    return response


# =========================================================
# VACCINATION
# =========================================================

@login_required
def schedule_shot(request):
    if request.method == "POST":
        name = request.POST.get("name")
        vaccine = request.POST.get("vaccine")
        date = request.POST.get("date")

        appointment = VaccinationAppointment.objects.create(
            name=name,
            vaccine=vaccine,
            date=date,
        )

        return render(
            request,
            "schedule_shot.html",
            {
                "form_submitted": True,
                "form_id": appointment.id,
            },
        )

    return render(request, "schedule_shot.html")


@login_required
def download_vaccine_form(request, vaccine_id):
    appointment = get_object_or_404(
        VaccinationAppointment,
        id=vaccine_id,
    )

    response = HttpResponse(content_type="application/pdf")

    response[
        "Content-Disposition"
    ] = f'attachment; filename="vaccine_{appointment.id}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)

    pdf.drawString(100, 750, f"Vaccination #{appointment.id}")
    pdf.drawString(100, 730, f"Name: {appointment.name}")
    pdf.drawString(100, 710, f"Vaccine: {appointment.vaccine}")

    pdf.save()

    return response


# =========================================================
# AUTH
# =========================================================

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )

        user.save()

        messages.success(request, "Account created successfully.")

        return redirect("login")

    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            auth_login(request, user)
            return redirect("index")

        messages.error(request, "Invalid credentials.")

    return render(request, "login.html")


def logout_view(request):
    auth_logout(request)
    return redirect("login")


# =========================================================
# RECORDS
# =========================================================

@login_required
def records_list(request):
    records = PatientRecord.objects.all()

    return render(
        request,
        "records_list.html",
        {
            "records": records,
        },
    )


@staff_member_required(login_url="login")
def create_record(request):
    if request.method == "POST":
        form = PatientRecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)

            record.created_by = request.user
            record.time_in = timezone.now()

            record.save()

            messages.success(request, "Record created successfully.")

            return redirect("records_list")

    else:
        form = PatientRecordForm()

    return render(
        request,
        "create_record.html",
        {
            "form": form,
        },
    )


@login_required
def checkout_record(request, pk):
    if request.method != "POST":
        return HttpResponseForbidden("Only POST allowed")

    record = get_object_or_404(PatientRecord, pk=pk)

    if record.time_out:
        return JsonResponse(
            {
                "status": "already",
                "time_out": record.time_out.isoformat(),
            }
        )

    record.time_out = timezone.now()
    record.save()

    return JsonResponse(
        {
            "status": "ok",
            "time_out": record.time_out.isoformat(),
        }
    )