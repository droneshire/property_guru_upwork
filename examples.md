# Examples

## Listing API Response:
```
import requests

cookies = {
    'pgutid': 'e91a4650-fee8-4d8e-b6ab-19e1f8b180c5',
    '_ga': 'GA1.3.885489030.1688137301',
    'ajs_anonymous_id': 'e91a4650-fee8-4d8e-b6ab-19e1f8b180c5',
    '_hjSessionUser_2468245': 'eyJpZCI6IjgzNzFhMjMwLTc5N2ItNTM1MS1hOWQ1LTA2MzM2NmNiYjZiNyIsImNyZWF0ZWQiOjE2ODgxMzczMDIyODksImV4aXN0aW5nIjp0cnVlfQ==',
    '_gid': 'GA1.3.1822253008.1688434294',
    '_hjSession_2468245': 'eyJpZCI6ImJiMGExYzA0LWI2NDktNDU0ZS1iMzFkLTZhMjQ2MTA5MmIyNyIsImNyZWF0ZWQiOjE2ODg0MzQyOTU3MDIsImluU2FtcGxlIjpmYWxzZX0=',
    'ln_or': 'eyI0MTM5MzMyIjoiZCJ9',
    'ab.storage.deviceId.598492ca-0323-4cd6-a8dd-62e8595da78f': '%7B%22g%22%3A%224f32e07f-abe5-64d5-de56-9a75956fdbc1%22%2C%22c%22%3A1688137302852%2C%22l%22%3A1688434364962%7D',
    'PHPSESSID2': 'f65f7bbf785c3603f2baf0fbf039ecf6',
    'sixpack_client_id': '10BE6BA0-D176-FF69-9165-E50EE54632DE',
    'Visitor': '88e5ab1b-1159-4975-93d8-25b4717217fe',
    'pgutid': 'e91a4650-fee8-4d8e-b6ab-19e1f8b180c5',
    '_gaexp': 'GAX1.3.FQSP2Dq7QUmm5P82ZCMPAg.19631.1',
    'cf_chl_2': '4b1788fa27d7381',
    'cf_clearance': 'ttQavGLu8WJLpP0_2I8Ysjrzs0EunMVhgcYQqdv6wSg-1688435122-0-160',
    '__cf_bm': '7Kw_aus5__9AXJ8IpMzUgA4dIjNH0oySzjB0B1EZ05o-1688435285-0-AfYpdIkwXy+bRiJ9KViSAscamO9PDv5bo8eQ1Cyg6LbYOaWWXYQ8kt1dbCMzBKReuie4O4baSDbYmLWsraAIUuzBshg/0+V7mvdMlIfPP1JBUdS0zmnpJPxs7Swt+JViOA==',
    '_gat': '1',
    '_gat_regionalTracker': '1',
    'ab.storage.sessionId.598492ca-0323-4cd6-a8dd-62e8595da78f': '%7B%22g%22%3A%22f8d15167-e1fd-1271-66e5-9cff39543d7c%22%2C%22e%22%3A1688437237459%2C%22c%22%3A1688434364959%2C%22l%22%3A1688435437459%7D',
    '_ga_GD79JNX1P7': 'GS1.3.1688434920.1.1.1688435489.8.0.0',
    'ldpv': '24395172.1688434293742%2C24508728.1688435491732',
}

headers = {
    'authority': 'www.propertyguru.com.sg',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'pgutid=e91a4650-fee8-4d8e-b6ab-19e1f8b180c5; _ga=GA1.3.885489030.1688137301; ajs_anonymous_id=e91a4650-fee8-4d8e-b6ab-19e1f8b180c5; _hjSessionUser_2468245=eyJpZCI6IjgzNzFhMjMwLTc5N2ItNTM1MS1hOWQ1LTA2MzM2NmNiYjZiNyIsImNyZWF0ZWQiOjE2ODgxMzczMDIyODksImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.3.1822253008.1688434294; _hjSession_2468245=eyJpZCI6ImJiMGExYzA0LWI2NDktNDU0ZS1iMzFkLTZhMjQ2MTA5MmIyNyIsImNyZWF0ZWQiOjE2ODg0MzQyOTU3MDIsImluU2FtcGxlIjpmYWxzZX0=; ln_or=eyI0MTM5MzMyIjoiZCJ9; ab.storage.deviceId.598492ca-0323-4cd6-a8dd-62e8595da78f=%7B%22g%22%3A%224f32e07f-abe5-64d5-de56-9a75956fdbc1%22%2C%22c%22%3A1688137302852%2C%22l%22%3A1688434364962%7D; PHPSESSID2=f65f7bbf785c3603f2baf0fbf039ecf6; sixpack_client_id=10BE6BA0-D176-FF69-9165-E50EE54632DE; Visitor=88e5ab1b-1159-4975-93d8-25b4717217fe; pgutid=e91a4650-fee8-4d8e-b6ab-19e1f8b180c5; _gaexp=GAX1.3.FQSP2Dq7QUmm5P82ZCMPAg.19631.1; cf_chl_2=4b1788fa27d7381; cf_clearance=ttQavGLu8WJLpP0_2I8Ysjrzs0EunMVhgcYQqdv6wSg-1688435122-0-160; __cf_bm=7Kw_aus5__9AXJ8IpMzUgA4dIjNH0oySzjB0B1EZ05o-1688435285-0-AfYpdIkwXy+bRiJ9KViSAscamO9PDv5bo8eQ1Cyg6LbYOaWWXYQ8kt1dbCMzBKReuie4O4baSDbYmLWsraAIUuzBshg/0+V7mvdMlIfPP1JBUdS0zmnpJPxs7Swt+JViOA==; _gat=1; _gat_regionalTracker=1; ab.storage.sessionId.598492ca-0323-4cd6-a8dd-62e8595da78f=%7B%22g%22%3A%22f8d15167-e1fd-1271-66e5-9cff39543d7c%22%2C%22e%22%3A1688437237459%2C%22c%22%3A1688434364959%2C%22l%22%3A1688435437459%7D; _ga_GD79JNX1P7=GS1.3.1688434920.1.1.1688435489.8.0.0; ldpv=24395172.1688434293742%2C24508728.1688435491732',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.propertyguru.com.sg/listing/for-sale-the-woodleigh-residences-24508728',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

params = {
    'projectUrl': 'the-woodleigh-residences-23532',
    'listingId': '24508728',
    'projectId': '23532',
    'statusCode': 'ACT',
    'listingType': 'SALE',
    'bedrooms': '2',
    'listingTypeText': 'For Sale',
    'propertyName': 'The Woodleigh Residences',
    'locale': 'en',
    'region': 'sg',
}

response = requests.get(
    'https://www.propertyguru.com.sg/api/consumer/listings/other',
    params=params,
    cookies=cookies,
    headers=headers,
)
```

```

{
  "items": [
    {
      "id": 24565932,
      "title": "The Woodleigh Residences",
      "address": "19 Bidadari Park Drive",
      "image": "https://sg1-cdn.pgimgs.com/listing/24565932/UPHO.142479904.V550/The-Woodleigh-Residences-Macpherson-Potong-Pasir-Singapore.jpg",
      "link": {
        "href": "https://www.propertyguru.com.sg/listing/for-sale-the-woodleigh-residences-24565932"
      },
      "data": {
        "label": {
          "typeLabel": "Apartment"
        },
        "pricing": {
          "price": "S$ 1,350,000"
        },
        "rooms": {
          "baths": 1,
          "beds": 2
        }
      },
      "metadata": {},
      "context": {
        "data": {
          "id": 24565932,
          "name": "The Woodleigh Residences",
          "price": 1350000,
          "category": "Apartment",
          "brand": "Kajima Development Pte Ltd & Singapore Press Holdings Ltd",
          "variant": "Sale",
          "position": 1,
          "dimension19": 59242,
          "dimension22": "{\"page\":1,\"limit\":8,\"rank\":1}",
          "dimension23": "{\"Product\":[\"Turbo\"]}",
          "dimension24": "ACT",
          "dimension25": 59242,
          "dimension40": ""
        }
      },
      "shouldRenderRooms": true
    },
    {
      "id": 24552143,
      "title": "The Woodleigh Residences",
      "address": "23 Bidadari Park Drive",
      "image": "https://sg1-cdn.pgimgs.com/listing/24552143/UPHO.142320675.V550/The-Woodleigh-Residences-Macpherson-Potong-Pasir-Singapore.jpg",
      "link": {
        "href": "https://www.propertyguru.com.sg/listing/for-sale-the-woodleigh-residences-24552143"
      },
      "data": {
        "label": {
          "typeLabel": "Apartment"
        },
        "pricing": {
          "price": "S$ 1,290,000"
        },
        "rooms": {
          "baths": 1,
          "beds": 2
        }
      },
      "metadata": {},
      "context": {
        "data": {
          "id": 24552143,
          "name": "The Woodleigh Residences",
          "price": 1290000,
          "category": "Apartment",
          "brand": "Kajima Development Pte Ltd & Singapore Press Holdings Ltd",
          "variant": "Sale",
          "position": 2,
          "dimension19": 10418822,
          "dimension22": "{\"page\":1,\"limit\":8,\"rank\":2}",
          "dimension23": "{\"Product\":[\"Turbo\"]}",
          "dimension24": "ACT",
          "dimension25": 10418822,
          "dimension40": ""
        }
      },
      "shouldRenderRooms": true
    },
    {
      "id": 24464923,
      "title": "The Woodleigh Residences",
      "address": "Bidadari Park Drive",
      "image": "https://sg1-cdn.pgimgs.com/listing/24464923/UPHO.142477689.V550/The-Woodleigh-Residences-Macpherson-Potong-Pasir-Singapore.jpg",
      "link": {
        "href": "https://www.propertyguru.com.sg/listing/for-sale-the-woodleigh-residences-24464923"
      },
      "data": {
        "label": {
          "typeLabel": "Apartment"
        },
        "pricing": {
          "price": "S$ 1,625,000"
        },
        "rooms": {
          "baths": 2,
          "beds": 2
        }
      },
      "metadata": {},
      "context": {
        "data": {
          "id": 24464923,
          "name": "The Woodleigh Residences",
          "price": 1625000,
          "category": "Apartment",
          "brand": "Kajima Development Pte Ltd & Singapore Press Holdings Ltd",
          "variant": "Sale",
          "position": 3,
          "dimension19": 10263498,
          "dimension22": "{\"page\":1,\"limit\":8,\"rank\":3}",
          "dimension23": "{\"Product\":[\"Turbo\"]}",
          "dimension24": "ACT",
          "dimension25": 10263498,
          "dimension40": ""
        }
      },
      "shouldRenderRooms": true
    },
    {
      "id": 24395172,
      "title": "The Woodleigh Residences",
      "address": "21 Bidadari Park Drive",
      "image": "https://sg1-cdn.pgimgs.com/listing/24395172/UPHO.141991101.V550/The-Woodleigh-Residences-Macpherson-Potong-Pasir-Singapore.jpg",
      "link": {
        "href": "https://www.propertyguru.com.sg/listing/for-sale-the-woodleigh-residences-24395172"
      },
      "data": {
        "label": {
          "typeLabel": "Apartment"
        },
        "pricing": {
          "price": "S$ 1,300,000"
        },
        "rooms": {
          "baths": 1,
          "beds": 2
        }
      },
      "metadata": {},
      "context": {
        "data": {
          "id": 24395172,
          "name": "The Woodleigh Residences",
          "price": 1300000,
          "category": "Apartment",
          "brand": "Kajima Development Pte Ltd & Singapore Press Holdings Ltd",
          "variant": "Sale",
          "position": 4,
          "dimension19": 437083,
          "dimension22": "{\"page\":1,\"limit\":8,\"rank\":4}",
          "dimension23": "{\"Product\":[\"Turbo\"]}",
          "dimension24": "ACT",
          "dimension25": 437083,
          "dimension40": ""
        }
      },
      "shouldRenderRooms": true
    },
    {
      "id": 24486168,
      "title": "The Woodleigh Residences",
      "address": "21 Bidadari Park Drive",
      "image": "https://sg1-cdn.pgimgs.com/listing/24486168/UPHO.141567434.V550/The-Woodleigh-Residences-Macpherson-Potong-Pasir-Singapore.jpg",
      "link": {
        "href": "https://www.propertyguru.com.sg/listing/for-sale-the-woodleigh-residences-24486168"
      },
      "data": {
        "label": {
          "typeLabel": "Apartment"
        },
        "pricing": {
          "price": "S$ 1,350,000"
        },
        "rooms": {
          "baths": 1,
          "beds": 2
        }
      },
      "metadata": {},
      "context": {
        "data": {
          "id": 24486168,
          "name": "The Woodleigh Residences",
          "price": 1350000,
          "category": "Apartment",
          "brand": "Kajima Development Pte Ltd & Singapore Press Holdings Ltd",
          "variant": "Sale",
          "position": 5,
          "dimension19": 628635,
          "dimension22": "{\"page\":1,\"limit\":8,\"rank\":5}",
          "dimension23": "{\"Product\":[\"Turbo\"]}",
          "dimension24": "ACT",
          "dimension25": 628635,
          "dimension40": ""
        }
      },
      "shouldRenderRooms": true
    },
    {
      "id": 24500131,
      "title": "The Woodleigh Residences",
      "address": "Bidadari Park Drive",
      "image": "https://sg1-cdn.pgimgs.com/listing/24500131/UPHO.141724050.V550/The-Woodleigh-Residences-Macpherson-Potong-Pasir-Singapore.jpg",
      "link": {
        "href": "https://www.propertyguru.com.sg/listing/for-sale-the-woodleigh-residences-24500131"
      },
      "data": {
        "label": {
          "typeLabel": "Apartment"
        },
        "pricing": {
          "price": "S$ 1,348,000"
        },
        "rooms": {
          "baths": 1,
          "beds": 2
        }
      },
      "metadata": {},
      "context": {
        "data": {
          "id": 24500131,
          "name": "The Woodleigh Residences",
          "price": 1348000,
          "category": "Apartment",
          "brand": "Kajima Development Pte Ltd & Singapore Press Holdings Ltd",
          "variant": "Sale",
          "position": 6,
          "dimension19": 496494,
          "dimension22": "{\"page\":1,\"limit\":8,\"rank\":6}",
          "dimension23": "{\"Product\":[\"Turbo\"]}",
          "dimension24": "ACT",
          "dimension25": 496494,
          "dimension40": ""
        }
      },
      "shouldRenderRooms": true
    },
    {
      "id": 24468604,
      "title": "The Woodleigh Residences",
      "address": "11 Bidadari Park Drive",
      "image": "https://sg1-cdn.pgimgs.com/listing/24468604/UPHO.141369604.V550/The-Woodleigh-Residences-Macpherson-Potong-Pasir-Singapore.jpg",
      "link": {
        "href": "https://www.propertyguru.com.sg/listing/for-sale-the-woodleigh-residences-24468604"
      },
      "data": {
        "label": {
          "typeLabel": "Apartment"
        },
        "pricing": {
          "price": "S$ 1,280,000"
        },
        "rooms": {
          "baths": 1,
          "beds": 2
        }
      },
      "metadata": {},
      "context": {
        "data": {
          "id": 24468604,
          "name": "The Woodleigh Residences",
          "price": 1280000,
          "category": "Apartment",
          "brand": "Kajima Development Pte Ltd & Singapore Press Holdings Ltd",
          "variant": "Sale",
          "position": 7,
          "dimension19": 14358259,
          "dimension22": "{\"page\":1,\"limit\":8,\"rank\":7}",
          "dimension23": "{\"Product\":[\"Turbo\"]}",
          "dimension24": "ACT",
          "dimension25": 14358259,
          "dimension40": ""
        }
      },
      "shouldRenderRooms": true
    },
    {
      "id": 24484769,
      "title": "The Woodleigh Residences",
      "address": "19 Bidadari Park Drive",
      "image": "https://sg1-cdn.pgimgs.com/listing/24484769/UPHO.141586144.V550/The-Woodleigh-Residences-Macpherson-Potong-Pasir-Singapore.jpg",
      "link": {
        "href": "https://www.propertyguru.com.sg/listing/for-sale-the-woodleigh-residences-24484769"
      },
      "data": {
        "label": {
          "typeLabel": "Apartment"
        },
        "pricing": {
          "price": "S$ 1,450,000"
        },
        "rooms": {
          "baths": 2,
          "beds": 2
        }
      },
      "metadata": {},
      "context": {
        "data": {
          "id": 24484769,
          "name": "The Woodleigh Residences",
          "price": 1450000,
          "category": "Apartment",
          "brand": "Kajima Development Pte Ltd & Singapore Press Holdings Ltd",
          "variant": "Sale",
          "position": 8,
          "dimension19": 291918,
          "dimension22": "{\"page\":1,\"limit\":8,\"rank\":8}",
          "dimension23": "{\"Product\":[\"Turbo\"]}",
          "dimension24": "ACT",
          "dimension25": 291918,
          "dimension40": ""
        }
      },
      "shouldRenderRooms": true
    }
  ],
  "title": "124 Other Properties For Sale In The Woodleigh Residences",
  "action": {
    "name": "View All",
    "href": "/property-for-sale/at-the-woodleigh-residences-23532"
  }
}
```
