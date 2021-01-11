from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout, get_user_model
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q

from utils.api import APIView, validate_serializer

from account.permissions import login_required

from .models import User, UserProfile

from .serializers import (
    UserLoginSerializer,
    UserRegisterSerializer,
    UserProfileSerializer,
    EditUserProfileSerializer,
    UsernameOrEmailCheckSerializer,
)

User = get_user_model()

# Create your views here.
class UserLoginAPIView(APIView):
    @validate_serializer(UserLoginSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data

        credential = {
            'username': data.get('username'),
            'password': data.get('password')
        }
        user = authenticate(request, **credential)
        if user:
            login(request, user)
            return self.success("Succeeded")
        else:
            return self.error(HTTPStatus.BAD_REQUEST, err="Invalid username or password")


class UserLogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return self.success("Succeedded")


class UserRegisterAPIView(APIView):
    @validate_serializer(UserRegisterSerializer)
    def post(self, request):
        """
            global disable check
        """

        data = request.data
        data["username"] = data["username"].lower()
        data["email"] = data["email"].lower()

        if User.objects.filter(Q(username=data["username"]) | Q(email=data["email"])).exists():
            return self.error(HTTPStatus.BAD_REQUEST, err="username or email is already exists")
                
        user = User.objects.create(
            username=data["username"],
            email=data["email"],
        )
        user.set_password(data["password"])
        user.save()

        UserProfile.objects.create(user=user)
        return self.success("succeeded")

class UserProfileAPIView(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return self.success()

        username = request.GET.get("username", None)
        try:
            if username:
                user = User.objects.get(username=username)
            else:
                user = request.user
        except User.DoesNotExist:
            return self.error(HTTPStatus.BAD_REQUEST, "User does not exist")

        resp_data = UserProfileSerializer(user.userprofile).data
        return self.success(resp_data)

    @validate_serializer(EditUserProfileSerializer)
    @login_required
    def put(self, request):
        data = request.data
        user_profile = request.user.userprofile

        for k, v in data.items():
            setattr(user_profile, k, v)
        
        user_profile.save()
        return self.success(UserProfileSerializer(user_profile).data)
        

class UsernameOrEmailCheck(APIView):
    @validate_serializer(UsernameOrEmailCheckSerializer)
    def post(self, request):
        data = request.data
        username = data.get('username', '').lower()
        email = data.get('email', '').lower()

        result = {
            "username": False,
            "email": False
        }

        if User.objects.filter(username=username).exists():
            result['username'] = True

        if User.objects.filter(email=email).exists():
            result['email'] = True

        return self.success(data=result)
