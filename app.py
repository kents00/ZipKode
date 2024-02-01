from flask import Flask, render_template, request
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)

def read_data_from_file(file_path):
    """
    The function reads data from a file and organizes it into a nested dictionary structure.

    :param file_path: The file path is the location of the file that you want to read the data from. It
    should be a string that specifies the path to the file, including the file name and extension. For
    example, "data.txt" or "C:/Users/username/data.txt"
    :return: a nested dictionary containing the data read from the file. The structure of the dictionary
    is as follows:
    """
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
    """
    The `search_data` function takes a user input and a data dictionary, and returns a dictionary of
    matching regions, provinces, cities, and zip codes based on exact or partial matches.

    :param user_input: The user_input parameter is the input provided by the user, which can be a
    region, province, zip code, or city/municipality
    :param data: The `data` parameter is a dictionary that contains information about regions,
    provinces, cities, and zip codes. The structure of the `data` dictionary is as follows:
    :return: The function `search_data` returns a dictionary `result` containing the search results. The
    structure of the dictionary is as follows:
    """
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
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_zip_code():
    user_input = request.form.get('search_zip')
    if not user_input:
        abort(400, "Please provide a valid search input.")

    result = search_data(user_input, data)
    return render_template('index.html', result=result, search_zip=user_input)

class ZipCodeSearch(Resource):
    def get(self):
        try:
            user_input = request.args.get('search_zip', '')
            if not user_input:
                abort(400, "Please provide a valid search input.")

            result = search_data(user_input, data)
            return {'result': result, 'search_zip': user_input}
        except Exception as e:
            logging.error(f"Error processing search request: {str(e)}")
            return {'error': 'Internal Server Error'}, 500

api.add_resource(ZipCodeSearch, '/search')

if __name__ == '__main__':
    app.run(debug=True)
