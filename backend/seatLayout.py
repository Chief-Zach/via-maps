import json

import requests

def get_car_data(train_number: str, date: str):
   #train_number = "52"
   with open("routes.json") as file:
      route_data = json.load(file)

   response = requests.post('https://api.reservia.viarail.ca/auth/token', json={"grant_type":"https://com.sqills.s3.oauth.public","code":"B2C_WEB_BOOKING"})

   token = response.json()["access_token"]

   headers = {"Authorization": f"Bearer {token}"}

   params = {
      "from_station":route_data[train_number]["origin"],
      "to_station":route_data[train_number]["destination"],
      #"date":"2024-12-28",
      "date": date,
      "service_name":f"VIA{train_number}",
      "booking":{
         "currency":"CAD",
         "passengers":[
            {
               "id":"passenger_1",
               "uuid":"0a88a02e-1509-3a0d-817c-186221848fbe",
               "ref_id":20557677,
               "type":"ADT",
               "disability_type":"ND",
               "discount_cards":[

               ],
               "first_name":"Sam",
               "last_name":"Crawford",
               "email":"samcrawford1995@gmail.com",
               "country_of_residence":"CA",
               "protect_privacy":True,
               "travel_documents":[

               ],
               "passengerTypeDetails":{
                  "code":"ADT",
                  "sequence_number":1,
                  "age_from":18,
                  "age_to":65,
                  "description":"Adult"
               },
               "passengerSsrProducts":[

               ],
               "isDummyPassenger":False,
               "isAdded":True,
               "firstTimeTraveller":False,
               "canChangeName":True,
               "canHavePet":True,
               "isRemoved":False,
               "isTravelPassGuest":False,
               "fullName":"Sam Crawford"
            }
         ]
      },
      "segment":{
         "id":"segment_1",
         "destination_station":"TRTO",
         "origin_station":"WDON",
         "service_name":"VIA79",
         "start_validity_date":"2024-12-28",
         "start_validity_time":"00:00:00",
         "direction":"outward"
      },
      "comfort_zones":[
         "ESC"
      ],
      "product_code":"ESC"
   }

   response = requests.post("https://api.reservia.viarail.ca/inventory/carriage-layout", headers=headers, json=params)

   data = response.json()
   # print(data["carriageLayout"])
   cars = []
   for car in range(len(data["carriageLayout"]["carriages"])):
       cars.append({"number": data["carriageLayout"]["carriages"][car]["carriage_number"], "type": data["carriageLayout"]["carriages"][car]["carriage_code"], "class": "Business" if "BUS" in data["carriageLayout"]["carriages"][car]["carriage_type"] else "Economy", "is_new": data["carriageLayout"]["carriages"][car]["carriage_code"] == "VEN"})
       print(f'Car {data["carriageLayout"]["carriages"][car]["carriage_number"]} - {data["carriageLayout"]["carriages"][car]["carriage_code"]} ({"Business" if "BUS" in data["carriageLayout"]["carriages"][car]["carriage_type"] else "Economy"}) New Train: {data["carriageLayout"]["carriages"][car]["carriage_code"] == "VEN"}')

   return {"cars": cars, "origin": route_data[train_number]["origin"], "destination": route_data[train_number]["destination"]}
