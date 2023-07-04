from django.conf import settings
from twilio.rest import Client
import random

class MessaHandler:
    phone_number = None
    otp = None

    def __int__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def send_otp_on_phone( self ):
        client = Client (settings.SID, settings.AUTH_TOKEN )

        message = client.messages.create (
                                    body=f'Your otp is {self.otp}',
                                    from_= '+14179813832',
                                    to=self.phone_number,
                                )