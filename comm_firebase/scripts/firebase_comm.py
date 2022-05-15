import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import rospy

cred = credentials.Certificate("/home/pratik/office_rbt_ws/src/comm_firebase/scripts/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

firestoreDB = firestore.client()

# firestoreDB.collection('Faculty_Name').document('Sir 3').set({'name':'John'})
# use above line to add new entries' data to firebase
url = 'https://carryo-bot-6f391-default-rtdb.firebaseio.com/'

prev_caller = ''
prev_receiver = ''
prev_time = 0
# global prev_caller, prev_receiver
first_time = True
call_rec = []
counter = 0



def communicate():
    global prev_caller, prev_receiver, prev_time, first_time
    if first_time:
        # do not consider the first data when the robots just starts
        name = db.reference('faculty_name', url=url).get()  # get data
        # print(name)
        prev_caller = name['Caller']
        prev_receiver = name['Reciever']
        first_time = False

    current_millis = rospy.get_time()
    time_eclapsed = abs(current_millis - prev_time)
    # print(time_eclapsed)
    if not first_time:
        # if its not first time then fetch the data and then send it to behaviour planner
        if time_eclapsed > 1:
            prev_time = current_millis
            name = db.reference('faculty_name', url=url).get()  # get data
            print(name)
            # print(name)
            if prev_caller != name['Caller'] or prev_receiver != name['Reciever']:
                # call_rec.clear()
                del call_rec[:]
                call_rec.append(name['Caller'])
                call_rec.append(name['Reciever'])
                prev_caller = name['Caller']
                prev_receiver = name['Reciever']
                return call_rec


# communicate()
def send_mode(mode):
    # print("sended mode to firebase")
    m = 5
    db.reference('mode', url=url).set(m)
