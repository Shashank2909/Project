import cv2 
import os

def face_save(name):
    vid = cv2.VideoCapture(0) 
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    path = os.getcwd()
    directory = os.path.join(path,'training',name)
    try:
        os.makedirs(directory)
    except FileExistsError:
        print("Error")
    os.chdir(directory) 
    count = 0
    while True:
        ret,img = vid.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if faces is None:
            continue
        elif count<=10:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                crop = gray[y:y+h,x:x+w]
                resize_img = cv2.resize(crop,(30,30))
                s = '{}-{}.jpeg'.format(name,count)
                cv2.imwrite(s,resize_img)
                count+=1
            
                    

        cv2.imshow('img', img)
       

        if count==10:
            break

    vid.release()
    cv2.destroyAllWindows()

# i = int(input("Do you want to register a user?...press 1"))

# if i==1:
#     name = input("Enter the name")
#     face_save(name)

face_save('shashank')