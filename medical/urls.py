from django.urls import path
from medical import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Pages
    path('about/', views.about, name='about'),
    path('appointment/', views.appointment, name='appointment'),
    path('contact/', views.contact, name='contact'),
    path('department_details/', views.department_details, name='department_details'),
    path('departments/', views.departments, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('faq/', views.faq, name='faq'),
    path('gallery/', views.gallery, name='gallery'),
    path('privacy/', views.privacy, name='privacy'),
    path('service_details/', views.service_details, name='service_details'),
    path('services/', views.services, name='services'),
    path('terms/', views.terms, name='terms'),
    path('testimonials/', views.testimonials, name='testimonials'),

    # Doctors
    path('doctor_profile/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),

    # Pharmacy / Chemist
    path('chemist/', views.chemist, name='chemist'),
    path('chemist/<int:medicine_id>/', views.medicine_detail, name='medicine_detail'),

    # Cart system
    path('add_to_cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:medicine_id>/', views.add_to_cart, name='add_to_cart_alt'),
    path('cart/remove/<int:medicine_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),

    # Checkout & Payments
    path('checkout/', views.checkout, name='checkout'),
    path('payment/execute/', views.execute_payment, name='execute_payment'),
    path('payment/cancel/', views.cancel_payment, name='cancel_payment'),
    path('payment-history/', views.payment_history, name='payment_history'),

    # AI
    path('ai/', views.ai_analysis_page, name='ai_analysis_page'),
    path('ai-analysis/', views.ai_analysis, name='ai_analysis'),

    # Tests & Vaccines
    path('order-test/', views.order_test, name='order_test'),
    path('schedule-shot/', views.schedule_shot, name='schedule_shot'),
    path('download-test-form/<int:test_id>/', views.download_test_form, name='download_test_form'),
    path('download-vaccine-form/<int:vaccine_id>/', views.download_vaccine_form, name='download_vaccine_form'),

    # Auth
    path("signup/", views.signup, name="signup"),
    path("login/", views.signin, name="login"),
    path("logout/", views.logout, name="logout"),

    # Records system
    path("records/", views.records_list, name="records_list"),
    path("records/create/", views.create_record, name="create_record"),
    path("records/checkout/<int:pk>/", views.checkout_record, name="checkout_record"),
]