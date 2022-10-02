import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
import urllib3
from google.cloud.firestore_v1.base_query import BaseQuery

http = urllib3.PoolManager()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
cred = credentials.Certificate("./auth.json")
firebase_admin.initialize_app(cred, {
    'projectId': "food-haccp",
})
db = firestore.client()

docs1 = db.collection(u'items')\
    .where(u'prdkind', u'==', u'커피')\
    .order_by(u'prdlstNm', direction=BaseQuery.ASCENDING)\
    .limit(10)\
    .stream()

for doc in docs1:
    print(f'{doc.id} => {doc.to_dict()}')

print("--------------")

docs2 = db.collection(u'items')\
    .where(u'prdkind', u'==', u'커피')\
    .order_by(u'prdlstNm', direction=BaseQuery.ASCENDING) \
    .limit(5) \
    .stream()

for doc in docs2:
    print(f'{doc.id} => {doc.to_dict()}')

print("--------------")

last_doc = list(docs2)[-1]
last_pop = last_doc.to_dict()[u'prdlstNm']

docs3 = db.collection(u'items')\
        .where(u'prdkind', u'==', u'커피')\
        .order_by(u'prdlstNm', direction=BaseQuery.ASCENDING)\
        .start_after({u'prdlstNm': last_pop})\
        .limit(5) \
        .stream()

for doc in docs3:
    print(f'{doc.id} => {doc.to_dict()}')
