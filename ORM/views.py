from django.shortcuts import render, redirect
from django.views import View
from .models import User, ResetUuid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Mail Imports
from django.core.mail import send_mail
from django.conf import settings

# UUID Generation, Expiry Time & timezone
import uuid, random, datetime
from pytz import timezone


# Create your views here.
# To restrict the Access
class Index(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "index.html")


class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user != None:
                login(request, user)
                return redirect("index/")
            else:
                print("Invalid Credentials!!")
        else:
            print("Username Not Found!!")

        return render(request, "login.html")


class Register(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone = request.POST.get("phoneNo")

        if User.objects.filter(email=email).exists():
            print("Email Already Exist!!")
        elif User.objects.filter(username=username).exists():
            print("Username Already Exists!!")
        else:
            User.objects.create_user(
                first_name=firstName,
                last_name=lastName,
                email=email,
                username=username,
                phone=phone,
                password=password,
            )
            print("REGISTERED!")
            return redirect("/")

        return render(request, "signup.html")


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class Forgot(View):
    def get(self, request):
        return render(request, "forgot.html")

    def post(self, request):
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():

            user = User.objects.get(email=email)
            forgot_id = uuid.uuid1(random.randint(0, 281474976710655))
            current_time = datetime.datetime.now()
            expiry_date = current_time + datetime.timedelta(hours=2)
            if current_time < expiry_date:
                expiry_flag = True
            else:
                expiry_flag = False

            forgot = ResetUuid(
                UUID=forgot_id,
                user=user,
                expiry=expiry_date,
                expiry_flag=expiry_flag,
            )
            forgot.save()

            URL = f"{settings.SITE_URL}/{forgot_id}"

            if email:
                subject = "Password Reset Request"
                message = (
                    "To reset your password, click the link below to get started:\n"
                    f"Reset your password\n\t{URL}"
                )

                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                    print(
                        f"\nSubject = {subject}\nmessage = {message}\nHOST = {settings.EMAIL_HOST_USER}\nmail = {email}"
                    )

                    return redirect("/")
                except Exception as e:
                    return render(request, "forgot.html")
            else:
                return render(request, "forgot.html")
        else:
            print(f"Invalid Email Address {email}")
        return render(request, "forgot.html")


class Reset(View):
    def get(self, request, uuid):
        return render(request, "resetPassword.html", {"uuid": uuid})

    def post(self, request, uuid):
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        current_datatime = datetime.datetime.now()

        reset_uuid = ResetUuid.objects.get(UUID=uuid)
        user = reset_uuid.user
        current_time = current_datatime.astimezone(timezone("UTC"))
        print(current_time)

        if current_time < reset_uuid.expiry and new_password == confirm_password:
            user.set_password(confirm_password)
            user.save()
            return redirect("/")
        else:
            return redirect("/")
