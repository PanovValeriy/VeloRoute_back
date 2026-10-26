from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.constants import USER_STATUS_ACTIVE, USER_STATUS_INACTIVE, USER_STATUS_REGISTER
from user.crud import registerUser, findUserLogin, cancelRegisterUser, checkUserStatus
from user.serializers import UserDetailSerializer
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([AllowAny])
def view_register(request):
    login = request.data.get('login', '').strip()
    password = request.data.get('password', '').strip()
    firstName = request.data.get('firstName', '').strip()
    lastName = request.data.get('lastName', '').strip()
    nickName = request.data.get('nickName', '').strip()
    if nickName == '':
        nickName = login

    result = registerUser(login, password, firstName, lastName, nickName)
    if result['status'] == 'error':
        return Response(
            {'detail': result['message']},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {'user':UserDetailSerializer(result['user']).data},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def view_register_cancel(request):
    login = request.data.get('login', '')
    password = request.data.get('password', '')
    result = cancelRegisterUser(login, password)
    if result['status'] == 'error':
        return Response({'detail': result['message']}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail':result['message']}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def view_login(request):
    login = request.data.get('login', '').strip()
    password = request.data.get('password', '').strip()
    if not login or not password:
        return Response({
                'detail': 'Укажите логин и пароль'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    result = findUserLogin(login)
    if result['status'] == 'error':
        return Response(
            {
                'detail': 'Неверный логин или пароль'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    elif not result['user'].checkPassword(password):
        return Response(
            {
                'detail': 'Неверный логин или пароль'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    if result['user'].status == USER_STATUS_INACTIVE:
        return Response(
            {
                'detail': 'Ваш аккаунт заблокирован'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    elif result['user'].status == USER_STATUS_REGISTER:
        return Response(
            {
                'detail': 'Ваш аккаунт ожидает подтверждения'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    elif result['user'].status != USER_STATUS_ACTIVE:
        return Response({
                'detail': 'Неизвестная ошибка авторизации'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    user_auth = authenticate(request, username=login, password=password)
    if user_auth:
        token, created = Token.objects.get_or_create(user=user_auth)
        serializer = UserDetailSerializer(result['user'])
        return Response(
        {
                'token': token.key,
                'user': serializer.data,
            },
            status=status.HTTP_200_OK)

    return Response(
    {
            'detail': 'Неверный логин или пароль'
        },
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def view_logout(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
    except Token.DoesNotExist:
        pass

    return Response(
        {'status': 'success'},
        status=status.HTTP_200_OK
    )

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def view_profile(request):
    loginUser = checkUserStatus(request.user.username)
    if loginUser['status'] == 'error':
        return Response(
            {'detail': loginUser['message']},
            status=status.HTTP_401_UNAUTHORIZED
        )
    result = findUserLogin(request.user.username)
    if result['status'] == 'success':
        serializer = UserDetailSerializer(result['user'])
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'detail': 'Пользователь не найден'},
            status=status.HTTP_401_UNAUTHORIZED,
        )