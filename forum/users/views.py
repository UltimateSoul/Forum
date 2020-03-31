from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.tasks import send_confirmation_email
from users.serializers import RegisterUserSerializer
from users.tokens import account_activation_token

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        user_serializer = RegisterUserSerializer(data=data)
        if user_serializer.is_valid():

            user = User.objects.create_user(
                **user_serializer.data,
                is_active=False
            )
            token = Token.objects.get(user=user)
            email_token = account_activation_token.make_token(user)
            current_site = get_current_site(request)
            send_confirmation_email.delay(user_pk=user.id,
                                          current_site=current_site,
                                          token=email_token,
                                          user_email=user.email)
            # settings.BASE_DIR  ToDo: add default image (situated in static folder)
            return Response(data={'auth_token': token.key})
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailConfirmationHandleView(View):

    def get(self, request, uidb64, token, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')