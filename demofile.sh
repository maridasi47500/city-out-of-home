
mkdir templates 
python3 scaffold.py ad_trip city_id:references country_id:references pic:file departure_country_id departure_city_id price
python3 scaffold.py user username email country_id:references phone password
python3 scaffold.py city name
python3 scaffold.py country name
python3 scaffold.py ad_trip_booking user_id:references ad_trid_id:references
python3 scaffold.py company digitalidentity name description pic:file
python3 scaffold.py userknowcompany user_id:references company_digitalidentity_id:references
