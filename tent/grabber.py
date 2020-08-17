import json
import requests

from grabber.config import NPS_GOV_JSON_WHITELIST_FIELDS
from grabber.secret import API_KEY


def filter_json(json_object: dict, whitelist: list = [], blacklist: list = []):
    """Filter a JSON object by applying a top-level key whitelist or blacklist

    :param json_object: A JSON object in dictionary form
    :param whitelist: A list of keys to use as a whitelist for JSON filtering
    :param blacklist: A list of keys to use as a blacklist for JSON filtering
    :return: A filtered JSON object
    """
    filtered_object = {}
    for key, val in json_object.items():
        if key in whitelist and key not in blacklist:
            filtered_object[key] = json_object[key]
    return filtered_object


def access_api(limit: int = 50, start: int = 0):
    """Retrieve a JSON object from the nps.gov public API. Perform basic filtering on the JSON object.

    :param limit: The number of API entries to request
    :param start: The campground 'index' to start at when making an API request
    :return: A JSON object containing campground data
    """
    api_url = f'https://developer.nps.gov/api/v1/campgrounds?limit={limit}&start={start}&api_key={API_KEY}'
    response = requests.get(url=api_url)
    response_data = response.json().get('data')
    filtered_response_data = []
    if not response_data:
        return []
    for response in response_data:
        filtered_response_data.append(filter_json(json_object=response,
                                                  whitelist=NPS_GOV_JSON_WHITELIST_FIELDS))
    return filtered_response_data


def convert_to_db_record(data: list):
    """Convert a JSON object from the nps.gov public API to a record ready for database entry

    :param data: A JSON object from the nps.gov public API
    :return: A record ready for database entry
    """
    entries = []
    for data in data:
        entry = {}
        # Fetch name
        name = data.get('name')
        entry['name'] = name

        # Fetch address
        physical_address = None
        for address in data.get('addresses'):
            if address.get('type') == 'Physical':
                physical_address = address
        if not physical_address:
            physical_address = data.get('addresses')
            if physical_address:
                physical_address = physical_address[0]
        if physical_address:
            street_address = physical_address.get('line1')
            city = physical_address.get('city')
            state_code = physical_address.get('stateCode')
            postal_code = physical_address.get('postalCode')
            physical_address = f'{street_address}, {city}, {state_code} {postal_code}'
        entry['address'] = physical_address

        phone_number = None
        contacts = data.get('contacts')
        if contacts:
            numbers = contacts.get('phoneNumbers')
            if numbers:
                phone_number = numbers[0].get('phoneNumber')
        if phone_number:
            phone_number = int(phone_number)
        entry['phone_number'] = phone_number

        longitude = data.get('longitude')
        latitude = data.get('latitude')
        if longitude:
            longitude = float(longitude)
        if latitude:
            latitude = float(latitude)
        entry['longitude'] = longitude
        entry['latitude'] = latitude

        amenities = data.get('amenities')
        amenities = json.dumps(amenities)
        entry['amenities'] = amenities

        images = []
        for ii in data.get('images'):
            images.append({'title': ii.get('title'), 'url': ii.get('url')})
        images = json.dumps(images)
        entry['images'] = images

        entries.append(entry)
    return entries


def main():
    access_api(limit=25)


if __name__ == '__main__':
    main()
