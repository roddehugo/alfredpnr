# -*- coding: utf-8 -*-
import lxml.html
import re
import requests

from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

################################
# Alfred PNR Flask Application #
################################
app = Flask(__name__)

# Define url pieces
base_url = 'http://classic.checkmytrip.com/plnext/XCMTXITN/'
end_url = '?SITE=XCMTXITN&LANGUAGE=GB'


def make_json_error(ex):
    """
    Specialized JSON-oriented Flask App
    When things go wrong, default errors that Flask/Werkzeug respond with are all HTML.
    Which breaks the clients who expect JSON back even in case of errors.
    All errors that Werkzeug may throw are now intercepted and converted into JSON response
    http://flask.pocoo.org/snippets/83/
    """
    response = jsonify(status="error", message=str(ex))
    response.status_code = (
        ex.code
        if isinstance(ex, HTTPException)
        else 500
    )
    return response


def gen_post_url():
    """
    Generate the POST url
    First make a GET request to fetch the session id from Amadeus form
    Then concatenate the url using both url pieces aforementioned
    """
    response = requests.get(base_url + 'CleanUpSessionPui.action' + end_url)
    response.raise_for_status()
    regex = re.search(r';jsessionid=(.+)\?', response.text)
    try:
        return base_url + 'RetrievePNR.action;jsessionid=' + regex.group(1) + end_url
    except AttributeError, e:
        raise Exception("Cant' find jsessionid in GET response.")


def retrieve_html(posturl, formdata):
    """
    Fetch HTML DOM
    Make a POST request with data and sanitize it
    Returns the lxml object from post response
    """
    response = requests.post(posturl, data=formdata)
    response.raise_for_status()
    content = response.text.replace('\n', '').replace('\r', '').replace('\t', '')
    return lxml.html.fromstring(content)


def scrap_data(html):
    """
    Do the Job
    Use lxml xpath method to scrap data from html DOM
    Returns a dict containing:
        - passenger information
        - etickets number
        - corresponding flights for the given PNR
    """
    if html.xpath('//*[@id="WDSError"][@style="width:95%;display:none"]'):
        script = html.xpath('//script[@language="javascript"]//text()')[-1]
        error = re.search(r'WDSError\.add\("(.+)"\);', script)
        raise Exception(error.group(1))

    try:
        fullname = html.xpath('//*[@id="pax2"]//span/text()')[0]
        _, email, _, tel = html.xpath('//*[@id="pax1"]//table[2]//td//text()')
    except IndexError, ValueError:
        raise Exception('Unable to find passenger information. Please review scraping process!')

    passenger = {
        'fullname': fullname.strip(),
        'email': email.strip(),
        'tel': tel.strip()
    }

    etickets = [
        {
            'number': eti[0],
            'summary': eti[1]
        }
        for eti in zip(
            [x[9:-1] for x in html.xpath('//*[@id="documentNumber_1"]//text()')],
            [x.strip() for x in html.xpath('//*[@id="eticketNumbers"]//th[@class="cfsp_c2"]//text()')]
        )
    ]

    flights = {}

    for i, eti in enumerate(etickets):
        flights[eti['number']] = []

        for j in range(0, len(html.xpath('//*[@id="tabFgtReview_%s"]/tr' % i)) / 5):
            time = [
                x.strip()
                for x in html.xpath('(//*[@id="tabFgtReview_%s"]/tr/td/table)[%s]//td/text()' % (i, j+1))
                if x.strip()
            ]

            flights[eti['number']].append({
                'summary': eti['summary'],
                'date': html.xpath(
                    '//*[@id="tabFgtReview_%s"]//td[@class="textBold"][@colspan="2"]//text()' % i
                )[i].strip(),
                'departure': {
                    'time': time[0],
                    'location': time[1]
                },
                'arrival': {
                    'time': time[2],
                    'location': time[3]
                },
                'airline': time[5].replace(u'\xa0', ' '),
                'duration': time[7],
                'aircraft': time[9]
            })

    return passenger, etickets, flights


@app.route("/find/<pnr>/<lastname>")
def find(pnr, lastname):
    """
    Flask API main route
    GET Method with two parameters:
        - Passenger Name Record
        - Passenger Lastname
    Returns a JSON response
    """
    formdata = {
        'DIRECT_RETRIEVE': 'true',
        'SESSION_ID': '',
        'REC_LOC': pnr,
        'DIRECT_RETRIEVE_LASTNAME': lastname
    }

    html = retrieve_html(gen_post_url(), formdata)
    passenger, etickets, flights = scrap_data(html)
    return jsonify(status="success", passenger=passenger, etickets=etickets, flights=flights)

if __name__ == '__main__':
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    app.run()
