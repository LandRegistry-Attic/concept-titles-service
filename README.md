Post a System of Record revision
POST /titles-revisions

Get a title
GET /titles/{title_id}

Filter by postcode
GET /titles?postcode={value}

Example:
GET /titles/SY938123
****
Response body:

    {

        "title_number" : "SY938123",

        "address": "123 Fake St",

        "postcode": "ABC12 3CD",

        "registered_owners": [

            {

                "name": "A N Other",

                "address": "123 Fake St"

            },

            {

                "name": "B Other",

                "address": "123 Fake St"

            }

        ],

        "lenders": [

            {

                "name": "Acme Bank PLC"

            }

        ],

        "extent" : 

        {

            "type": "multi_polygon", 

            "coordinates": [

                [

                    [[30, 20], [45, 40], [10, 40], [30, 20]]

                ], 

                [

                    [[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]

                ]

            ]

        }

    }