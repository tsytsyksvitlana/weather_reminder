from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from weather_reminder.authenticate.models.user import User


class UserRegisterForm(UserCreationForm):
    """
    Form for user registration which allows users to register by providing
    a username, email, and password. Also includes password confirmation.
    """

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserLoginForm(AuthenticationForm):
    """
    Form for user authentication which allows users
    to log in using their username and password
    """

    class Meta:
        model = User
        fields = ("username", "password")
