from flask import Flask, render_template, request, jsonify, abort
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)


def read_data_from_file(file_path):
    data = {}

    with open(file_path, 'r') as file:
        for line in file:
            region, province, city, zip_code = line.strip().split('\t')

            if region not in data:
                data[region] = {}
            if province not in data[region]:
                data[region][province] = {}
            data[region][province][city] = zip_code

    return data


def search_data(user_input, data):
    result = {}

    # Exact match for region
    exact_region_match = None
    for region, provinces in data.items():
        if user_input.lower() == region.lower():
            exact_region_match = region
            result[region] = {}
            for province, cities in provinces.items():
                result[region][province] = cities
            break  # Stop searching after an exact match

    # Exact match for province
    exact_province_match = None
    if not exact_region_match:  # Skip if an exact region match is already found
        for region, provinces in data.items():
            for province in provinces:
                if user_input.lower() == province.lower():
                    exact_province_match = province
                    result[region] = {province: provinces[province]}
                    break  # Stop searching after an exact match
            if exact_province_match:
                break  # Stop searching after an exact match

    # Partial match for region or province
    if not exact_region_match and not exact_province_match:  # Skip if an exact match is already found
        for region, provinces in data.items():
            if user_input.lower() in region.lower() or user_input.lower() in [province.lower() for province in provinces]:
                result[region] = {}
                for province, cities in provinces.items():
                    result[region][province] = cities

    # Exact match for zip code or city/municipality
    for region, provinces in data.items():
        for province, cities in provinces.items():
            for city, zip_code in cities.items():
                if user_input.lower() == zip_code or user_input.lower() == city.lower():
                    if region not in result:
                        result[region] = {}
                    if province not in result[region]:
                        result[region][province] = {}
                    result[region][province][city] = zip_code
                    return result  # Stop searching after an exact match

    # If no exact matches found, perform partial matching for zip code or city/municipality
    for region, provinces in data.items():
        for province, cities in provinces.items():
            for city, zip_code in cities.items():
                if user_input.lower() in zip_code or user_input.lower() in city.lower():
                    if region not in result:
                        result[region] = {}
                    if province not in result[region]:
                        result[region][province] = {}
                    result[region][province][city] = zip_code

    return result


file_path = os.path.join('data/postal_regions.txt')
data = read_data_from_file(file_path)


@app.route('/')
def index():
    all_data = data
    return render_template('index.html', result=all_data, search_term=None)


@app.route('/search', methods=['POST'])
def search_zip_code():
    user_input = request.form.get('search_term')
    result = search_data(user_input, data)
    return render_template('index.html', result=result, search_term=user_input)


class APIResource(Resource):
    def get(self):
        user_input = request.args.get('search_term')

        if not user_input:
            abort(400, description="Missing 'search_term' parameter in the request.")

        result = search_data(user_input, data)
        return jsonify({'result': result, 'search_term': user_input})


api.add_resource(APIResource, '/search')

if __name__ == '__main__':
    app.run(debug=True)
