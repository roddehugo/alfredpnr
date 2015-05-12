import lxml.html
import re
import requests

from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException


app = Flask(__name__)

base_url = 'https://classic.checkmytrip.com/plnext/XCMTXITN/'
end_url = '?SITE=XCMTXITN&LANGUAGE=GB'


def make_json_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.code
        if isinstance(ex, HTTPException)
        else 500
    )
    return response


def gen_post_url():
    r_get = requests.get(base_url + 'CleanUpSessionPui.action' + end_url)
    regex = re.search(';jsessionid=(.+)\?', r_get.text)
    return base_url + 'RetrievePNR.action;jsessionid=' + regex.group(1) + end_url


def retrieve_html(post_url, formdata):
    r_post = requests.post(post_url, data=formdata)
    content = r_post.text.replace('\n', '').replace('\r', '').replace('\t', '')
    return lxml.html.fromstring(content)


@app.route("/find/<pnr>/<lastname>")
def get(pnr, lastname):
    formdata = {
        'DIRECT_RETRIEVE': 'true',
        'SESSION_ID': '',
        'REC_LOC': pnr,
        'DIRECT_RETRIEVE_LASTNAME': lastname
    }
    html = retrieve_html(gen_post_url(), formdata)
    import ipdb
    ipdb.set_trace()

    fullname = html.xpath('//*[@id="pax2"]//span/text()')[0]
    _, email, _, tel = html.xpath('//*[@id="pax1"]//table[2]//td//text()')

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
                'summary': eti['number'],
                'date': html.xpath('//*[@id="tabFgtReview_%s"]//td[@class="textBold"][@colspan="2"]//text()' % i)[i].strip(),
                'departure': {
                    'time': time[0],
                    'loc': time[1]
                },
                'arrival': {
                    'time': time[2],
                    'loc': time[3]
                },
                'airline': time[5],
                'duration': time[7],
                'aircraft': time[9]
            })

    return jsonify(passenger=passenger, etickets=etickets, flights=flights)

if __name__ == '__main__':
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    app.run()
