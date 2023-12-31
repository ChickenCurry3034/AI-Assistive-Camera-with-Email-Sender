import streamlit as st
import cv2
import time
from PIL import Image
import numpy as np
from email.message import EmailMessage
import ssl
import smtplib

cap = cv2.VideoCapture(0)

frameST = st.empty()

#Initializing the face and eye cascade classifiers from xml files
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

#Variable store execution state
first_read = True

#Starting the video capture
ret,img = cap.read()

frameST1 = st.empty()
camClick = frameST1.button('Ready to Take Picture!')

check = False

contrast = st.sidebar.slider("Contrast", 0, 10)
brightness = st.sidebar.slider("Brightness",0,100)
graychecker = st.sidebar.checkbox('Grayscale?')

while(check == False):
        ret,img = cap.read()
	#Converting the recorded image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#Applying filter to remove impurities
        gray = cv2.bilateralFilter(gray,5,1,1)

	#Detecting the face for region of image to be fed to eye classifier
        faces = face_cascade.detectMultiScale(gray, 1.3, 5,minSize=(50,50))
        if(len(faces)>0):
                for (x,y,w,h) in faces:
                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                        
                        #roi_face is face which is input to eye classifier
                        roi_face = gray[y:y+h,x:x+w]
                        roi_face_clr = img[y:y+h,x:x+w]
                        eyes = eye_cascade.detectMultiScale(roi_face,1.1,2,minSize=(50,50))

			#Examining the length of eyes object for eyes
                        if(len(eyes)>=2):
                        	#Check if program is running for detection 
                        	if(first_read):
                        		cv2.putText(img, 
                        		"Eye detected", 
                        		(50,50), 
                        		cv2.FONT_HERSHEY_DUPLEX, 1,
                        		(0,255,0),2)
                        		if(camClick):
                                                check = True
                                                break
                                                
                        else:
                        	if(first_read):
                        		#To ensure if the eyes are present before starting
                        		cv2.putText(img, 
                        		"No eyes detected", (50,50),
                        		cv2.FONT_HERSHEY_DUPLEX, 1,
                        		(0,0,255),2)
                        
                        
        else:
        	cv2.putText(img,
        	"No face detected",(50,50),
        	cv2.FONT_HERSHEY_DUPLEX, 1,(0,0,255),2)
			
        cv2.imshow('img',img)
        out = cv2.addWeighted( img, contrast, img, 0, brightness)
        if(graychecker):
                out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
                frameST.image(out)
        else:
                frameST.image(out,channels="BGR")

ret,img = cap.read()
frameST.image(out, channels="BGR")
frameST1.empty()

email_password = st.text_input('What is your app password?',type="password")
email_receiver = st.text_input('Which email is this going to?')
subject = st.text_input('Insert Subject')
body = st.text_input('Insert Body')
send_mail = st.button('Send Email')
if send_mail:
        em=EmailMessage()
        em['From']='aarushmane@gmail.com'
        em['To']=email_receiver
        em['subject']=subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login('aarushmane@gmail.com',email_password)
                smtp.sendmail('aarushmane@gmail.com',email_receiver,em.as_string())
