from core.constants import USER_STATUS_REGISTER, USER_STATUS_ACTIVE, USER_STATUS_INACTIVE
from user.models import User

def registerUser(login, password, firstName, lastName, nickName):
    if not login or not password:
        return {
                'user': None,
                'status': 'error',
                'message': 'Укажите логин и пароль'
                }
    if User.objects.filter(login=login).exists():
        return {
                'user': None,
                'status': 'error',
                'message': 'Логин уже занят'
                }
    user = User(
        login=login,
        firstName=firstName,
        lastName=lastName,
        nickName=nickName,
        status=USER_STATUS_REGISTER
    )
    user.setPassword(password)
    user.save()
    return {
            'user': user,
            'status': 'success',
            'message': 'Заявка на регистрацию пользователя создана успешно'
            }

def cancelRegisterUser(login, password):
    if not login or not password:
        return {
                'user': None,
                'status': 'error',
                'message': 'Укажите логин и пароль'
                }
    users = User.objects.filter(login=login, status=2)
    if len(users) == 0:
        return {
                'status': 'error',
                'message': 'Заявка не найдена'
                }

    if not users[0].checkPassword(password):
        return {
            'status': 'error',
            'message': 'Неверный логин или пароль'
        }
    try:
        users[0].delete()
        return {
            'status': 'success',
            'message': 'Заявка удалена успешно'
        }

    except:
        return {
            'status': 'error',
            'message': 'Ошибка удаления заявки'
        }


def readUser(idUser):
    try:
        user = User.objects.get(id=idUser)
        return {
                'user': user,
                'status': 'success',
                'message': 'Пользователь найден'
                }
    except:
        return {
                'user': None,
                'status': 'error',
                'message': 'Пользователь не найден'
                }


def updateUser(idUser, password=None, firstName=None, lastName=None, nickName=None):
    try:
        user = User.objects.get(id=idUser)
    except:
        return {
                'user': None,
                'status': 'error',
                'message': 'Пользователь не найден'
                }
    if password != None:
        user.setPassword(password)
    if firstName != None:
        user.firstName = firstName
    if lastName != None:
        user.lastName = lastName
    if nickName != None:
        user.nickName = nickName
    user.save()
    return {
            'user': user,
            'status': 'success',
            'message': 'Пользователь обновлен успешно'
            }


def findUserLogin(login):
    try:
        user = User.objects.get(login=login)
        return {
                'user': user,
                'status': 'success',
                'message': 'Пользователь найден успешно'
                }
    except:
        return {
                'user': None,
                'status': 'error',
                'massage': 'Пользователь на найден'
                }

def checkUserStatus(login):
    try:
        user = User.objects.get(login=login)
        if user.status == USER_STATUS_ACTIVE:
            return {
                'user': user,
                'status': 'success',
                'message': 'Пользователь активен'
            }
        elif user.status == USER_STATUS_REGISTER:
            return {
                'user': None,
                'status': 'error',
                'message': 'Пользователь на регистрации'
            }
        elif user.status == USER_STATUS_INACTIVE:
            return {
                'user': None,
                'status': 'error',
                'message': 'Пользователь заблокирован'
            }
        else:
            return {
                'user': None,
                'status': 'error',
                'message': 'Неизвестный статус'
            }
    except:
        return {
            'user': None,
            'status': 'error',
            'message': 'Пользователь не найден'
        }