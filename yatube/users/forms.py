from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PasswordCgangeForm(PasswordChangeForm):
    model = User
    fields = ('текущий пароль', 'новый пароль', 'новый пароль (повторно)')
