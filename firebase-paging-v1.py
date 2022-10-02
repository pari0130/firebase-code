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

limit = 10
query = db.collection("items") \
    .where(u'prdkind', u'==', u'커피') \
    .order_by(u'prdlstNm', direction=BaseQuery.ASCENDING) \
    .limit(limit)

docs = query.stream()
count = 0

while True:
    doc = None
    current_count = 0
    for doc in docs:
        current_count += 1
        print(f'{doc.id} => {doc.to_dict()}')

    last_doc = doc
    count += current_count

    if not last_doc or current_count < limit:
        break

    print("next_page")
    docs = query.start_after(last_doc).get()

print(f"count={count}")
