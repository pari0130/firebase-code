import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
from time import sleep
import urllib3

fp = open('./haccp-key.txt', 'r')
key = fp.readline()
print(key)
fp.close()

http = urllib3.PoolManager()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
cred = credentials.Certificate("./auth.json")
firebase_admin.initialize_app(cred, {
    'projectId': "food-haccp",
})
db = firestore.client()


def firestore_save(item):
    document = item['prdlstReportNo']
    doc_ref = db.collection(u'items').document(u'{}'.format(document))
    doc_ref.set(item)


def get_food_items(_page):
    url = f"https://apis.data.go.kr/B553748/CertImgListService/getCertImgListService?returnType=json&pageNo={_page}" \
          "&numOfRows=100" + \
          f"&serviceKey={key}"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}

    print(f"call url -> {url}")

    try:
        req = http.request('GET', url, headers=headers)
        response = json.loads(req.data)
        print(str(_page) + " page -> " + str(response))

        header = response['header']
        body = response['body']

        if header['resultCode'] == "OK":
            if body['totalCount'] == '0' or len(body['items']) == 0:
                print("break")
                return
            else:
                for item in body['items']:
                    print(item['item'])
                    firestore_save(item['item'])
                _page += 1
                sleep(0.5)
                get_food_items(_page)
        else:
            print("not ok break")
    except Exception as ex:
        print(ex)


get_food_items(1)
