from flask import Flask, render_template, request, redirect, url_for, session, flash
from Forms import CreateCustomerForm, CreateStaffForm, LoginForm, UpdateCustomerForm, UpdateStaffForm,\
    ChangePasswordForm, CreateReturnForm, UpdateReturnForm, CreateRegisterForm, CreateEventsForm
from VoucherForms import CreateVoucherForm
from werkzeug.datastructures import CombinedMultiDict
import shelve, Customer, Staff, Voucher, Return, ReturnsLogin, Registrants, Event
from datetime import date,datetime

ANIPACTED = Flask(__name__)
ANIPACTED.secret_key = 'secret key'


@ANIPACTED.route('/')
def pr_home():
    return render_template('homePR.html')


@ANIPACTED.route('/homeCS')
def cs_home():
    return render_template('homeCS.html')


@ANIPACTED.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    customers_dict = {}
    staff_dict = {}
    db = shelve.open('customer.db', 'r')
    if 'Customers' in db:
        customers_dict = db['Customers']
        for key in customers_dict:
            customer = customers_dict.get(key)
            if customer.get_email() == login_form.username.data and customer.get_password() == login_form.password.data:
                session['customer_id'] = customer.get_customer_id()
                session['customer_name'] = customer.get_name()
                session['loginReturns'] = customer.get_name()
                db.close()
                return redirect(url_for('cs_home'))
    else:
        db.close()
        flash('No customer records found')
        return redirect(url_for('login'))

    db = shelve.open('Staff.db', 'r')
    if 'Staff' in db:
        staff_dict = db['Staff']
        for key in staff_dict:
            staff = staff_dict.get(key)
            if staff.get_email() == login_form.username.data and staff.get_password() == login_form.password.data:
                session['staff_id'] = staff.get_staff_id()
                session['staff_name'] = staff.get_name()
                db.close()
                return redirect(url_for('stf_home'))
    else:
        db.close()
        flash('No staff records found')
        return redirect(url_for('login'))
    return render_template('Login.html', form=login_form)


@ANIPACTED.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        try:
            db = shelve.open('customer.db', 'c')
            customers_dict = db.get('Customers', {})
            datecreated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            customer = Customer.Customer(create_customer_form.name.data, create_customer_form.gender.data,
                                         create_customer_form.birthday.data, create_customer_form.occupation.data,
                                         create_customer_form.phone_number.data, create_customer_form.email.data,
                                         create_customer_form.address.data, create_customer_form.password.data,
                                         create_customer_form.confirm_password.data, 'Active', datecreated)
            customers_dict[customer.get_customer_id()] = customer
            db['Customers'] = customers_dict
            print(customer.get_name(), "was stored in customer.db successfully with customer_id ==", customer.get_customer_id())
            session['customer_created'] = customer.get_name()
            return redirect(url_for('login'))
            db.close()

        except Exception as e:
            print("Error occurred while creating and storing customer:", e)
            flash("Error occurred while creating and storing customer")
            return redirect(url_for('create_customer'))
    return render_template('createCustomer.html', form=create_customer_form)


@ANIPACTED.route('/CustomersOverview')
def retrieve_customer():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('CustomersOverview.html', count=len(customers_list), customers_list=customers_list)


@ANIPACTED.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = UpdateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_name(update_customer_form.name.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_birthday(update_customer_form.birthday.data)
        customer.set_occupation(update_customer_form.occupation.data)
        customer.set_phone_number(update_customer_form.phone_number.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_address(update_customer_form.address.data)

        db['Customers'] = customers_dict
        db.close()

        session['customer_updated'] = customer.get_name()

        return redirect(url_for('retrieve_customer'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.name.data = customer.get_name()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.birthday.data = customer.get_birthday()
        update_customer_form.occupation.data = customer.get_occupation()
        update_customer_form.phone_number.data = customer.get_phone_number()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.address.data = customer.get_address()

        return render_template('updateCustomer.html', form=update_customer_form)


@ANIPACTED.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']
    customer = customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    session['customer_deleted'] = customer.get_name()

    return redirect(url_for('retrieve_customer'))




@ANIPACTED.route('/createStaff', methods=['GET', 'POST'])
def create_staff():
    create_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'c')

        try:
            staff_dict = db['Staff']
        except:
            print("Error in retrieving Staff from staff.db.")
        datecreated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff = Staff.Staff(create_staff_form.name.data,create_staff_form.gender.data, create_staff_form.phone_number.data,
                            create_staff_form.email.data, create_staff_form.departments.data,
                            create_staff_form.job_name.data, create_staff_form.address.data, create_staff_form.password.data,
                            create_staff_form.confirm_password.data, 'Active', datecreated)

        staff_dict[staff.get_staff_id()] = staff
        db['Staff'] = staff_dict
        print(staff.get_name(), "was stored in staff.db successfully with staff_id ==",staff.get_staff_id())

        db.close()

        session['staff_created'] = staff.get_name()

        return redirect(url_for('retrieve_staff'))
    return render_template('createStaff.html', form=create_staff_form)


@ANIPACTED.route('/StaffOverview')
def retrieve_staff():
    staff_dict = {}
    db = shelve.open('staff.db', 'r')
    staff_dict = db['Staff']
    db.close()

    staff_list = []
    for key in staff_dict:
        staff = staff_dict.get(key)
        staff_list.append(staff)

    return render_template('StaffOverview.html', count=len(staff_list), staff_list=staff_list)


@ANIPACTED.route('/updateStaff/<int:id>/', methods=['GET', 'POST'])
def update_staff(id):
    update_staff_form = UpdateStaffForm(request.form)
    if request.method == 'POST' and update_staff_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')
        staff_dict = db['Staff']

        staff = staff_dict.get(id)
        staff.set_name(update_staff_form.name.data)
        staff.set_gender(update_staff_form.gender.data)
        staff.set_phone_number(update_staff_form.phone_number.data)
        staff.set_email(update_staff_form.email.data)
        staff.set_departments(update_staff_form.departments.data)
        staff.set_job_name(update_staff_form.job_name.data)
        staff.set_address(update_staff_form.address.data)

        db['Staff'] = staff_dict
        db.close()

        session['staff_updated'] = staff.get_name()

        return redirect(url_for('retrieve_staff'))
    else:
        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()

        staff = staff_dict.get(id)
        update_staff_form.name.data = staff.get_name()
        update_staff_form.gender.data = staff.get_gender()
        update_staff_form.phone_number.data = staff.get_phone_number()
        update_staff_form.email.data = staff.get_email()
        update_staff_form.departments.data = staff.get_departments()
        update_staff_form.job_name.data = staff.get_job_name()
        update_staff_form.address.data = staff.get_address()

    return render_template('updateStaff.html', form=update_staff_form)


@ANIPACTED.route('/delete_staff/<int:id>', methods=['POST'])
def delete_staff(id):
    staff_dict = {}
    db = shelve.open('staff.db', 'w')
    staff_dict = db['Staff']
    staff = staff_dict.pop(id)

    db['Staff'] = staff_dict
    db.close()

    session['staff_deleted'] = staff.get_name()

    return redirect(url_for('retrieve_staff'))


@ANIPACTED.route('/EditProfileCS/<int:id>', methods=['GET', 'POST'])
def edit_cs_profile(id):
    edit_profile_form=UpdateCustomerForm(request.form)
    if request.method == 'POST' and edit_profile_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']
        customer = customers_dict.get(id)
        customer.set_name( edit_profile_form.name.data)
        customer.set_gender( edit_profile_form.gender.data)
        customer.set_birthday( edit_profile_form.birthday.data)
        customer.set_occupation( edit_profile_form.occupation.data)
        customer.set_phone_number( edit_profile_form.phone_number.data)
        customer.set_email( edit_profile_form.email.data)
        customer.set_address( edit_profile_form.address.data)


        db['Customers'] = customers_dict
        db.close()
        session['customer_updated']=customer.get_name()

        return redirect(url_for('cs_home'))


    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        edit_profile_form.name.data = customer.get_name()
        edit_profile_form.gender.data = customer.get_gender()
        edit_profile_form .birthday.data= customer.get_birthday()
        edit_profile_form .occupation.data = customer.get_occupation()
        edit_profile_form .phone_number.data = customer.get_phone_number()
        edit_profile_form .email.data = customer.get_email()
        edit_profile_form .address.data = customer.get_address()

    return render_template('EditProfileCS.html', form=edit_profile_form, customer=customer)


@ANIPACTED.route('/homeSTF')
def stf_home():
    return render_template('homeSTF.html')


@ANIPACTED.route('/EditProfileSTF/<int:id>', methods=['GET', 'POST'])
def edit_stf_profile(id):
    edit_stf_profile_form=UpdateStaffForm(request.form)
    if request.method == 'POST' and edit_stf_profile_form.validate():
        staff_dict = {}
        db = shelve.open('staff.db', 'w')
        staff_dict = db['Staff']
        staff = staff_dict.get(id)
        staff.set_name( edit_stf_profile_form.name.data)
        staff.set_gender( edit_stf_profile_form.gender.data)
        staff.set_phone_number( edit_stf_profile_form.phone_number.data)
        staff.set_email( edit_stf_profile_form.email.data)
        staff.set_departments( edit_stf_profile_form.departments.data)
        staff.set_job_name( edit_stf_profile_form.job_name.data)
        staff.set_address( edit_stf_profile_form.address.data)

        db['Staff'] = staff_dict
        db.close()
        session['staff_updated']=staff.get_name()

        return redirect(url_for('stf_home'))


    else:
        staff_dict = {}
        db = shelve.open('staff.db', 'r')
        staff_dict = db['Staff']
        db.close()

        staff = staff_dict.get(id)
        edit_stf_profile_form.name.data = staff.get_name()
        edit_stf_profile_form .gender.data = staff.get_gender()
        edit_stf_profile_form .email.data = staff.get_email()
        edit_stf_profile_form.phone_number.data = staff.get_phone_number()
        edit_stf_profile_form .departments.data= staff.get_departments()
        edit_stf_profile_form .job_name.data= staff.get_job_name()
        edit_stf_profile_form .address.data = staff.get_address()

    return render_template('EditProfileSTF.html', form=edit_stf_profile_form, staff=staff)

@ANIPACTED.route("/UpdatePwCS/<int:id>", methods=['GET', 'POST'])
def update_pw_cs(id):
    change_cpassword_form = ChangePasswordForm(request.form)
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customer = customers_dict.get(id)
    old_password = customer.get_password()

    if request.method == 'POST' and change_cpassword_form.validate():
        if change_cpassword_form.old_password.data != old_password:
            change_cpassword_form.old_password.errors.append("Old password is incorrect")
            return render_template('UpdatePwCS.html', form=change_cpassword_form, customer=customer)

        db = shelve.open('customer.db', 'w')
        customer.set_password(change_cpassword_form.password.data)
        customer.set_confirm_password(change_cpassword_form.confirm_password.data)
        customers_dict[id] = customer
        db['Customers'] = customers_dict
        db.close()

        session["password_reset_successful"] = customer.get_name()

        return redirect(url_for('cs_home'))

    change_cpassword_form.password.data = customer.get_password()
    change_cpassword_form.confirm_password.data = customer.get_confirm_password()

    return render_template('UpdatePwCS.html', form=change_cpassword_form, customer=customer)


@ANIPACTED.route("/UpdatePwSTF/<int:id>", methods=['GET', 'POST'])
def update_pw_stf(id):
    update_pw_stf_form = ChangePasswordForm(request.form)
    staff_dict = {}
    db = shelve.open('staff.db', 'r')
    staff_dict = db['Staff']
    db.close()

    staff = staff_dict.get(id)
    old_password = staff.get_password()

    if request.method == 'POST' and update_pw_stf_form.validate():
        if update_pw_stf_form.old_password.data != old_password:
           update_pw_stf_form.old_password.errors.append("Old password is incorrect")
           return render_template('UpdatePwSTF.html', form=update_pw_stf_form, staff=staff)

        db = shelve.open('staff.db', 'w')

        staff.set_password(update_pw_stf_form.password.data)
        staff.set_confirm_password(update_pw_stf_form.confirm_password.data)
        staff_dict[id] = staff
        db['Staff'] = staff_dict
        db.close()

        session["password_reset_successful"] = staff.get_name()

        return redirect(url_for('stf_home'))

    update_pw_stf_form.password.data = staff.get_password()
    update_pw_stf_form.confirm_password.data = staff.get_confirm_password()

    return render_template('UpdatePwSTF.html', form=update_pw_stf_form, staff=staff)

@ANIPACTED.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('pr_home'))


@ANIPACTED.errorhandler(404)
def page_not_found(e):
    return render_template('error404C.html'), 404


@ANIPACTED.errorhandler(404)
def page_not_found(e):
    return render_template('error404S.html'), 404

@ANIPACTED.route('/StaffStatus/<int:id>', methods=['POST'])
def StaffStatus(id):
    staff_dict = {}
    db = shelve.open('staff.db', 'w')
    staff_dict = db['Staff']
    staff=staff_dict.get(id)
    staff.set_status("non-active")
    db['Staff'] = staff_dict
    db.close()

    session['staff_disabled']= staff.get_name()

    return redirect(url_for('retrieve_staff'))



@ANIPACTED.route('/StaffStatusActive/<int:id>', methods=['POST'])
def StaffStatusActive(id):
    staff_dict = {}
    db = shelve.open('staff.db', 'w')
    staff_dict = db['Staff']
    staff=staff_dict.get(id)
    staff.set_status("Active")
    db['Staff'] = staff_dict
    db.close()

    session['staff_enabled']= staff.get_name()

    return redirect(url_for('retrieve_staff'))

@ANIPACTED.route('/CustomerStatusActivate/<int:id>', methods=['POST'])
def CustomerStatusActivate(id):
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']
        customer = customers_dict.get(id)
        customer.set_status('Active')
        db['Customers'] = customers_dict
        db.close()

        session['customer_enabled']= customer.get_name()

        return redirect(url_for('retrieve_customer'))

@ANIPACTED.route('/CustomerStatus/<int:id>', methods=['POST'])
def CustomerStatus(id):
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']
        customer = customers_dict.get(id)
        customer.set_status('non-active')
        db['Customers'] = customers_dict
        db.close()

        session['customer_disabled']= customer.get_name()

        return redirect(url_for('retrieve_customer'))


@ANIPACTED.route("/clearDb", methods=["POST", "GET"])
def clear_db():
    voucher_dict = {}
    db = shelve.open('save.db', 'w')
    voucher_dict = db['redeemed']

    used_dict = {}
    a = shelve.open("used.db", "c")
    used_dict = a["used"]

    used_dict.clear()
    voucher_dict.clear()

    db['redeemed'] = voucher_dict
    a["used"] =  used_dict

    db.close()
    a.close()

    return redirect(url_for('retrieve_vouchers'))


@ANIPACTED.route('/useVoucher/<vouid>', methods=['POST'])
def use_voucher(vouid):
    voucher_dict = {}
    db = shelve.open('save.db', 'w')
    voucher_dict = db['redeemed']

    names = [voucher_dict[vouid]]
    print(names)
    print(session["customer_name"])
    index = names.index(session["customer_name"])
    print(index)
    names.pop(index)
    print(names)
    voucher_dict[vouid] = names
    db["redeemed"] = voucher_dict
    db.close()

    vouchers = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)

    used_dict = {}
    a = shelve.open("used.db", "c")
    used_dict = a["used"]
    print(used_dict)
    if vouid in used_dict:
        list = [used_dict[vouid]]
        print(list)
        list.append(session["customer_name"])
        used_dict[vouid] = list
    else:
        used_dict.update({vouid: session["customer_name"]})
    print(used_dict)

    for k in used_dict:
        a[k] = used_dict[k]
    print(f"final used: {used_dict}")
    a["used"] = used_dict

    return redirect(url_for('retrieve_vouchers_account'))


@ANIPACTED.route('/redeemVoucher/<vouid>', methods=['GET', 'POST'])
def redeem_voucher(vouid):
        vouchers = {}
        db = shelve.open('voucher.db', 'r')
        vouchers_dict = db['Vouchers']
        db.close()

        vouchers_list = []
        for key in vouchers_dict:
            voucher = vouchers_dict.get(key)
            vouchers_list.append(voucher)

        redeemed_dict = {}
        a = shelve.open("save.db", "c")
        redeemed_dict = a["redeemed"]
        print(redeemed_dict)
        if vouid in redeemed_dict:
            list = [redeemed_dict[vouid]]
            print(list)
            list.append(session["customer_name"])
            redeemed_dict[vouid] = list
        else:
            redeemed_dict.update({vouid: session["customer_name"]})
        print(redeemed_dict)

        for k in redeemed_dict:
                a[k] = redeemed_dict[k]
        print(redeemed_dict)
        a["redeemed"] = redeemed_dict

        return redirect(url_for('retrieve_vouchers_customer'))


@ANIPACTED.route('/retrieveVouchersAccount', methods=["GET", "POST"])
def retrieve_vouchers_account():
    redvouch_dict = {}
    db = shelve.open('save.db', 'r')
    redvouch_dict = db['redeemed']
    db.close()

    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()


    redvouch_list = []
    for key in redvouch_dict:
        redvouch = redvouch_dict.get(key)
        if session["customer_name"] in redvouch:
            print("the user who registered is", session["customer_name"])
            redvouch_list.append(key)

    print(redvouch_list)
    vouchers_list2 = []
    for key in redvouch_list:
        key1 = int(key)
        voucher = vouchers_dict.get(key1)
        vouchers_list2.append(voucher)

    return render_template('retrieveVouchersCustomer.html', count=len(vouchers_list2), vouchers_list=vouchers_list2, vouchers_list2=vouchers_list2)


@ANIPACTED.route('/retrieveVouchersCustomer', methods=["GET", "POST"])
def retrieve_vouchers_customer():
    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    redvouch_dict = {}
    db = shelve.open('save.db', 'r')
    redvouch_dict = db['redeemed']
    db.close()

    used_dict = {}
    db = shelve.open('used.db', 'r')
    used_dict = db['used']
    db.close()

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)

    vouchers_list1 = []
    for i in vouchers_list:
        if i.get_status() == 'Active' and i.get_expiry() >= datetime.date(datetime.now()):
            vouchers_list1.append(i)

    redvouch_list = []
    for key in redvouch_dict:
        redvouch = redvouch_dict.get(key)
        if session["customer_name"] in redvouch:
            print("the user who registered is", session["customer_name"])
            redvouch_list.append(key)

    print(redvouch_list)
    vouchers_list2 = []
    for key in redvouch_list:
        key1 = int(key)
        voucher = vouchers_dict.get(key1)
        vouchers_list2.append(voucher)

    used_list = []
    for key in used_dict:
        usedvoucher = used_dict.get(key)
        if session["customer_name"] in usedvoucher:
            print("the user who registered is", session["customer_name"])
            used_list.append(key)

    print(used_list)
    vouchers_list3 = []
    for key in used_list:
        key1 = int(key)
        voucher = vouchers_dict.get(key1)
        vouchers_list3.append(voucher)

    return render_template('retrieveVouchersCustomer.html', count=len(vouchers_list1), vouchers_list=vouchers_list1, vouchers_list2=vouchers_list2, vouchers_list3=vouchers_list3)

@ANIPACTED.route('/createVoucher', methods=['GET', 'POST'])
def create_voucher():
    create_voucher_form = CreateVoucherForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and create_voucher_form.validate():
        vouchers_dict = {}
        db = shelve.open('voucher.db', 'c')

        try:
            vouchers_dict = db['Vouchers']
        except:
            print("Error in retrieving Vouchers from voucher.db.")

        today = date.today()
        voucher = Voucher.Voucher(create_voucher_form.picture.data, create_voucher_form.name.data, create_voucher_form.type.data, create_voucher_form.amount.data, create_voucher_form.min_spend.data, create_voucher_form.expiry.data, create_voucher_form.description.data, 'Active', today)
        vouchers_dict[voucher.get_voucher_id()] = voucher
        db['Vouchers'] = vouchers_dict

        db.close()

        session['voucher_created'] = voucher.get_name()
        return redirect(url_for('retrieve_vouchers'))
    return render_template('createVoucher.html', form=create_voucher_form)


@ANIPACTED.route('/retrieveVouchers')
def retrieve_vouchers():
    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)


    return render_template('retrieveVouchers.html', count=len(vouchers_list), vouchers_list=vouchers_list)


@ANIPACTED.route('/updateVoucher/<int:id>/', methods=['GET', 'POST'])
def update_voucher(id):
    update_voucher_form = CreateVoucherForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and update_voucher_form.validate():
        vouchers_dict = {}
        db = shelve.open('voucher.db', 'w')
        vouchers_dict = db['Vouchers']

        voucher = vouchers_dict.get(id)
        voucher.set_picture(update_voucher_form.picture.data)
        voucher.set_name(update_voucher_form.name.data)
        voucher.set_type(update_voucher_form.type.data)
        voucher.set_amount(update_voucher_form.amount.data)
        voucher.set_min_spend(update_voucher_form.min_spend.data)
        voucher.set_expiry(update_voucher_form.expiry.data)
        voucher.set_description(update_voucher_form.description.data)

        db['Vouchers'] = vouchers_dict
        db.close()

        session['voucher_updated'] = voucher.get_name()
        return redirect(url_for('retrieve_vouchers'))
    else:
        voucher_dict = {}
        db = shelve.open('voucher.db', 'r')
        vouchers_dict = db['Vouchers']
        db.close()

        voucher = vouchers_dict.get(id)
        update_voucher_form.picture.data = voucher.get_picture()
        update_voucher_form.name.data = voucher.get_name()
        update_voucher_form.type.data = voucher.get_type()
        update_voucher_form.amount.data = voucher.get_amount()
        update_voucher_form.min_spend.data = voucher.get_min_spend()
        update_voucher_form.expiry.data = voucher.get_expiry()
        update_voucher_form.description.data = voucher.get_description()


        return render_template('updateVoucher.html', form=update_voucher_form)


@ANIPACTED.route('/deleteVoucher/<int:id>', methods=['POST'])
def delete_voucher(id):
    vouchers_dict = {}
    db = shelve.open('voucher.db', 'w')
    vouchers_dict = db['Vouchers']

    voucher = vouchers_dict.pop(id)

    db['Vouchers'] = vouchers_dict
    db.close()

    session['voucher_deleted'] = voucher.get_name()
    return redirect(url_for('retrieve_vouchers'))


@ANIPACTED.route('/img/<fname>')
def legacy_images(fname):
    return ANIPACTED.redirect(ANIPACTED.url_for('static', filename='uploads/' + fname), code=301)

@ANIPACTED.route('/stretrieveReturns')
def retrieveSreturns():
    returns_dict = {}
    db = shelve.open('return.db', 'r')
    returns_dict = db['Returns']
    db.close()

    returns_list = []
    for key in returns_dict:
        returns = returns_dict.get(key)
        returns_list.append(returns)

    return render_template('stretrieveReturns.html', count=len(returns_list), returns_list=returns_list)

@ANIPACTED.route('/createReturn', methods=['GET', 'POST'])
def create_return():
    create_return_form = CreateReturnForm(request.form)
    if request.method == 'POST' and create_return_form.validate():
        returns_dict = {}
        db = shelve.open('return.db', 'c')

        try:
            returns_dict = db['Returns']
        except:
            print("Error in retrieving Returns from return.db.")

        returns = Return.Return(create_return_form.name.data, create_return_form.orderid.data,
                                     create_return_form.returnreason.data, create_return_form.contact.data,
                                     create_return_form.address.data, create_return_form.returnoption.data,
                                     create_return_form.returndate.data, create_return_form.remarks.data, 'Filed')
        returns_dict[returns.get_return_id()] = returns
        db['Returns'] = returns_dict

        db.close()

        session['return_created'] = returns.get_orderid()

        return redirect(url_for('retrieve_returns'))
    return render_template('createReturn.html', form=create_return_form)


@ANIPACTED.route('/retrieveReturns')
def retrieve_returns():
    returns_dict = {}
    db = shelve.open('return.db', 'r')
    returns_dict = db['Returns']
    db.close()

    returns_list = []
    for key in returns_dict:
        returns = returns_dict.get(key)
        if returns.get_name() == session['loginReturns']:
            returns_list.append(returns)

    return render_template('retrieveReturns.html', count=len(returns_list), returns_list=returns_list)

@ANIPACTED.route('/updateReturn/<int:id>/', methods=['GET', 'POST'])
def update_return(id):
    update_return_form = CreateReturnForm(request.form)
    if request.method == 'POST' and update_return_form.validate():
        returns_dict = {}
        db = shelve.open('return.db', 'w')
        returns_dict = db['Returns']

        returns = returns_dict.get(id)
        returns.set_name(update_return_form.name.data)
        returns.set_orderid(update_return_form.orderid.data)
        returns.set_returnreason(update_return_form.returnreason.data)
        returns.set_contact(update_return_form.contact.data)
        returns.set_address(update_return_form.address.data)
        returns.set_returnoption(update_return_form.returnoption.data)
        returns.set_returndate(update_return_form.returndate.data)
        returns.set_remarks(update_return_form.remarks.data)

        db['Returns'] = returns_dict
        db.close()

        session['return_updated'] =  returns.get_orderid()

        return redirect(url_for('retrieve_returns'))
    else:
        returns_dict = {}
        db = shelve.open('return.db', 'r')
        returns_dict = db['Returns']
        db.close()

        returns = returns_dict.get(id)
        update_return_form.name.data = returns.get_name()
        update_return_form.orderid.data = returns.get_orderid()
        update_return_form.returnreason.data = returns.get_returnreason()
        update_return_form.contact.data = returns.get_contact()
        update_return_form.address.data = returns.get_address()
        update_return_form.returnoption.data = returns.get_returnoption()
        update_return_form.returndate.data = returns.get_returndate()
        update_return_form.remarks.data = returns.get_remarks()

        return render_template('updateReturn.html', form=update_return_form)

@ANIPACTED.route('/stupdateReturn/<int:id>/', methods=['GET', 'POST'])
def stupdateReturn(id):
    update_return_form = UpdateReturnForm(request.form)
    if request.method == 'POST' and update_return_form.validate():
        returns_dict = {}
        db = shelve.open('return.db', 'w')
        returns_dict = db['Returns']

        returns = returns_dict.get(id)
        returns.set_name(update_return_form.name.data)
        returns.set_orderid(update_return_form.orderid.data)
        returns.set_returnreason(update_return_form.returnreason.data)
        returns.set_contact(update_return_form.contact.data)
        returns.set_address(update_return_form.address.data)
        returns.set_returnoption(update_return_form.returnoption.data)
        returns.set_returndate(update_return_form.returndate.data)
        returns.set_remarks(update_return_form.remarks.data)
        returns.set_status(update_return_form.status.data)

        db['Returns'] = returns_dict
        db.close()

        session['return_updated'] =  returns.get_orderid()

        return redirect(url_for('retrieveSreturns'))
    else:
        returns_dict = {}
        db = shelve.open('return.db', 'r')
        returns_dict = db['Returns']
        db.close()

        returns = returns_dict.get(id)
        update_return_form.name.data = returns.get_name()
        update_return_form.orderid.data = returns.get_orderid()
        update_return_form.returnreason.data = returns.get_returnreason()
        update_return_form.contact.data = returns.get_contact()
        update_return_form.address.data = returns.get_address()
        update_return_form.returnoption.data = returns.get_returnoption()
        update_return_form.returndate.data = returns.get_returndate()
        update_return_form.remarks.data = returns.get_remarks()
        update_return_form.status.data = returns.get_status()

        return render_template('stupdateReturn.html', form=update_return_form)

@ANIPACTED.route('/deleteReturn/<int:id>', methods=['POST'])
def delete_return(id):
    returns_dict = {}
    db = shelve.open('return.db', 'w')
    returns_dict = db['Returns']
    returns = returns_dict.pop(id)

    db['Returns'] = returns_dict
    db.close()

    session['return_deleted'] = returns.get_orderid()

    return redirect(url_for('retrieve_returns'))



@ANIPACTED.route('/CSretrieveEvents/<int:id>/')
def CSeventhistory(id):
    registrants_dict = {}
    db = shelve.open('registrant.db','r')
    registrants_dict = db['Registrants']
    registrants_id = registrants_dict[id]
    if registrants_id:
        return render_template('CS-eventhistory.html', registrant=registrants_id)
    else:
        return redirect('error404C.html')

@ANIPACTED.route('/CS-eventregister', methods=['GET', 'POST'])
def CSeventregister():
    CSregister_form = CreateRegisterForm(request.form)
    if request.method == 'POST' and CSregister_form.validate():
        registrants_dict = {}
        db = shelve.open('registrant.db', 'c')

        try:
            registrants_dict = db['Registrants']
        except:
            print("Error in retrieving Registrants from event.db.")

        today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        registrant = Registrants.Registrant(CSregister_form.name.data,
                            CSregister_form.phoneno.data,
                            CSregister_form.email.data,
                            CSregister_form.gender.data,
                            'Active', today)
        registrants_dict[registrant.get_count_id()] = registrant
        db['Registrants'] = registrants_dict

        db.close()

        session['registrant_created'] = registrant.get_name()
        return redirect(url_for('CSretrieve_events'))
    return render_template('CS-eventregister.html', form=CSregister_form)

@ANIPACTED.route('/STF-addevents', methods=['GET', 'POST'])
def create_event():
    create_event_form = CreateEventsForm(request.form)
    if request.method == 'POST' and create_event_form.validate():
        events_dict = {}
        db = shelve.open('event.db', 'c')

        try:
            events_dict = db['Events']
        except:
            print("Error in retrieving Events from event.db.")

        today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        event = Event.Event(create_event_form.title_name.data,
                            create_event_form.event_date.data,
                            create_event_form.tagscategory.data,
                            create_event_form.event_desc.data,
                            'Active', today)
        events_dict[event.get_event_id()] = event
        db['Events'] = events_dict

        db.close()

        session['event_created'] = event.get_title_name()
        return redirect(url_for('retrieve_events'))
    return render_template('STF-addevents.html', form=create_event_form)

@ANIPACTED.route('/STF-updateevents/<int:id>/', methods=['GET', 'POST'])
def update_event(id):
    update_event_form = CreateEventsForm(request.form)
    if request.method == 'POST' and update_event_form.validate():
        events_dict = {}
        db = shelve.open('event.db', 'w')
        events_dict = db['Events']

        event = events_dict.get(id)
        event.set_title_name(update_event_form.title_name.data)
        event.set_event_date(update_event_form.event_date.data)
        event.set_tagscategory(update_event_form.tagscategory.data)
        event.set_event_desc(update_event_form.event_desc.data)

        db['Events'] = events_dict
        db.close()

        session['event_updated'] = event.get_title_name()
        return redirect(url_for('retrieve_events'))
    else:
        events_dict = {}
        db = shelve.open('event.db', 'r')
        events_dict = db['Events']
        db.close()

        event = events_dict.get(id)
        update_event_form.title_name.data = event.get_title_name()
        update_event_form.event_date.data = event.get_event_date()
        update_event_form.tagscategory.data = event.get_tagscategory()
        update_event_form.event_desc.data = event.get_event_desc()

        return render_template('STF-updateevents.html', form=update_event_form)

@ANIPACTED.route('/STF-eventsoverview1')
def retrieve_events():
    events_dict = {}
    db = shelve.open('event.db', 'r')
    events_dict = db['Events']
    db.close()
    events_list = []

    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)

    return render_template('STF-eventsoverview1.html', count=len(events_list), events_list=events_list)

@ANIPACTED.route('/PRretrieveEvents')
def PRretrieve_events():
    events_dict = {}
    db = shelve.open('event.db', 'r')
    events_dict = db['Events']
    db.close()
    events_list = []

    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)

    return render_template('PR-eventspage.html', count=len(events_list), events_list=events_list)

@ANIPACTED.route('/CSretrieveEvents')
def CSretrieve_events():
    events_dict = {}
    db = shelve.open('event.db', 'r')
    events_dict = db['Events']
    db.close()
    events_list = []

    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)

    return render_template('CS-eventspage.html', count=len(events_list), events_list=events_list)


@ANIPACTED.route('/deleteEvent/<int:id>', methods=['POST'])
def delete_events(id):
    events_dict = {}
    db = shelve.open('event.db', 'w')
    events_dict = db['Events']

    event = events_dict.pop(id)

    db['Events'] = events_dict
    db.close()

    session['event_deleted'] = event.get_title_name()
    return redirect(url_for('retrieve_events'))

if __name__ == '__main__':
    ANIPACTED.run(debug=True)
