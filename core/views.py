from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignupForm
from pymongo import MongoClient
import pywhatkit as kit
import random
import time
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ---------- MongoDB ---------- #
client = MongoClient("mongodb://localhost:27017/")
db = client["security_app"]
users_collection = db["users"]

# ---------- Model ---------- #
model = load_model("core/phishing_model.h5")
with open("core/tokenizer.pickle", "rb") as f:
    data = pickle.load(f)
    tokenizer = data["tokenizer"]
    MAX_LENGTH = data["max_length"]

# ---------- Utils ---------- #
def generate_otp():
    return str(random.randint(100000, 999999))

def send_whatsapp_confirmation(phone_number, otp):
    try:
        message = f"Your OTP for signup is: {otp}"
        kit.sendwhatmsg_instantly(f"+92{phone_number}", message, wait_time=10, tab_close=True)
    except Exception as e:
        print("WhatsApp Error:", e)

# ---------- Views ---------- #
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            if users_collection.find_one({"email": data["email"]}):
                return HttpResponse("Email already exists")

            request.session["signup_data"] = data
            request.session["resend_count"] = 0
            request.session["otp"] = None
            request.session["otp_time"] = 0

            return redirect("verify_otp")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

def verify_otp_view(request):
    if "signup_data" not in request.session:
        return redirect("signup")

    signup_data = request.session["signup_data"]
    resend_count = request.session.get("resend_count", 0)
    session_otp = request.session.get("otp")
    otp_time = request.session.get("otp_time", 0)

    context = {
        "resend_available": False,
        "resend_count": resend_count,
        "max_resends": 3,
        "error": "",
        "otp_sent": bool(session_otp)
    }

    now = time.time()
    expired = session_otp and now - otp_time > 45
    context["resend_available"] = expired and resend_count < 3

    # First-time visit → Send OTP
    if not session_otp:
        otp = generate_otp()
        request.session["otp"] = otp
        request.session["otp_time"] = now
        send_whatsapp_confirmation(signup_data["phone"], otp)
        context["otp_sent"] = True

    if request.method == "POST":
        if "resend" in request.POST:
            if resend_count < 3:
                otp = generate_otp()
                request.session["otp"] = otp
                request.session["otp_time"] = now
                request.session["resend_count"] += 1
                send_whatsapp_confirmation(signup_data["phone"], otp)
                context["message"] = "New OTP sent!"
                context["otp_sent"] = True
            else:
                context["error"] = "Maximum resend attempts reached. Try again later."

        elif "otp" in request.POST:
            user_otp = request.POST.get("otp")
            if not session_otp or expired:
                context["error"] = "OTP expired. Please resend."
            elif user_otp == session_otp:
                users_collection.insert_one(signup_data)
                request.session.flush()
                return redirect("login")
            else:
                context["error"] = "Invalid OTP."

    return render(request, "verify_otp.html", context)

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = users_collection.find_one({"email": email, "password": password})
        if user:
            request.session["user"] = user["email"]
            return redirect("dashboard")
        else:
            return HttpResponse("Invalid credentials")
    return render(request, "login.html")

def dashboard(request):
    result = None
    if request.method == "POST":
        url = request.POST.get("url")
        if url:
            sequence = tokenizer.texts_to_sequences([url])
            padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post', truncating='post')
            prediction = model.predict(padded)[0][0]
            result = "Phishing URL ❌" if prediction >= 0.5 else "Safe URL ✅"
    return render(request, "dashboard.html", {"result": result})
