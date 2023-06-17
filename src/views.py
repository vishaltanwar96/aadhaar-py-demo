from flask.views import View
from flask import render_template, request, flash
from aadhaar.qr import AadhaarSecureQR


from forms import QRCodeInputForm


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
