# pylint: disable=all

import re

from pydantic import BaseModel, EmailStr, constr, validator, root_validator


class RegisterUserRequest(BaseModel):
    """
    Регистрация пользователя
    """

    email: EmailStr | None
    phone: str | None

    password: constr(min_length=8, max_length=64)

    # @validator('password')
    # def password_must_contain_special_characters(cls, v):
    #     if not re.search(r'[^a-zA-Z0-9]', v):
    #         raise ValueError('Пароль должен содержать спец. символы')
    #     return v

    @validator('password')
    def password_must_contain_numbers(cls, v):
        if not re.search(r'[0-9]', v):
            raise ValueError('Пароль должен содержать цифры')
        return v

    # @validator('password')
    # def password_must_contain_uppercase(cls, v):
    #     if not re.search(r'[A-Z]', v):
    #         raise ValueError('Пароль должен содержать большие буквы')
    #     return v

    @validator('password')
    def password_must_contain_lowercase(cls, v):
        if not re.search(r'[a-z]', v):
            raise ValueError('Пароль должен содержать маленькие буквы')
        return v

    @validator('phone')
    def phone_format(cls, value):
        if not re.match(r'\+79\d{8}', value):
            raise ValueError('Номер телефона должен соответстовать формату +79XXXXXXXX.')
        return value

    @root_validator
    def email_or_phone_required(cls, values: dict) -> dict:
        if not (values.get('email') or values.get('phone')):
            raise ValueError('Должны быть указаны номер телефона или адрес электронной почты.')
        return values


class LoginUserRequest(BaseModel):
    email: EmailStr | None
    phone: str | None
    password: str

    @root_validator
    def email_or_phone_required(cls, values: dict) -> dict:
        if not (values.get('email') or values.get('phone')):
            raise ValueError('Должны быть указаны номер телефона или адрес электронной почты.')
        return values
