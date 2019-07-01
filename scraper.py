import googlemaps
import os
import time
import csv
import const

from app import utils


file_path = os.path.dirname(os.path.abspath("__file__"))
google_map_api_key = os.getenv("GOOGlE_API_KEY")
google_map_client = googlemaps.Client(key=google_map_api_key)


class GenerateCSV:

    def __init__(self, place_details):
        self.places = place_details

    def write_to_csv(self):
        # csv_file_name = f"data_out_{utils.generate_timestamp_file_name()}.csv"
        with open(utils.create_tmp_file(), mode='a', newline="", encoding='utf-8') as data_out:
            field_name = const.DATA_OUT_FIELDNAME + const.OPENING_DAYS
            csv_writer = csv.DictWriter(data_out, fieldnames=field_name)
            csv_writer.writeheader()
            if self.places is None:
                return None
            else:
                for place in self.places:
                    csv_writer.writerow({
                        field_name[0]: place.get('name'),
                        field_name[1]: place.get('formatted_address'),
                        field_name[3]: place.get('geometry')['location']['lat'],
                        field_name[4]: place.get('geometry')['location']['lng'],
                        field_name[5]: place.get('rating'),
                        field_name[6]: place.get('formatted_phone_number'),
                    })
            return data_out.name


class NearBySearch:

    def __init__(self, *args):
        self.lat_lng_list = args[0]
        self.radius = args[1]
        self.business_type = args[2]
        self.token = ""

        if self.radius == "":
            self.radius = const.RADIUS
        self.result = []
        self.place_details = []

    def find_nearby_place(self, location):
        find_place = google_map_client.places_nearby(location, self.radius, type=self.business_type, page_token=self.token)

        if find_place.get('next_page_token'):
            self.token = find_place['next_page_token']
            r = find_place['results']
            for i in r:
                self.result.append(i)
            time.sleep(5)
            return self.find_nearby_place(location)
        else:
            r = find_place['results']
            for i in r:
                self.result.append(i)
            return self.result

    def find_place_details(self):
        places_id = [place_id['place_id'] for place_id in self.result]
        for place_id in places_id:
            place_detail = google_map_client.place(place_id)
            self.place_details.append(place_detail['result'])
        self.result = []

    def start_scrapping(self):
        if google_map_api_key is None:
            return None
        for lat_lng in self.lat_lng_list:
            self.find_nearby_place(lat_lng)
        self.find_place_details()
        csv_writer = GenerateCSV(self.place_details).write_to_csv()
        self.place_details = []
        return csv_writer
