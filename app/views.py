from flask import request, render_template, jsonify, send_file, session
import os
from app import app
from scraper import NearBySearch
from const import BUSINESS_TYPE

app.config.from_object('config')
app.secret_key = os.getenv("GOOGLE_SCRAPER_SECRET")
google_map_key = os.getenv("GOOGlE_API_KEY")


@app.route('/')
def start():
    business_list = [bus.replace("_", " ").title() for bus in BUSINESS_TYPE]
    return render_template('index.html', api_key=google_map_key, business_type=business_list)


@app.route('/api/latlng', methods=['POST'])
def files():
    if request.method == 'POST':
        get_data = request.get_json('data')
        lat_lng = get_data['data']
        radius = get_data['radius']
        business_type = get_data['business_type']
        business_type = business_type.replace(" ", "_").lower()

        if not get_data['data']:
            return jsonify("Data Empty")
        else:
            near_by_data = NearBySearch(lat_lng, radius, business_type)
            scrap_data = near_by_data.start_scrapping()
            get_file_path = os.path.join(os.getcwd(), scrap_data)
            session["download_file"] = get_file_path
            return jsonify("Success")


@app.route('/download', methods=['GET'])
def download_file():
    get_download_file = session["download_file"]
    return send_file(get_download_file, as_attachment=True)
