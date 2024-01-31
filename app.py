# app.py

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Sample data for zip codes
zip_code_data = {
    "12345": {"city": "City A", "province": "Province X", "region": "Region I"},
    "67890": {"city": "City B", "province": "Province Y", "region": "Region II"},
    # Add more zip codes and corresponding cities, provinces, and regions as needed
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_zip_code():
    search_term = request.form.get('search_term')
    results = find_zip_code(search_term)
    return render_template('index.html', results=results, search_term=search_term)


def find_zip_code(search_term):
    results = []
    search_term_lower = search_term.lower()

    for zip_code, info in zip_code_data.items():
        if (
            search_term_lower in info['city'].lower() or
            search_term_lower in info['province'].lower() or
            search_term_lower in info['region'].lower()
        ):
            results.append(
                {'zip_code': zip_code, 'city': info['city'], 'province': info['province'], 'region': info['region']})

    if results:
        return results
    else:
        return [{'error': 'No matching results'}]


if __name__ == '__main__':
    app.run(debug=True)
