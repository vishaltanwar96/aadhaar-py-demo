from flask_wtf import FlaskForm
from wtforms import validators, IntegerField, SubmitField, ValidationError
from aadhaar.qr import AadhaarSecureQR
from aadhaar.exceptions import MalformedIntegerReceived


class QRCodeInputForm(FlaskForm):
    qr_code_data = IntegerField(
        label='Scanned data from Secure Aadhaar QR Code',
        validators=[validators.InputRequired()],
    )

    def validate_qr_code_data(self, field):
        try:
            AadhaarSecureQR(field.data)
        except MalformedIntegerReceived:
            raise ValidationError('The data cannot be decoded')
        except TypeError:
            raise ValidationError('Please send the valid QR data')

