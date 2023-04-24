import datetime
from datetime import datetime
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField, PasswordField, TelField, DateField, IntegerField
from wtforms.validators import ValidationError
import re


def check_phone(Form, field):
    if not re.match(r'^[89][0-9]{7}$', str(field.data)):
        raise validators.ValidationError('Invalid phone number,it must start with either 8 or 9 and be 8 digit long')


class CreateStaffForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', choices=[('Female', 'Female'), ('Male', 'Male'), ('Other', ' Other')], default='F')
    phone_number = TelField('Phone Number', [validators.DataRequired(), check_phone])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    departments = RadioField('Departments', choices=[('A', 'Administrators'), ('P', 'Products'), ('E', 'Events'), ('R', 'Rewards'), ('S', 'After-Sales')], default='A')
    job_name = StringField('Job Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    password = PasswordField(validators=[validators.DataRequired(), validators.Regexp(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$",
        message="Invalid password. It must contain a minimum eight and maximum 10 characters, at least one uppercase "
                "letter, one lowercase letter, one number and one special character.")])
    confirm_password = PasswordField(validators=[validators.EqualTo('password', 'Password mismatch')])

class UpdateStaffForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', choices=[('Female', 'Female'), ('Male', 'Male'), ('Other', ' Other')], default='F')
    phone_number = TelField('Phone Number', [validators.DataRequired(), check_phone])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    departments = RadioField('Departments', choices=[('A', 'Administrators'), ('P', 'Products'), ('E', 'Events'), ('R', 'Rewards'), ('S', 'After-Sales')], default='A')
    job_name = StringField('Job Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])


class CreateCustomerForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', choices=[('Female', 'Female'), ('Male', 'Male'), ('Other', ' Other')], default='F')
    birthday = DateField('Birthday', format='%Y-%m-%d')  # in update from profile
    occupation = StringField('Occupation', [validators.Length(min=1, max=150), validators.DataRequired()])
    phone_number = TelField('Phone Number', [validators.DataRequired(), check_phone])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    password = PasswordField(validators=[validators.DataRequired(), validators.Regexp(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$",
        message="Invalid password. It must contain a minimum eight and maximum 10 characters, at least one uppercase "
                "letter, one lowercase letter, one number and one special character.")])
    confirm_password = PasswordField(validators=[validators.EqualTo('password', 'Password mismatch')])


class UpdateCustomerForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', choices=[('Female', 'Female'), ('Male', 'Male'), ('Other', ' Other')], default='F')
    birthday = DateField('Birthday', format='%Y-%m-%d')  # in update from profile
    occupation = StringField('Occupation', [validators.Length(min=1, max=150), validators.DataRequired()])
    phone_number = TelField('Phone Number', [validators.DataRequired(), check_phone])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[validators.DataRequired(), validators.Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$', message="Invalid password. It must contain at least one uppercase letter, one lowercase letter, one digit, one special character and be at least 8 characters long.")])
    password = PasswordField(validators=[validators.DataRequired(), validators.Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$', message="Invalid password. It must contain at least one uppercase letter, one lowercase letter, one digit, one special character and be at least 8 characters long.")])
    confirm_password = PasswordField(validators=[validators.EqualTo('password', 'Password mismatch'),validators.DataRequired()])

class CreateReturnForm(Form):
    def validate_date(form, field):
        if field.data < datetime.date(datetime.now()):
            raise ValidationError('Return date cannot be in the past')

    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    orderid = StringField('Order ID', [validators.Length(min=1, max=150), validators.DataRequired()])
    returnreason = TextAreaField('Return Reason', [validators.DataRequired()])
    contact = IntegerField('Contact Number (+65)', [validators.number_range(min=10000000, max=99999999), validators.DataRequired()])
    address = TextAreaField('Address', [validators.length(max=200), validators.DataRequired()])
    returnoption = RadioField('Preferred return option', choices=[('P', 'Pickup'), ('D', 'Dropoff')])
    returndate = DateField('Preferred return date', format='%Y-%m-%d', validators=[validate_date])
    remarks = TextAreaField('Additional Remarks', [validators.Optional()])


class UpdateReturnForm(Form):
    def validate_date(form, field):
        if field.data < datetime.date(datetime.now()):
            raise ValidationError('Return date cannot be in the past')

    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    orderid = StringField('Order ID', [validators.Length(min=1, max=150), validators.DataRequired()])
    returnreason = TextAreaField('Return Reason', [validators.DataRequired()])
    contact = IntegerField('Contact Number (+65)', [validators.number_range(min=10000000, max=99999999), validators.DataRequired()])
    address = TextAreaField('Address', [validators.length(max=200), validators.DataRequired()])
    returnoption = RadioField('Preferred return option', choices=[('P', 'Pickup'), ('D', 'Dropoff')])
    returndate = DateField('Preferred return date', format='%Y-%m-%d', validators=[validate_date])
    remarks = TextAreaField('Additional Remarks', [validators.Optional()])
    status = SelectField('Edit status', choices=[('', 'Select'), ('Filed', 'Filed'),('Contacted', 'Contacted'), ('Returned', 'Returned')], default='')

class CreateRegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    phoneno = IntegerField('Phone Number', [validators.InputRequired(), check_phone])
    gender = SelectField('Gender', [validators.DataRequired()],
                        choices=[('M', 'MALE'), ('F', 'FEMALE')], default='Select gender')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])

class CreateEventsForm(Form):
    def validate_date(form, field):
        if field.data < datetime.date(datetime.now()):
            raise ValidationError("Event date cannot be in the past.")

    title_name = StringField('Event Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    event_date = DateField('Event Date', format='%Y-%m-%d', validators=[validate_date])
    tagscategory = SelectField('Tag/Category', [validators.DataRequired()],
                               choices=[('D', 'DOUJIN'), ('A', 'ANIME'), ('M', 'MANGA'),  ('COS', 'COSPLAY'),
                                        ('CON', 'CONVENTION')], default='ANIME')
    event_desc = TextAreaField('Event Desc', [validators.Length(min=1, max=2000), validators.DataRequired()])
