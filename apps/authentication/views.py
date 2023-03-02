from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate

from .models import User
from .forms import UserRegistrationForm, UserConfirmForm, UserLoginForm
from .services.confirm_code import CodeConfirm


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'auth/registration.html'

    def form_valid(self, form):
        code = CodeConfirm(self.request, email=form.cleaned_data['email'])
        code.craete()
        code.send_code_to_email()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return f'confirm/{self.object.id}'


class UserConfirmView(UpdateView):
    model = User
    form_class = UserConfirmForm
    template_name = 'auth/confirm.html'
    success_url = '/auth/login'

    def form_valid(self, form):
        code = CodeConfirm(self.request)
        form_code = form.cleaned_data['code']
        if code.check(form_code):
            code.clean()
            return super().form_valid(form)
        form.add_error('code', 'Неверный код подтверждения')
        return super().form_invalid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'auth/login.html'

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        if not user:
            return super().form_valid(form)
        if not user.is_confirmed:
            return redirect('register_confirm', pk=user.id)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return '/order/all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('next'):
            context['message'] = \
                'Для продолжения вам необходимо авторизоваться'
        return context
