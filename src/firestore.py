import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
#DO NOT SHARE THE API KEY
cred = credentials.Certificate('capstone-45462-firebase-adminsdk-zzso5-df5915dc4b.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def initalize_firestore():
    #app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    increment = firestore.Increment(1)
    batch = db.batch()

    statsRef = db.collection(u'MATLAB_Simulations').document(u'count') #initalize simulationsCount 
    batch.set(statsRef, {u'simulationsCount': 0}) #initalize simulationsCount to 0

#Test batch writing and incrememnt counter
increment = firestore.Increment(1)

batch = db.batch()
statsRef = db.collection(u'MATLAB_Simulations').document(u'count') #initalize simulationsCount 

#Write data to db, if the colletcion or document doesn't exist, it will be automatically written to db
#Feed input, output arrays to database; data structure: data = [[Simulation_name, input0,output0],...]
def write_data(data):
    #Select the collection 'Models' and add a new document with ID: record['Model']
    #data['Simulation'] parameter MUST BE A STRING IN ORDER TO BE WRITTEN
    doc_ref = db.collection(u'MATLAB_Simulations').document(data['Simulation']) #store a new document with the name of model
    doc_ref.set(data)
    batch.update(statsRef, {u'simulationsCount': increment}) #increment the counter of how many simulations have been stored
    batch.commit()

def check_count():
    doc_ref = db.collection(u'MATLAB_Simulations').document(u'count')
    doc = doc_ref.get()
    if doc.exists: 
        #print(f'Current Count: {doc.to_dict()}')
        count = doc.to_dict()['simulationsCount']
    else: #if count doesn't exist yet, initalize to 0 
        #print(u'No such document!')
        statsRef = db.collection(u'MATLAB_Simulations').document(u'count') #initalize simulationsCount 
        batch.set(statsRef, {u'simulationsCount': 0}) #initalize simulationsCount to 0 
        batch.commit()
        count = 0 
    return count