from djoser.email import (
    PasswordChangedConfirmationEmail,
    PasswordResetEmail,
)


class CustomPasswordResetEmail(PasswordResetEmail):
    template_name = 'email/password_reset.html'


class CustomPasswordChangedConfirmationEmail(PasswordChangedConfirmationEmail):
    template_name = 'email/password_reset_confirmation.html'
