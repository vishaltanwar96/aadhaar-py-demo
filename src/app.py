from flask_wtf import FlaskForm, CSRFProtect
from wtforms import validators, IntegerField, ValidationError
from aadhaar.exceptions import MalformedIntegerReceived
from flask.blueprints import Blueprint

from flask.views import View
from flask import render_template, request, flash, Flask
from aadhaar.qr import AadhaarSecureQR
import os


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


class IndexView(View):

    def dispatch_request(self):
        qr_code_input_form = QRCodeInputForm()
        if request.method == 'GET':
            return render_template('index.html', form=qr_code_input_form)
        elif request.method == 'POST':
            if not qr_code_input_form.validate():
                flash(qr_code_input_form.errors['qr_code_data'][0])
                return render_template('index.html', form=qr_code_input_form)
            else:
                qr_code_data = request.form['qr_code_data']
                return render_template('qr_data.html', qr_code_data=AadhaarSecureQR(qr_code_data).extract_data())


core = Blueprint('core', __name__)
core.add_url_rule('/', view_func=IndexView.as_view(name='index'), methods=('GET', 'POST'))
app = Flask(__name__)
CSRFProtect(app)
app.register_blueprint(core)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if __name__ == "__main__":
    app.run()
