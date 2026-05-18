from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class AuthService:

    @staticmethod
    def register_user(form):

        try:

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )

            return user

        except Exception as e:
            raise ValidationError(
                f"Failed to create user: {str(e)}"
            )