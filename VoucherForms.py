
from wtforms import Form, StringField, TextAreaField, validators, IntegerField, SelectField
from wtforms.fields import DateField
from datetime import datetime
from wtforms.validators import ValidationError
from flask_wtf.file import FileField

class CreateVoucherForm(Form):

    def validate_date(form, field):
        if field.data < datetime.date(datetime.now()):
            raise ValidationError("Date cannot be earlier than today's date")

    picture = SelectField("Image:", choices=[("voucher1.png", "Cash"), ("voucher2.png", "Discount"), ("voucher3.png", "Free Shipping")])
    name = StringField('Voucher Name', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Regexp('^\w+', message="Voucher name must contain only letters numbers or underscore")])
    type = SelectField("Voucher Type", [validators.DataRequired()], choices=[("$", "$"), ("%", "%"), ("Gift", "Free")])
    amount = IntegerField('Amount Off ($/%)', [validators.NumberRange(min=0), validators.InputRequired()], render_kw={'style': 'width: 8ch'})
    min_spend = IntegerField('Min. Spend ($)', [validators.InputRequired(), validators.NumberRange(min=0)], render_kw={'style': 'width: 8ch'})
    expiry = DateField('Expiry Date', [validators.DataRequired(), validate_date], format='%Y-%m-%d', default=datetime.now, render_kw={'style': 'width: 20ch'})
    description = TextAreaField('Description', [validators.DataRequired(), validators.Length(min=1, max=150), validators.Regexp('^\w+', message="Voucher name must contain only letters numbers or underscore")])
    status = SelectField('Status', [validators.DataRequired()], choices=[("Active", "Active"), ("Inactive", "Inactive")])
