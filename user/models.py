from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from core.constants import USER_STATUS_ACTIVE, USER_STATUS_INACTIVE, USER_STATUS_REGISTER, USER_STATUS_LIST


class User(models.Model):

    STATUS_CHOICES = [
        (USER_STATUS_ACTIVE, USER_STATUS_LIST[USER_STATUS_ACTIVE]),
        (USER_STATUS_INACTIVE, USER_STATUS_LIST[USER_STATUS_INACTIVE]),
        (USER_STATUS_REGISTER, USER_STATUS_LIST[USER_STATUS_REGISTER]),
    ]

    login = models.CharField(max_length=25, unique=True, null=False, blank=False, verbose_name='Логин')
    password = models.CharField(max_length=128, null=False, blank=False, verbose_name='Пароль')
    firstName = models.CharField(max_length=25, null=True, blank=True, verbose_name='Имя')
    lastName = models.CharField(max_length=25, null=True, blank=True, verbose_name='Фамилия')
    nickName = models.CharField(max_length=25, null=False, blank=False, verbose_name='Ник')
    status = models.PositiveSmallIntegerField(default=2, choices=STATUS_CHOICES, verbose_name='Статус')
    dateCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    dateUpdate = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.login

    class Meta:
        ordering = ['login']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def setPassword(self, raw_password):
        """Установка хэша пароля."""
        self.password = make_password(raw_password)

    def checkPassword(self, raw_password):
        """Проверка пароля."""
        return check_password(raw_password, self.password)
