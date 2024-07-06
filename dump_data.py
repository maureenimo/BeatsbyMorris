from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///instance/app.db')


def dump_locations():
    locations = [
        # Json List of option locations
        {"name": "A.S.K. Showground/Wanye",
         "latitude": -1.3069613908896498, "longitude": 36.76321887833723, "delivery_fee": 250},
        {"name": "Adams Arcade / Dagoretti Corner",
            "latitude": -1.2982852031464247, "longitude": 36.76240902177483, "delivery_fee": 270},
        {"name": "Bahati / Marish / Viwandani / Jeri",
            "latitude": -1.2885200308543792, "longitude": 36.86783099127937, "delivery_fee": 250},
        {"name": "Bomas/CUEA/Galleria",
         "latitude": -1.343203802850624, "longitude": 36.766004256891186, "delivery_fee": 300},
        {"name": "Buruburu / Hamza / Harambee",
            "latitude": -1.2792463969985197, "longitude": 36.87854685246232, "delivery_fee": 300},
        {"name": "CBD - /City Market/Nation Centre",
            "latitude": -1.2830720951853314, "longitude": 36.82247814857535, "delivery_fee": 200},
        {"name": "CBD - KICC/Parliament/Kencom",
            "latitude": -1.2889431285257336, "longitude": 36.820907337118484, "delivery_fee": 200},
        {"name": "CBD - Luthuli/Afya Centre/ R. Ngala",
            "latitude": -1.285196837991742, "longitude": 36.82874869322758, "delivery_fee": 220},
        {"name": "CBD - UON/Globe/Koja/River Road",
            "latitude": -1.2787685475917847, "longitude": 36.820458868384954, "delivery_fee": 220},
        {"name": "City Stadium/Makongeni/Mbotela",
            "latitude": -1.2943843148614944, "longitude": 36.85087622637833, "delivery_fee": 210},
        {"name": "Dagoretti South - Ngand'o/Riruta",
            "latitude": -1.294703118968996, "longitude": 36.74279827879842, "delivery_fee": 370},
        {"name": "Donholm/Greenfields/Kayole/Nasra",
            "latitude": -1.2932502376671238, "longitude": 36.89593656780591, "delivery_fee": 340},
        {"name": "Embakasi - Fedha",
         "latitude": -1.3181083919918704, "longitude": 36.89665806403926, "delivery_fee": 320},
        {"name": "Embakasi East - Utawala/mihango/GSU",
            "latitude": -1.2828439944459837, "longitude": 36.959813577926155, "delivery_fee": 400},
        {"name": "Embakasi East-Pipeline/Transami/Airport North Rd",
            "latitude": -1.3249749793269512, "longitude": 36.89729232362643, "delivery_fee": 380},
    ]

    with engine.connect() as connection:
        trans = connection.begin()  # Begin a transaction
        try:
            # Clear locations table
            query = text("""
            DELETE FROM locations;
            """)
            connection.execute(query)
            # Insert locations
            for location in locations:
                query = text("""
                INSERT INTO locations (name, latitude, longitude, delivery_fee)
                VALUES (:name, :latitude, :longitude, :delivery_fee);
                """)
                connection.execute(query, {
                                   'name': location["name"], 'latitude': location["latitude"], 'longitude': location["longitude"], 'delivery_fee': location["delivery_fee"]})
            trans.commit()  # Commit the transaction
        except:
            trans.rollback()  # Rollback the transaction in case of error
            raise


if __name__ == "__main__":
    dump_locations()
