API Documentation
=================

## Disaster

### Get Latest Disaster Reports

Request:

    GET /disasters

Params:

* `page`: Paging number. Default to 1.
* `per_page`: Items per page. Max. is 20.
* `category`: Disaster category, e.g. `earthquake`.

Response:

```json
{
  "items": [
    {
      "geometry": {
        "coordinates": [
          -147.9326,
          64.6649
        ],
        "type": "Point"
      },
      "id": "548393e044d7f22d5c71aab1",
      "properties": {
        "alert": null,
        "cdi": null,
        "code": "11458339",
        "detail": "http://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/ak11458339.geojson",
        "dmin": null,
        "felt": null,
        "gap": null,
        "ids": ",ak11458339,",
        "mag": 0.1,
        "magType": "ml",
        "mmi": null,
        "net": "ak",
        "nst": null,
        "place": "20km S of Ester, Alaska",
        "rms": 0.04,
        "sig": 0,
        "sources": ",ak,",
        "status": "automatic",
        "time": 1417905812000,
        "title": "M 0.1 - 20km S of Ester, Alaska",
        "tsunami": null,
        "type": "earthquake",
        "types": ",general-link,geoserve,nearby-cities,origin,",
        "tz": -540,
        "updated": 1417906732772,
        "url": "http://earthquake.usgs.gov/earthquakes/eventpage/ak11458339"
      },
      "source": "usgs",
      "source_id": "ak11458339",
      "type": "Feature"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 1
  }
}
```

Error Code:

* `200`: Request succeed.
* `400`: Invalid request or parameters.
* `404`: Empty result or incorrect URL.

### Get Nearby Disaster Reports

Request:

    GET /disasters/nearby

Params:

* `page`: Paging number. Default to 1.
* `per_page`: Items per page. Max. is 20.
* `lon`: Longitude.
* `lat`: Latitude.
* `radius`: Radius in meters. Must greater then equal zero.
* `category`: Disaster category, e.g. `earthquake`.

Response:

```json
{
  "items": [
    {
      "geometry": {
        "coordinates": [
          -147.9326,
          64.6649
        ],
        "type": "Point"
      },
      "id": "548393e044d7f22d5c71aab1",
      "properties": {
        "alert": null,
        "cdi": null,
        "code": "11458339",
        "detail": "http://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/ak11458339.geojson",
        "dmin": null,
        "felt": null,
        "gap": null,
        "ids": ",ak11458339,",
        "mag": 0.1,
        "magType": "ml",
        "mmi": null,
        "net": "ak",
        "nst": null,
        "place": "20km S of Ester, Alaska",
        "rms": 0.04,
        "sig": 0,
        "sources": ",ak,",
        "status": "automatic",
        "time": 1417905812000,
        "title": "M 0.1 - 20km S of Ester, Alaska",
        "tsunami": null,
        "type": "earthquake",
        "types": ",general-link,geoserve,nearby-cities,origin,",
        "tz": -540,
        "updated": 1417906732772,
        "url": "http://earthquake.usgs.gov/earthquakes/eventpage/ak11458339"
      },
      "source": "usgs",
      "source_id": "ak11458339",
      "type": "Feature"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 1
  }
}
```

Error Code:

* `200`: Request succeed.
* `400`: Invalid request or parameters.
* `404`: Empty result or incorrect URL.

### Verify Disaster Report

Request:

    GET /disasters/verify

Params:

* `lon`: Longitude.
* `lat`: Latitude.
* `radius`: Radius in meters. Must greater than equal zero.
* `category`: Disaster category, e.g. `earthquake`.

Response:

```json
{
  "message": "OK"
}
```

Error Code:

* `200`: Request succeed.
* `400`: Invalid request or parameters.
* `404`: Empty result or incorrect URL.

### Get Specific Disaster Report

Request:

    GET /disasters/{id}

Response:

```json
{
    "geometry": {
    "coordinates": [
        -147.9326,
        64.6649
    ],
    "type": "Point"
    },
    "id": "548393e044d7f22d5c71aab1",
    "properties": {
        "alert": null,
        "cdi": null,
        "code": "11458339",
        "detail": "http://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/ak11458339.geojson",
        "dmin": null,
        "felt": null,
        "gap": null,
        "ids": ",ak11458339,",
        "mag": 0.1,
        "magType": "ml",
        "mmi": null,
        "net": "ak",
        "nst": null,
        "place": "20km S of Ester, Alaska",
        "rms": 0.04,
        "sig": 0,
        "sources": ",ak,",
        "status": "automatic",
        "time": 1417905812000,
        "title": "M 0.1 - 20km S of Ester, Alaska",
        "tsunami": null,
        "type": "earthquake",
        "types": ",general-link,geoserve,nearby-cities,origin,",
        "tz": -540,
        "updated": 1417906732772,
        "url": "http://earthquake.usgs.gov/earthquakes/eventpage/ak11458339"
    },
    "source": "usgs",
    "source_id": "ak11458339",
    "type": "Feature"
}
```

Error Code:

* `200`: Request succeed.
* `404`: Empty result or incorrect URL.
