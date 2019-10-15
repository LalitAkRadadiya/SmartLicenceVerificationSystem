import os
import cv2
import urllib.parse
import time
import urllib.request
import face_recognition
import glob
import sys

known_face_encodings=[]
known_face_names=[]
video_capture = cv2.VideoCapture(0)
process_this_frame = True
known_number=[]


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def parseNamePHP(name, number):
    url = 'http://localhost/Hackathon-htdocs/htdocs/data.php'
    mydata = [('username', name), ('number', number)]
    mydata = urllib.parse.urlencode(mydata).encode('utf-8')
    req = urllib.request.Request(url, mydata)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    print(the_page)

def readData(dir):
    cd=os.getcwd()
    for d in (os.listdir(dir)):
        print(d)
        os.chdir(os.path.join(cd,dir,d))
        #Counts the number of jpg files
        temp_file_name = d+".jpg"
        temp_img=face_recognition.load_image_file(temp_file_name)
        temp_face_encoding = face_recognition.face_encodings(temp_img)[0]
        known_face_encodings.append(temp_face_encoding)
        text_file = open(os.path.join(os.getcwd(),d)+".txt","r")
        name=text_file.readline()
        number=text_file.readline()
        known_face_names.append(name)
        number.replace(" ","")
        known_number.append(number)

def detection(process_this_frame):
    name=""
    x=0
    y=0
    

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.49)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    number = known_number[first_match_index]
                face_names.append(name)

        process_this_frame = not process_this_frame
        # Display the results

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            if name=="Unknown":
            	y=y+1
            	print(name)
            	print(y)
            	if y==20:
            		sys.exit(os.system("curl https://notify.run/m9K1NtcVlrkTgvP6 -d 'Unknown Person come to your Home'"))
            else:
            	x=x+1
            	y=0
            	print(name,x)
        

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit()
        # elif name!="" and name!="Unknown":
        #     time.sleep(4)
        #     break
        
    return name,number
def main():
    readData("known_people")
    name,number = detection(process_this_frame)
    print(name,number)
    parseNamePHP(name,number)

main()
