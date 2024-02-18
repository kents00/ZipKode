from flask import Flask, render_template, request, jsonify, abort
from flask_restful import Resource, Api
import sqlite3
import os

app = Flask(__name__)
api = Api(app)

DATABASE_FILENAME = 'data.db'
DATABASE_PATH = os.path.join('data', DATABASE_FILENAME)

def fetch_data_from_db():
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM postal_data")
        return c.fetchall()


def search_data(user_input):
    result = {}
    query = "SELECT * FROM postal_data WHERE region LIKE ? OR province LIKE ? OR city LIKE ? OR zip_code LIKE ?"
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(query, (f'%{user_input}%', f'%{user_input}%',
                  f'%{user_input}%', f'%{user_input}%'))
        rows = c.fetchall()

        for row in rows:
            region, province, city, zip_code = row['region'], row['province'], row['city'], row['zip_code']
            result.setdefault(region, {}).setdefault(
                province, {})[city] = zip_code

    return result

@app.route('/')
def index():
    all_data = fetch_data_from_db()
    return render_template('index.html', result=all_data, search_term=None)


@app.route("/robots.txt")
def robots_dot_txt():
    return "User-agent: *\nAllow: /"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/search', methods=['POST'])
def search_zip_code():
    user_input = request.form.get('search_term')
    result = search_data(user_input)
    return render_template('index.html', result=result, search_term=user_input)


class APIResource(Resource):
    def get(self):
        user_input = request.args.get('search_term')

        if not user_input:
            abort(400, description="Missing 'search_term' parameter in the request.")

        result = search_data(user_input)
        return jsonify({'result': result, 'search_term': user_input})


api.add_resource(APIResource, '/search')

if __name__ == '__main__':
    app.run(debug=True)
