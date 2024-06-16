from flask import Flask, make_response, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Address, db, Food, User, Review, Location
from requests.auth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse
import requests
import base64
from datetime import datetime
from sqlalchemy import inspect
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USE_SSL'] = False  
# app.config['MAIL_USERNAME'] = 'nimz69509@gmail.com'
# app.config['MAIL_PASSWORD'] = 'zabc lnoq cbkv nupc'
# app.config['MAIL_DEFAULT_SENDER'] = 'nimz69509@gmail.com'
# app.json.compact = False

CORS(app)

migrate = Migrate(app, db)
db.init_app(app)

mail = Mail(app)


with app.app_context():
    # Check if the 'foods' table exists
    db.create_all()
    inspector = inspect(db.engine)
        # print all table names
    if 'foods' in inspector.get_table_names():
        print(inspector.get_table_names())
        

# #Mpesa
# consumer_key='7GSlEmZiocYKga9acUBDyIYiuJqOvZvHd6XGzbcVZadPm93f'
# consumer_secret='Vh2mvQS4GKyo6seUtpAApN1plTwMDTeqyGZNBEtESYH05sBfRMSddn5vnlJ4zifA'
# base_url='https://1115-105-161-25-71.ngrok-free.app'

#Dishes API
@app.route('/dishes', methods=['GET'])
def get_foods():
    foods = []
    for food in Food.query.all():
        response_body = {
            "id": food.id,
            "name": food.name,
            "image": food.image,
            "description": food.description,
            "price": food.price
        }
        foods.append(response_body)

    response = make_response(
        jsonify(foods),
        200
    )
    return response


#register users
@app.route('/user', methods=['POST'])
def register_user():
    data = request.get_json()

    required_fields = ['first_name', 'last_name', 'email', 'phone', 'password']
    if not all(field in data for field in required_fields):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return make_response(jsonify({"error": "User with this email already exists"}), 409)

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        password=data['password']
    )
    
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "phone": new_user.phone,
        "created_at": new_user.created_at,
    }

    return make_response(jsonify(response_body), 201)
    

# View all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    if users:
        users_list = []
        for user in users:
            user_data = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "created_at": user.created_at,
            }
            users_list.append(user_data)

        return make_response(jsonify(users_list), 200)
    else:
        return make_response(jsonify({"error": "No users found"}), 404)


#collect reviews
@app.route('/reviews', methods=['POST'])
def submit_review():
    data = request.get_json()

    required_fields = ['user_email', 'rating']
    if not all(field in data for field in required_fields):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    user = User.query.filter_by(email=data['user_email']).first()
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    new_review = Review(
        user_id=user.id,
        rating=data['rating'],
        feedback=data.get('feedback', None)
    )

    db.session.add(new_review)
    db.session.commit()

    response_body = {
        "id": new_review.id,
        "user_email": data['user_email'],
        "rating": new_review.rating,
        "feedback": new_review.feedback,
        "created_at": new_review.created_at,
    }

    return make_response(jsonify(response_body), 201)


# Collect address
@app.route('/address', methods=['POST'])
def add_address():
    data = request.get_json()

    required_fields = ['user_email', 'city', 'area', 'street', 'building', 'room']
    if not all(field in data for field in required_fields):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    user = User.query.filter_by(email=data['user_email']).first()
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    new_address = Address(
        user_id=user.id,
        city=data['city'],
        area=data['area'],
        street=data['street'],
        building=data['building'],
        room=data['room'],
        notes=data.get('notes', None)
    )

    db.session.add(new_address)
    db.session.commit()

    response_body = {
        "id": new_address.id,
        "user_email": data['user_email'],
        "city": new_address.city,
        "area": new_address.area,
        "street": new_address.street,
        "building": new_address.building,
        "room": new_address.room,
        "notes": new_address.notes,
    }

    return make_response(jsonify(response_body), 201)

# View addresses for a user
@app.route('/addresses/<user_email>', methods=['GET'])
def get_addresses_by_user(user_email):
    user = User.query.filter_by(email=user_email).first()

    if user:
        addresses = Address.query.filter_by(user_id=user.id).all()
        if addresses:
            addresses_list = []
            for address in addresses:
                address_data = {
                    "id": address.id,
                    "user_email": user_email,
                    "city": address.city,
                    "area": address.area,
                    "street": address.street,
                    "building": address.building,
                    "room": address.room,
                    "notes": address.notes,
                }
                addresses_list.append(address_data)

            return make_response(jsonify(addresses_list), 200)
        else:
            return make_response(jsonify({"error": "No addresses found for the user"}), 404)
    else:
        return make_response(jsonify({"error": "User not found"}), 404)



@app.route('/payment', methods=['POST', 'OPTIONS'])
def post():
    if request.method == 'OPTIONS':
        # Pre-flight request
        response = make_response('', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # The rest of your payment processing logic here
    parser = reqparse.RequestParser()
    parser.add_argument('phone', type=str, required=True)
    parser.add_argument('amount', type=str, required=True)
    args = parser.parse_args()

    phone_number = args['phone']
    amount = args['amount']

    consumer_key = "AAa4RjX5YgWolpQsX8b1E6MAZDHH1zRXpfXBWnjfGSWImQEU"
    consumer_secret = "pPAPZ4X3uvGyfeFpEoziaxR43lRih7PxnHV2FA62sCOgmWwKAnZ5S6sdIlhRwXlf"
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    data = r.json()
    access_token = "Bearer " + data['access_token']
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    bussiness_shortcode = '174379'
    data_to_encode = bussiness_shortcode + passkey + timestamp
    encoded_data = base64.b64encode(data_to_encode.encode())
    password = encoded_data.decode('utf-8')

    request_payload = {
        "BusinessShortCode": bussiness_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": f"254{phone_number[1:]}",
        "PartyB": bussiness_shortcode,
        "PhoneNumber": f"254{phone_number[1:]}",
        "CallBackURL": "https://mydomain.com/pat",
        "AccountReference": "Client",
        "TransactionDesc": "Client Paid"
    }

    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": access_token, "Content-Type": "application/json"}

    response = requests.post(stk_url, json=request_payload, headers=headers)

    if response.status_code > 299:
        mpesa_response = {'message': 'Failed'}
        final_response = make_response(jsonify(mpesa_response))
        return final_response
    else:
        message = {'message': 'Successful'}
        response = make_response(jsonify(message))

        # Assuming you have a 'Payment' model, you can add the payment data to the database here
        new_data = Payment(number=phone_number, amount=amount)
        db.session.add(new_data)
        db.session.commit()

        return response


@app.route('/send_confirmation', methods=['POST'])
def send_confirmation():
    print("Attempting network connection...")
    data = request.get_json()

    # data
    email = data.get('email')
    numberOfGuests = data.get('numberOfGuests')
    tableNumber = data.get('tableNumber')

    # email
    subject = 'Reservation Confirmation - Chai Vevinah'

    # image
    logo_filename = 'chai-vevinah-logo.png'
    logo_path = os.path.join(app.root_path, 'asset', logo_filename)
    logo_url = f'cid:{logo_filename}'  
    logo_data = base64.b64encode(open(logo_path, 'rb').read()).decode('utf-8')
    print(f'Logo Path: {logo_path}')


    # email body
    body = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #333;
                }}
                p {{
                    color: #555;
                }}
                .logo {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .footer {{
                    margin-top: 20px;
                    padding-top: 10px;
                    border-top: 1px solid #ddd;
                    text-align: center;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">
                    <img src="data:image/png;base64,{{ logo_data }}" alt="Chai Vevinah Logo" style="max-width: 100%; height: auto;">
                </div>
                <h1>Chai Vevinah Reservation Confirmation</h1>
                <p>Thank you for choosing Chai Vevinah. Your reservation details are confirmed:</p>
                <ul>
                    <li><strong>Number of Guests:</strong> {numberOfGuests}</li>
                    <li><strong>Table Number:</strong> {tableNumber}</li>
                </ul>
                <p>We look forward to serving you. If you have any questions or need further assistance, feel free to contact us.</p>
                <div class="footer">
                    <p>Chai Vevinah | Administration</p>
                </div>
            </div>
        </body>
    </html>
    """

    # Send
    try:
        msg = Message(subject, recipients=[email], html=body)
        msg.sender = 'lactorjm3@gmail.com'  # sender 
        mail.send(msg)
        return jsonify({'success': True, 'message': 'Email sent successfully'})
    except Exception as e:
        print(f'Error: {str(e)}')  
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})
        

@app.route('/locations', methods=['GET'])
def get_locations():
    locations = []
    for location in Location.query.all():
        response_body = {
            "id": location.id,
            "name": location.name,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "delivery_fee": location.delivery_fee
        }
        locations.append(response_body)
    response = make_response(
        jsonify(locations),
        200
    )
    return response


@app.route('/locations/<int:id>', methods=['GET'])
def get_location(id):
    location = Location.query.get(id)
    if location is None:
        return make_response(jsonify({"message": "Location not found"}), 404)
    response_body = {
        "id": location.id,
        "name": location.name,
        "latitude": location.latitude,
        "longitude": location.longitude
    }
    return make_response(jsonify(response_body), 200)


# Get distance from google maps API
@app.route('/distance', methods=['GET'])
def get_distance():
    origin = request.args.get('origins')
    destination = request.args.get('destinations')
    api_key = request.args.get('key')
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key={}".format(
        origin, destination, api_key)
    response = requests.get(url)
    print(response.json())
    return response.json()

    

if __name__ == '__main__':
    app.run(port=5000, debug=True)
