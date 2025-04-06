#!/bin/python
from flask import Flask, request, render_template as tmplt
import phonenumbers
from phonenumbers import geocoder as geo, carrier as cari, timezone as tz
from phonenumbers.phonenumberutil import NumberParseException

web_app = Flask(__name__)

@web_app.route("/", methods=['POST', 'GET'])
def Finder():
    if request.method == "GET":
        phone_number = request.args.get("phoneNumber")

       
        if not phone_number or phone_number.strip() == "":
            return tmplt('finder.html')

        # <---------------[Error Handling]---------------->
        try:
            caller = phonenumbers.parse(phone_number, "US")  # Default country (change if needed)

            if not phonenumbers.is_valid_number(caller):
                raise ValueError("Invalid number")

        except NumberParseException:
            return "<script>alert('Invalid phone number format!'); window.location.href='/';</script>"

        except ValueError:
            return "<script>alert('Invalid phone number!'); window.location.href='/';</script>"

        except Exception as Er:
            return f"<script>alert('Unexpected error: {Er}'); window.location.href='/';</script>"

        #<---------[Feching Phone Number Details]---------------->
        geo_location = geo.description_for_number(caller, "en")
        carrier_name = cari.name_for_number(caller, "en")
        time_zone = tz.time_zones_for_number(caller)

        return tmplt("result.html", geoL=geo_location, cName=carrier_name, tzone=time_zone, pNumber=caller)

if __name__ == "__main__":
    web_app.run(debug=True)
