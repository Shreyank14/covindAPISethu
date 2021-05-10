import requests
import json
from datetime import date

today = date.today()

URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="

#districtID = 269
dateNeeded = today.strftime("%d-%m-%Y")


class vaccine_center(dict):
    def __init__(self, name, address, block_name, fee_type, available_capacity, vaccine, date, age):
        self.name = name
        self.address = address
        self.block_name = block_name
        self.fee_type = fee_type
        self.available_capacity = available_capacity
        self.vaccine = vaccine
        self.date = date
        self.age = age
        # self.slots = slots

    def asdict(self):
        return {'name': self.name, 'address': self.address, 'block_name': self.block_name, 'fee_type': self.fee_type, 'available_capacity': self.available_capacity, 'vaccine': self.vaccine, 'date': self.date, 'age': self.age}

    def __getattr__(self, attr):
        return self[attr]


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        print("APIError: status={}".format(self.status))
        return None

# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36


class cowinAPI:
    def call_api(self, age, district_id):
        url = URL+str(district_id)+'&date='+str(dateNeeded)
        header = {'accept': 'application/json',
                  'Content-Type': 'application/json',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                  'From': 'shreyankshetty007@gmail.com'}
        filtered_centers = {'centers': []}
        print(url)
        resp = requests.get(url, headers=header)
        if resp.status_code != 200:
            # This means something went wrong.
            print(resp.text)
            raise APIError(resp.status_code)

        else:
            available_centers = json.loads(resp.text)
            for center in available_centers['centers']:
                for slot in center['sessions']:
                    if (slot['available_capacity'] > 0) & (slot['min_age_limit'] == age):
                        filtered_center = vaccine_center(
                            center['name'], center['address'], center['block_name'], center['fee_type'], slot['available_capacity'], slot['vaccine'], slot['date'], slot['min_age_limit'])
                        filtered_centers['centers'].append(
                            filtered_center.asdict())
            return filtered_centers


#api = cowinAPI()
# print(api.call_api())
