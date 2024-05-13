from django.shortcuts import render

from django.contrib.auth.views import LoginView as BaseLogin
from django.contrib.auth.views import LogoutView as BaseLogout
from django.contrib.auth.hashers import make_password
from django.views.generic import CreateView, UpdateView, View
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.contrib import messages
from django.template.loader import render_to_string

from django.conf import settings
from users.forms import UserForm, UserRegisterForm
from users.models import User


class LoginView(BaseLogin):
    template_name = "users/login.html"
    # success_url = '/'  # URL, на который нужно перенаправить пользователя после успешной аутентификации
    # form_class = UserForm


class LogoutView(BaseLogout):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = "users/register.html"

    def form_valid(self, form):
        new_user = form.save()

        token = default_token_generator.make_token(new_user)
        new_user.verification_token = token
        new_user.save()

        verify_url = self.request.build_absolute_uri(
            reverse_lazy('users:verify_email', kwargs={'pk': new_user.pk, 'token': token})
        )

        send_mail(
            subject='Мои поздравления',
            message=f'Ты один из нас, бобро пожаловать. \nПройди по ссылке для активации аккаунта '
                    f'{verify_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class VerifyEmailView(View):
    def get(self, request, pk, token):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")

        if user.verification_token == token:
            user.is_active = True
            user.save()
            messages.success(request, 'Ваш аккаунт успешно активирован. Вы можете войти.')
            return redirect('users:login')
        else:
            messages.error(request, 'Неверная ссылка для верификации. Пожалуйста, свяжитесь с администратором.')
            return redirect('users:login')


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = User.objects.make_random_password()
    print(new_password)
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:login'))

