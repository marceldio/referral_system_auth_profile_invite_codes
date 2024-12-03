from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import os
import random
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from referrals.sms_service import send_sms
from django.conf import settings


User = get_user_model()


class SendAuthCodeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Генерируем 4-значный код
        auth_code = random.randint(1000, 9999)

        # Получаем время жизни кода из .env (сейчас 15мин), значение по умолчанию здесь 5 мин
        timeout = int(os.getenv('AUTH_CODE_TIMEOUT', 300))

        # Сохраняем код в Redis
        cache.set(f'auth_code_{phone_number}', auth_code, timeout=timeout)

        # Проверяем, включена ли отправка SMS
        enable_sms = os.getenv('ENABLE_SMS', 'False').lower() == 'true'

        if enable_sms:
            # Отправляем код через SMS
            try:
                message = f"Ваш код для авторизации: {auth_code}"
                response = send_sms(phone_number, message)

                if response.status_code == 200:
                    return Response({'message': 'Auth code sent successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'error': 'Failed to send SMS', 'details': response.json()},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                return Response(
                    {'error': 'Error sending SMS', 'details': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            # Логируем код вместо отправки SMS
            print(f"Auth code for {phone_number}: {auth_code}")
            return Response({'message': 'Auth code generated successfully (SMS disabled)'},
                            status=status.HTTP_200_OK)


class VerifyAuthCodeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')

        if not phone_number or not auth_code:
            return Response({'error': 'Phone number and auth code are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        saved_code = cache.get(f'auth_code_{phone_number}')
        if saved_code != int(auth_code):
            raise ValidationError('Invalid or expired auth code')

        cache.delete(f'auth_code_{phone_number}')

        # Создаём пользователя, если его нет
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            user.invite_code = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))
            user.save()

        # Генерация токена
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'message': 'User verified successfully',
            'user_id': user.id,
            'access_token': access_token
        })


class ActivateInviteCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        invite_code = request.data.get('invite_code')

        if not invite_code:
            return Response({'error': 'Invite code is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, активирован ли уже инвайт-код
        if user.profile.activated_invite_code:
            return Response({'error': 'Invite code already activated'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, чтобы пользователь не использовал свой собственный инвайт-код
        if user.invite_code == invite_code:
            return Response({'error': 'You cannot activate your own invite code'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверяем существование инвайт-кода
        inviter = User.objects.filter(invite_code=invite_code).first()
        if not inviter:
            return Response({'error': 'Invalid invite code'}, status=status.HTTP_404_NOT_FOUND)

        # Сохраняем активированный код
        user.profile.activated_invite_code = invite_code
        user.profile.save()

        # Создаём связь в реферальной модели
        from .models import Referral
        Referral.objects.create(inviter=inviter, invited=user)

        return Response({'message': 'Invite code activated successfully'})


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"Authenticated user: {request.user}")
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
