import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json

# Use a service account.
#DO NOT SHARE THE API KEY
cred = credentials.Certificate('capstone-45462-firebase-adminsdk-zzso5-df5915dc4b.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def initalize_firestore():
    #app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    #increment = firestore.Increment(1)
    batch = db.batch()

    statsRef = db.collection(u'MATLAB_Simulations').document(u'count') #initalize simulationsCount 
    batch.set(statsRef, {u'simulationsCount': 0}) #initalize simulationsCount to 0

#Test batch writing and incrememnt counter
increment = firestore.Increment(1)

batch = db.batch()
statsRef = db.collection(u'MATLAB_Simulations').document(u'count') #initalize simulationsCount 

#Write data to db, if the collection or document doesn't exist, it will be automatically written to db
#Feed input, output arrays to database; data structure: data = [[Simulation_name, input0,output0],...]
def write_data(data):
    #Select the collection 'Models' and add a new document with ID: record['Model']
    #data['Simulation'] parameter MUST BE A STRING IN ORDER TO BE WRITTEN
    doc_ref = db.collection(u'MATLAB_Simulations').document(data['ID']) #store a new document with the name of model
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

def batched_read(): 
    #read from firestore MATLAB_simulations collection,
    #outputs 2 dictionaries: input, output with key as each corresponding simulation ID (count)
    docs = db.collection(u'MATLAB_Simulations').stream()
    
    input_array = {}
    temp_input = []
    output_array = {}
    temp_output = []

    for doc in docs:
        current_doc = doc.to_dict()
        #print(current_doc['Input'])
        if ('Input' in current_doc.keys()): 
            #THIS MAY REQUIRE FLOAT CASTING EACH VALUE
            temp_key = current_doc['ID']
            temp_input = [(current_doc['Input'])]
            temp_output = [(current_doc['Output'])]

            input_array[temp_key] = temp_input
            output_array[temp_key] = temp_output

            print(temp_key, input_array, output_array)

    return input_array, output_array



def write_ML_parameters(): ##this will be in ML blackboard
    #Note for Eamon: this is hard-coded because I don't have your output functions
    #serialize weight matrix as JSON, then deserialize when reading
    weight_matrix = [[1, 2, 3], [3, 4, 5]] 
    
    #if weight matrix is a np.array

    #weight_matrix = np.array([[1, 2], [3, 4]])
    #list(weight_matrix) #convert np.array to a python list.

    Obj1 = {
    'Model': 'ANN',
    'Weights' : json.dumps(weight_matrix), #json serialize the list of lists or numpy array
    'Performance' : 0.92,
    }
    data = Obj1

    doc_ref = db.collection(u'Trained_Models').document(data['Model'])
    doc_ref.set(data)
    batch.update(statsRef, {u'modelsCount': increment})
    batch.commit()

def read_ML_parameters(): ##used to read the ML_parameters from firestore (in case we need this)
    #deserialize weight matrix json 
    doc_ref = db.collection(u'Trained_Models').document(u'ANN')

    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        read_weight_matrix_json = doc.to_dict()['Weights']
        weight_matrix = json.loads(read_weight_matrix_json)
        print(weight_matrix, type(weight_matrix))
    else:
        print(u'No such document!')

check_count()