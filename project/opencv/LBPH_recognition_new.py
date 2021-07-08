#!/usr/bin/env python
# coding: utf-8

# In[24]:


import numpy as np
import os
import math
#import matplotlib.pyplot as plt
import cv2
import time
# from gtts import gTTS
import os
import shutil
#import motor
import em
import receive
import sms
# In[25]:

USER = "face"
PASSWORD = "f"

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_alt.xml")  # Object of face detector
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

roi_gray = []

#Removes parts of the sides of the face
#This is done so that the algorithm has to work with only the relevant/ most important part of the image
def cut_faces(image, faces_coord):
    faces = []

    for (x, y, w, h) in faces_coord:                                        #Trims parts of the face
        w_rm = int(0.2 * w / 2)
        faces.append(image[y : y + h, x + w_rm :  x + w - w_rm])

    return faces                                                            #Returns co-ordinates of the face

def save_faces(frame,faces,folder,counter):
    cut_face = cut_faces(frame, faces)

    face_bw = cv2.cvtColor(cut_face[0], cv2.COLOR_BGR2GRAY)

    face_bw_eq = cv2.equalizeHist(face_bw)
    face_bw_eq = cv2.resize(face_bw_eq, (256, 256), interpolation = cv2.INTER_CUBIC)
    #cv2.imshow('Face Recogniser', face_bw_eq)


    cv2.imwrite(folder + '/' + str(counter) + '.png',
                face_bw_eq)
    print('Images Saved:' + str(counter))
    cv2.imshow('Saved Face', face_bw_eq)
# In[26]:



def recieved():
    cv2.destroyAllWindows()
    while receive.r():
        if True:
            pass
            # motor.run_motor()
            break
    live()


#Adds a new person to the dataset and creates a separate folder for them
def add_person2(e9):
    person_name = e9.get()     #Get the name of the new person

    folder = 'people_folder' +'/'+ person_name

    if not os.path.exists(folder):                                          #Find the if the data for the given person already exists

        os.makedirs(folder)                                                    # Makes the new folder for saving the photos

        video = cv2.VideoCapture(0)

        counter = 1
        timer = 0

        cv2.namedWindow('Video Feed', cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('Saved Face', cv2.WINDOW_NORMAL)

        while counter < 21:
            _, frame = video.read()


            if counter == 1:
                time.sleep(6)
            else:
                time.sleep(1)

            faces = face_cascade.detectMultiScale(frame,1.3,4)
            profile_faces = profile_cascade.detectMultiScale(frame,1.3,4)

            if len(faces):
                save_faces(frame,faces,folder,counter)
                counter += 1
            elif len(profile_faces):
                save_faces(frame,profile_faces,folder,counter)
                counter += 1

            cv2.imshow('Video Feed', frame)
            cv2.waitKey(50)
            
            
    else:
        print("This name already exists.")
        
    cv2.destroyAllWindows()

# In[27]:


#Does the face recognition in real time
#Pressing ESC closes the live recognition
def live():

    cv2.namedWindow('Predicting for')
    images = []
    labels = []
    labels_dic = {}
    people = [person for person in os.listdir("people_folder")]
    threshold = 37


    for i, person in enumerate(people):
        print(person)
        labels_dic[i] = person

        for image in os.listdir("people_folder/" + person):
            print(image)
            images.append(cv2.imread('people_folder/'+person+'/'+ image, 0))
            labels.append(i)

    labels = np.array(labels)

    #rec_eig = cv2.face.EigenFaceRecognizer_create()
    rec_lbhp = cv2.face.LBPHFaceRecognizer_create()
    rec_lbhp.train(images, labels)

    cv2.namedWindow('face')
    webcam = cv2.VideoCapture(0)
    k_run = 0
    u_run = 0
    while True:
        _, frame = webcam.read()

        faces = face_cascade.detectMultiScale(frame, 1.3, 5)

        if faces is None:
            faces = profile_cascade.detectMultiscale(frame,1.3,5)

        if len(faces):
            cut_face = cut_faces(frame, faces)

            face = cv2.cvtColor(cut_face[0], cv2.COLOR_BGR2GRAY)
            face = cv2.equalizeHist(face)
            face = cv2.resize(face, (256, 256), interpolation = cv2.INTER_CUBIC)

            cv2.imshow('face', face)

            collector = cv2.face.StandardCollector_create()
            rec_lbhp.predict_collect(face, collector)
            conf = collector.getMinDist()

            print('Confidence ', conf)
            pred = collector.getMinLabel()
            txt = ''

            if conf < threshold:
                u_run = 0
                txt = labels_dic[pred].upper()
                k_run += 1
                if k_run>=10:
                    #motor.run_motor()
                    k_run = 0
            else:
                k_run = 0
                txt = 'Uknown'
                u_run += 1
                if u_run>=10:
                    #em.SendMail(face)
                    #sms.send()
                    print("chor aylo ")
                    u_run=0
                    webcam.release()
                    recieved()
                                
                    

            cv2.putText(frame, txt,
                        (faces[0][0], faces[0][1] - 10),
                        cv2.FONT_HERSHEY_PLAIN, 3, (66, 53, 243), 2)

            print(faces)
            cv2.rectangle(frame, (faces[0][0], faces[0][1]),(faces[0][0] + faces[0][2], faces[0][1] + faces[0][3]), (255, 255, 0), 8)#Makes rectangle around face

            cv2.putText(frame,"ESC to exit", (5, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_PLAIN, 1.3, (66, 53, 243), 2, cv2.LINE_AA)

        cv2.imshow("Live", frame)

        if cv2.waitKey(20) & 0xFF == 27:
            cv2.destroyAllWindows()
            break


# In[28]:


def delete2(e10):
    person_name = e10.get()
    folder = 'people_folder' +'/'+ person_name
    try:
        shutil.rmtree(folder)
        l8=Label(f4,text="deleted successfully",font=("arial",15,"bold"),bg="white").place(x=30,y=300)
        e10.delete(0,END)   
    except FileNotFoundError:
        print("User Does not exists")


# In[30]:


from tkinter import *
from PIL import Image,ImageTk#pip install pillow
root=Tk()
root.title("security system")
root.geometry("500x600+0+0")
strvar = StringVar(root,name="password")
#backimage = ImageTk.PhotoImage(file="background.jpeg")
#l0 = Label(root,image=backimage).place(x=350,y=0,relwidth=1,relheight=1)

#backimages = ImageTk.PhotoImage(file="kilo.jpeg")
#l1 = Label(root,image=backimages).place(x=80,y=230,width=400,height=530)

def delete():
    f4=Frame(root,bg="white")
    f4.place(x=0,y=0,width=500,height=600)
    
    l7=Label(f4,text="Enter your name",font=("arial",15,"bold"),bg="white").place(x=10,y=20)
    e4=Entry(f4,font=("arial",20))
    e4.place(x=10,y=60)
    
    b8=Button(f4,text="start",font=("arial",15,"bold"),bg="white",command=lambda: delete2(e4,f4)).place(x=50,y=120,anchor=CENTER)
 
    b9=Button(f4,text="back",font=("arial",15,"bold"),bg="white",command=show2).place(x=50,y=180,anchor=CENTER)

def password():
    f=Frame(root,bg="white").place(x=0,y=0,width=500,height=600)
    l = Label(f,text="Enter new User ID",font=("arial",15,"bold"),bg="white").place(x=10,y=20)
    e1 = Entry(f,font=("arial",20))
    e1.place(x=10,y=60)
    b=Button(f,text="change",font=("arial",15,"bold"),bg="white",command=lambda: ch_id(f,e1)).place(x=60,y=130,anchor=CENTER)
    
    l = Label(f,text="Enter new password",font=("arial",15,"bold"),bg="white").place(x=10,y=160)
    e2 = Entry(f,font=("arial",20))
    e2.place(x=10,y=200)
    b=Button(f,text="change",font=("arial",15,"bold"),bg="white",command=lambda: ch_pass(f,e2)).place(x=60,y=270,anchor=CENTER)

    Button(f,text="back",font=("arial",25,"bold"),bg="white",command=settings).place(x=230,y=370,anchor=CENTER)
        
def add_person():
    
    f3=Frame(root,bg="white")
    f3.place(x=0,y=0,width=500,height=600)
    
    l6=Label(f3,text="Enter your name",font=("arial",15,"bold"),bg="white").place(x=10,y=20)
    e3=Entry(f3,font=("arial",20))
    e3.place(x=10,y=60)
    
    b6=Button(f3,text="start",font=("arial",15,"bold"),bg="white",command=lambda: add_person2(e3)).place(x=50,y=120,anchor=CENTER)
        
    b7=Button(f3,text="back",font=("arial",15,"bold"),bg="white",command=show2).place(x=50,y=180,anchor=CENTER)

def settings():
    f5=Frame(root,bg="white").place(x=0,y=0,width=500,height=600)
    l8=Label(f5,text="Settings",font=("arial",25,"bold"),bg="white").place(x=150,y=10)
    b10=Button(f5,text="Change password and username",font=("arial",15,"bold"),bg="white",command=password).place(x=230,y=100,anchor=CENTER)
    b=Button(f5,text="back",font=("arial",25,"bold"),bg="white",command=show2).place(x=230,y=200,anchor=CENTER)
    

def quit():
    root.destroy()

def ch_id(f,id):
    file = open("password.txt","r")
    lines = file.readlines()
    file.close()
    lines[0] = id.get() + "\n"
    file = open("password.txt","w")
    file.writelines(lines)
    file.close()
    
    id.delete(0,END)
    l = Label(f,text="ID changed",font=("arial",15),bg="white")
    l.place(x=120,y=120)
    root.after(2000,l.destroy)
    
def ch_pass(f,p):
    file = open("password.txt","r")
    lines = file.readlines()
    file.close()
    lines[1] = p.get() + "\n"
    file = open("password.txt","w")
    file.writelines(lines)
    file.close()

    p.delete(0,END)
    l = Label(f,text="Password changed",font=("arial",15),bg="white")
    l.place(x=120,y=260)
    root.after(2000,l.destroy)
    
def show(e1,e2,f1):
    file1 = open("password.txt","r")
    lines = file1.readlines()
    file1.close()
    if e1.get() == lines[0].strip() and e2.get() == lines[1].strip() :
        show2()
    else:
        l5=Label(f1,text="Incorrect password. Please try again",font=("arial",12))
        l5.place(x=50,y=400)
        root.after(2000,l5.destroy)
        e1.delete(0,END)
        e2.delete(0,END)
        
def show2():
    
    f2=Frame(root,bg="white")
    f2.place(x=0,y=0,width=500,height=600)

    l5=Label(f2,text="welcome!",font=("arial",25,"bold"),bg="white").place(x=150,y=10)
    b2=Button(f2,text="add a face",font=("arial",25,"bold"),bg="white",command=add_person).place(x=230,y=100,anchor=CENTER)
    
    b3=Button(f2,text="delete face",font=("arial",25,"bold"),bg="white",command=delete).place(x=230,y=200,anchor=CENTER)
    b0=Button(f2,text="settings",font=("arial",25,"bold"),bg="white",command=settings).place(x=230,y=300,anchor=CENTER)
    b4=Button(f2,text="go live",font=("arial",25,"bold"),bg="white",command=live).place(x=230,y=400,anchor=CENTER)
    b5=Button(f2,text="exit",font=("arial",25,"bold"),bg="white",command=quit).place(x=230,y=500,anchor=CENTER)

        #b6=Button(f2,text="exit",font=("arial",25),command=exit)
    #b6.place(x=350,y=440,anchor=CENTER)    

def house():
    
    f1=Frame(root,bg="white")
    f1.place(x=0,y=0,width=500,height=600)

    l2=Label(f1,text="Login page",font=("arial",35,"bold"),bg="white",fg="green").place(x=50,y=30)

    l3=Label(f1,text="Enter your name",font=("arial",20,"bold"),bg="white",fg="black").place(x=50,y=120)
    e1=Entry(f1,font=("arial",15))
    e1.place(x=50,y=170)

    l4=Label(f1,text="Enter your password",font=("arial",20,"bold"),bg="white",fg="black").place(x=50,y=200)
    e2=Entry(f1,font=("arial",15),show="*")
    e2.place(x=50,y=240)




    b1=Button(f1,text="login",bg="white",font=("arial",20,"bold"),command=lambda: show(e1,e2,f1)).place(x=50,y=300)
    root.mainloop()
house()



# In[ ]:

#deleted msg/name doesnt exist
#



# In[ ]:





# In[ ]:
