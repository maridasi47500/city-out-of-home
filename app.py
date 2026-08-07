from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_ad_trip", methods=["GET","POST"])
def add_one_ad_trip():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        touslescity= query_db("select * from city")

        touslescountry= query_db("select * from country")

        one_user = query_db("insert into ad_trip (city_id,country_id,pic,departure_country_id,departure_city_id,price) values (:city_id,:country_id,:pic,:departure_country_id,:departure_city_id,:price)",hey)
        user = query_db('select * from ad_trip')

        return render_template("ad_tripform.html", ad_trips=user, one_user=one_user, the_title="add new ad_trip", touslescity=touslescity, touslescountry=touslescountry)


    touslescity= query_db("select * from city")

    touslescountry= query_db("select * from country")

    user = query_db('select * from ad_trip')
    one_user = query_db("select * from ad_trip limit 1", one=True)
    return render_template("ad_tripform.html", ad_trips=user, one_user=one_user, the_title="add new ad_trip", touslescity=touslescity, touslescountry=touslescountry)

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,email,country_id,phone,password) values (:username,:email,:country_id,:phone,:password)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','email','country_id','phone','password']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','email','country_id','phone','password']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','email','country_id','phone','password']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_city", methods=["GET","POST"])
def add_one_city():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into city (name) values (:name)",hey)
        user = query_db('select * from city')

        return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city")


    user = query_db('select * from city')
    one_user = query_db("select * from city limit 1", one=True)
    return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city")

@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_ad_trip_booking", methods=["GET","POST"])
def add_one_ad_trip_booking():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        touslesad_trid= query_db("select * from ad_trid")

        one_user = query_db("insert into ad_trip_booking (user_id,ad_trid_id) values (:user_id,:ad_trid_id)",hey)
        user = query_db('select * from ad_trip_booking')

        return render_template("ad_trip_bookingform.html", ad_trip_bookings=user, one_user=one_user, the_title="add new ad_trip_booking", touslesuser=touslesuser, touslesad_trid=touslesad_trid)


    touslesuser= query_db("select * from user")

    touslesad_trid= query_db("select * from ad_trid")

    user = query_db('select * from ad_trip_booking')
    one_user = query_db("select * from ad_trip_booking limit 1", one=True)
    return render_template("ad_trip_bookingform.html", ad_trip_bookings=user, one_user=one_user, the_title="add new ad_trip_booking", touslesuser=touslesuser, touslesad_trid=touslesad_trid)

@app.route("/add_one_company", methods=["GET","POST"])
def add_one_company():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        one_user = query_db("insert into company (digitalidentity,name,description,pic) values (:digitalidentity,:name,:description,:pic)",hey)
        user = query_db('select * from company')

        return render_template("companyform.html", companys=user, one_user=one_user, the_title="add new company")


    user = query_db('select * from company')
    one_user = query_db("select * from company limit 1", one=True)
    return render_template("companyform.html", companys=user, one_user=one_user, the_title="add new company")

@app.route("/add_one_userknowcompany", methods=["GET","POST"])
def add_one_userknowcompany():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        touslescompany_digitalidentity= query_db("select * from company_digitalidentity")

        one_user = query_db("insert into userknowcompany (user_id,company_digitalidentity_id) values (:user_id,:company_digitalidentity_id)",hey)
        user = query_db('select * from userknowcompany')

        return render_template("userknowcompanyform.html", userknowcompanys=user, one_user=one_user, the_title="add new userknowcompany", touslesuser=touslesuser, touslescompany_digitalidentity=touslescompany_digitalidentity)


    touslesuser= query_db("select * from user")

    touslescompany_digitalidentity= query_db("select * from company_digitalidentity")

    user = query_db('select * from userknowcompany')
    one_user = query_db("select * from userknowcompany limit 1", one=True)
    return render_template("userknowcompanyform.html", userknowcompanys=user, one_user=one_user, the_title="add new userknowcompany", touslesuser=touslesuser, touslescompany_digitalidentity=touslescompany_digitalidentity)

