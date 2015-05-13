# Alfred PNR

As part of a development project at the [UFPE][ufpe], this application aims to publish a simple API which shamefully scrap Amadeus [CheckMyTrip](cmt) webservice.

## API description

The applicaiton expose the following routes:

1. /find/\<pnr\>/\<lastname\>

This routes accepts as parameters:

* the [PNR][pnr]: usually the 6-character code you received once your booking is completed
* the passenger lastname: obviously your lastname used for booking

## Code

The web part has been developped using [Flask][flask] microframework.
It uses the awesome [requests][requests] package for requesting Amadeus webservice.
Finaly, the scraping is orchestrated through the [lxml][lxml] package

[ufpe]: http://www2.cin.ufpe.br/site/index.php "Centro de Informática"
[cmt]: https://classic.checkmytrip.com "Amadeus CheckMyTrip"
[pnr]: http://en.wikipedia.org/wiki/Passenger_name_record "Passenger Name Record Definition"
[flask]: http://flask.pocoo.org "Flask Microframework"
[requests]: http://docs.python-requests.org/en/latest/ "Requests: HTTP for Humans"
[lxml]: http://lxml.de "XML and HTML with Python"