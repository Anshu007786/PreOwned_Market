import imp
from django.conf import settings
from django.core.mail import EmailMessage




def SendAccountActivationEmail(email , emailToken):
    subject = 'PreOwned Market account needs verification!'
    emailFrom = settings.EMAIL_HOST_USER
    message = f'Hey, your PreOwned Market profile needs to be verified. Click on the link to proceed http://127.0.0.1:8000/accounts/activate/{emailToken}'
    print (message)
    msg = EmailMessage(subject , message , emailFrom , [email])
    msg.send()
    return True
