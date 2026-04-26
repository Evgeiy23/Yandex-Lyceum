import requests
from flask import Flask, render_template, abort
from data import db_session
from data import users_api

from api import API_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mars_explorer_secret_key'
app.register_blueprint(users_api.blueprint)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    api_request = f'http://localhost:5000/api/users/{user_id}'
    api_response = requests.get(api_request)

    if not api_response or api_response.status_code != 200:
        abort(404)

    data = api_response.json()
    user_data = data['user']
    city = user_data['city_from']

    geocoder_url = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": city,
        "format": "json"
    }

    geo_response = requests.get(geocoder_url, params=geocoder_params).json()
    geo_object = geo_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    coordinates = geo_object['Point']['pos'].replace(' ', ',')

    static_map_url = f"https://static-maps.yandex.ru/1.x/?ll={coordinates}&spn=0.1,0.1&l=sat"

    return render_template(
        'user_show.html',
        title='Hometown',
        user=user_data,
        map_url=static_map_url
    )


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()