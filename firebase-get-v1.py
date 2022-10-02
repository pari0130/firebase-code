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

docs = db.collection(u'items').where(u'prdkind', u'==', u'커피').order_by(u'prdlstReportNo', direction=BaseQuery.DESCENDING).limit(10).stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')