from django.contrib.auth.views import LoginView as BaseLogin
from django.contrib.auth.views import LogoutView as BaseLogout

from django.views.generic import CreateView, UpdateView, View, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.contrib import messages

from users.forms import UserForm, UserRegisterForm
from users.models import User
from users.services import my_send_mail


class LoginView(BaseLogin):
    template_name = "users/login.html"


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
            reverse_lazy('users:verify_email',
                         kwargs={'pk': new_user.pk, 'token': token})
        )
        my_send_mail(email=new_user.email, url=verify_url)
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
            return redirect('users:register_done')
        else:
            return redirect('users:register_fail')


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class RegisterDoneView(TemplateView):
    template_name = 'users/register_done.html'
    extra_context = {
        'answer': 'Ваш аккаунт успешно активирован. Вы можете войти.'
    }


class RegisterFailView(TemplateView):
    template_name = 'users/register_fail.html'
    extra_context = {
        'answer': 'Неверная ссылка для верификации. '
                  'Пожалуйста, свяжитесь с руководством.'
    }
