# Google Map Data Scraper
Google map data scraper allows you to scrap bulk data from Google Maps to CSV format.


# Requirements

Python 3.5 and above.
Google Map API key

If you don't have python install on your machine you can get it from [here](https://www.python.org/downloads/f).
Get Google map api key from [here](https://developers.google.com/maps/documentation/javascript/get-api-key).
   
# Add Google Map API Key and App Secret to Environment Variable
Add google map api key and app secret to your environment variable.

    export GOOGlE_API_KEY="YOUR API KEY"
    export GOOGLE_SCRAPER_SECRET="YOUR APP SECRET"

## How to Setup

    $ mkdir Project
    $ cd Project
    $ git clone git@github.com:prashantkrsahu/google-map-scraper.git
    $ cd google-map-scraper
    $ pip install -r requirements.txt
    $ python manage.py

   
## 
    $ python manage.py
    Open http://127.0.0.1:5000/ in your brawser