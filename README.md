# Alfred PNR

As part of a development project at the [UFPE][ufpe], this application aims to publish a simple API which shamefully scrap Amadeus [CheckMyTrip][cmt] webservice.


## API description

The applicaiton exposes the following routes:

1. ``/find/<pnr>/<lastname>``

This routes accepts as parameters:

* the [PNR][pnr]: usually the 6-character code you received once your booking is completed
* the passenger lastname: obviously your lastname used for booking

It returns the following JSON success array:

```json
{
  "etickets": [
    {
      "number": "047-2739560319",
      "summary": "Paris - Recife"
    },
    {
      "number": "047-2729056392",
      "summary": "Recife - Paris"
    }
  ],
  "flights": {
    "047-2729056392": [
      {
        "aircraft": "Airbus Industrie A320",
        "airline": "Tam Linhas Aereas JJ3505",
        "arrival": {
          "location": "Sao Paulo, Brazil - Guarulhos International, terminal 2",
          "time": "21:00"
        },
        "date": "Sunday, May 10, 2015",
        "departure": {
          "location": "Recife, Brazil - Guararapes International",
          "time": "17:30"
        },
        "duration": "3:30",
        "summary": "Recife - Paris"
      },
      {
        "aircraft": "Boeing 777-300",
        "airline": "Tam Linhas Aereas JJ8084",
        "arrival": {
          "location": "London, United Kingdom - Heathrow, terminal 1",
          "time": "15:10"
        },
        "date": "Sunday, May 10, 2015",
        "departure": {
          "location": "Sao Paulo, Brazil - Guarulhos International, terminal 3",
          "time": "23:45"
        },
        "duration": "11:25",
        "summary": "Recife - Paris"
      },
      {
        "aircraft": "Airbus Industrie A319",
        "airline": "British Airways BA336",
        "arrival": {
          "location": "Paris, France - Orly, terminal W",
          "time": "18:55"
        },
        "date": "Sunday, May 10, 2015",
        "departure": {
          "location": "London, United Kingdom - Heathrow, terminal 5",
          "time": "16:40"
        },
        "duration": "1:15",
        "summary": "Recife - Paris"
      }
    ],
    "047-2739560319": [
      {
        "aircraft": "Airbus Industrie A320",
        "airline": "TAP Portugal TP433",
        "arrival": {
          "location": "Lisbon, Portugal - Airport, terminal 1",
          "time": "14:40"
        },
        "date": "Sunday, April 26, 2015",
        "departure": {
          "location": "Paris, France - Orly, terminal W",
          "time": "13:15"
        },
        "duration": "2:25",
        "summary": "Paris - Recife"
      },
      {
        "aircraft": "Airbus Industrie A330-200",
        "airline": "TAP Portugal TP011",
        "arrival": {
          "location": "Recife, Brazil - Guararapes International",
          "time": "20:40"
        },
        "date": "Sunday, April 26, 2015",
        "departure": {
          "location": "Lisbon, Portugal - Airport, terminal 1",
          "time": "16:50"
        },
        "duration": "7:50",
        "summary": "Paris - Recife"
      }
    ]
  },
  "passenger": {
    "email": "test@example.com",
    "fullname": "John Smith",
    "tel": "0123456789"
  },
  "status": "success"
}
```

And this one in case of error:

```json
{
  "message": "We are unable to find this confirmation number. Please validate your entry and try again. (8104 - 2273)",
  "status": "error"
}
```


## Code developement

The web part has been developped using [Flask][flask] microframework.

It uses the awesome [requests][requests] package for requesting Amadeus webservice.

Finaly, the scraping is orchestrated through the [lxml][lxml] package.

[ufpe]: http://www2.cin.ufpe.br/site/index.php "Centro de Informática"
[cmt]: https://classic.checkmytrip.com "Amadeus CheckMyTrip"
[pnr]: http://en.wikipedia.org/wiki/Passenger_name_record "Passenger Name Record Definition"
[flask]: http://flask.pocoo.org "Flask Microframework"
[requests]: http://docs.python-requests.org/en/latest/ "Requests: HTTP for Humans"
[lxml]: http://lxml.de "XML and HTML with Python"