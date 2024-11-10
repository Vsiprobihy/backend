from djoser.email import (
    PasswordResetEmail,
    PasswordChangedConfirmationEmail,
)


class CustomPasswordResetEmail(PasswordResetEmail):
    template_name = "email/password_reset.html"


class CustomPasswordChangedConfirmationEmail(PasswordChangedConfirmationEmail):
    template_name = "email/password_reset_confirmation.html"
