from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Appointment(models.Model):
    DEPARTMENT_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('dermatology', 'Dermatology'),
        ('general', 'General Medicine'),
    ]

    DOCTOR_CHOICES = [
        ('dr-johnson', 'Dr. Sarah Johnson'),
        ('dr-martinez', 'Dr. Michael Martinez'),
        ('dr-chen', 'Dr. Lisa Chen'),
        ('dr-patel', 'Dr. Raj Patel'),
        ('dr-williams', 'Dr. Emily Williams'),
        ('dr-thompson', 'Dr. David Thompson'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    doctor = models.CharField(max_length=50, choices=DOCTOR_CHOICES)
    date = models.DateField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.department} with {self.doctor} on {self.date}"



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"



class Doctor(models.Model):
    DEPARTMENTS = [
        ('Cardiology', 'Cardiology'),
        ('Pediatrics', 'Pediatrics'),
        ('Dermatology', 'Dermatology'),
        ('Orthopedics', 'Orthopedics'),
        ('General Surgery', 'General Surgery'),
    ]

    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)  # e.g., "Pediatrician • DO"
    bio = models.TextField()
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    available_this_week = models.BooleanField(default=True)
    years_experience = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=100, blank=True)
    certifications = models.CharField(max_length=200, blank=True)
    residency = models.CharField(max_length=200, blank=True)
    fellowship = models.CharField(max_length=200, blank=True)
    publications = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name






class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('Painkiller', 'Painkiller'),
        ('Antibiotic', 'Antibiotic'),
        ('Vitamin', 'Vitamin'),
        ('Antiseptic', 'Antiseptic'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Other')
    manufacturer = models.CharField(max_length=150, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='medicines/', null=True, blank=True)
    expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 👇 Added fields for payment routing
    seller_name = models.CharField(max_length=100, help_text="Name of the doctor or chemist selling this medicine.")
    seller_mpesa_number = models.CharField(
        max_length=15,
        help_text="The M-Pesa number that will receive payment for this medicine (e.g., 254712345678)."
    )

    def __str__(self):
        return f"{self.name} - Sold by {self.seller_name}"

    def is_in_stock(self):
        return self.stock_quantity > 0

    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_total(self):
        """Calculate the total price for this cart item (price * quantity)."""
        return self.medicine.price * self.quantity

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity}"



class ManualPayment(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    transaction_code = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)  # ✅ add this field
    verified_at = models.DateTimeField(null=True, blank=True)  # ✅ optional timestamp

    def __str__(self):
        return f"{self.transaction_code} - {'Paid' if self.verified else 'Pending'}"




class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_code = models.CharField(max_length=50, blank=True, null=True)
    payment_method = models.CharField(max_length=50, default="Manual M-Pesa")
    payment_date = models.DateTimeField()
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.status})"



class TestOrder(models.Model):
    test_type = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

class VaccinationAppointment(models.Model):
    name = models.CharField(max_length=255)
    vaccine = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)




GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class PatientRecord(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    reason_for_visit = models.CharField(max_length=255)
    medical_history = models.TextField(blank=True)
    attending_doctor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='patient_records')
    time_in = models.DateTimeField(default=timezone.now)
    time_out = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_patient_records')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_in']

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.reason_for_visit}"

    @property
    def is_checked_out(self):
        return self.time_out is not None
