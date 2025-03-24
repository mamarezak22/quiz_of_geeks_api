from django.core.validators import RegexValidator

class PhoneNumberValidator(RegexValidator):
    regex = r'^09\d{9}$'
    message = 'phone number is invalid'
    code = "invalid"