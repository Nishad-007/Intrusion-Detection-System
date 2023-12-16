import numpy as np
import tkinter as tk
import customtkinter as ctk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint
from sklearn.preprocessing import StandardScaler
import joblib
from PIL import Image, ImageTk



#-----------------------------------------------GUI-----------------------------------------------------------------------

root = ctk.CTk()
root.state('zoomed')

img1 = ImageTk.PhotoImage(Image.open("pattern.png"))
l1= ctk.CTkLabel(master=root,image = img1)
l1.pack()


frame = ctk.CTkFrame(root,width=290,height=400,border_color="white",border_width=1)
frame.place(x=115,y=180)

frame2 = ctk.CTkFrame(root,width=900,height=400, border_color="white",border_width=1)
frame2.place(x=450,y=180)

frame3 = ctk.CTkFrame(root,width=1000,height=100,border_color="white",border_width=1)
frame3.place(x=250,y=50)

frame4 = ctk.CTkFrame(root,width=900,height=400,border_color="white",border_width=1)
#frame4.place(x=980,y=150) 
frame4.place(x=450,y=180)

frame5= ctk.CTkFrame(root,width=900,height=400, border_color="white",border_width=1)
frame5.place(x=450,y=180)

head = ctk.CTkLabel(frame3,text = "DDOS ATTACK DETECTION SYSTEM",font = ("Lucida Sans Typewriter",40,'bold'), corner_radius=6)
head.place(x=50,y=20)

#-----------------------------------------------Training Dataset-----------------------------------------------------------------


ddos_dataset = pd.read_csv('E:/DDOS Attack 27 Feb 2023/DDOS Attack/CICIDpreprocessing.csv')
ddos_dataset.drop(["Src IP","Src Port","Dst IP","Flow ID","Protocol","Timestamp"], axis=1, inplace = True)


X = ddos_dataset.drop(columns = "Label", axis=1)
Y = ddos_dataset["Label"]


#------------------------------------------Random Forest Classifier------------------------------------------------------------------------------

def RF():
    
    frame4.tkraise();
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.3, stratify=Y, random_state=2)
    RFC_spyder_Classifier = RandomForestClassifier(max_depth=40)
    RFC_spyder_Classifier.fit(X_train, Y_train)



    X_train_prediction = RFC_spyder_Classifier.predict(X_train)
    
    training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
    print('Accuracy score of the training data : ', training_data_accuracy)
    
    X_test_prediction = RFC_spyder_Classifier.predict(X_test)
    
    test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
    print('Accuracy score of the testing data : ', test_data_accuracy)
    
    classrepo= ctk.CTkLabel(frame4,text ="Classification report ",width=35,font=("Bahnschrift Light",27,"bold"))
    classrepo.place(x=75,y=85)
    
    label4 = ctk.CTkLabel(frame4,text ="training_data_accuracy : "+str(training_data_accuracy),font=("Tempus Sanc ITC",15))
    label4.place(x=95,y=135)
            
    label5 = ctk.CTkLabel(frame4,text ="test_data_accuracy : "+str(test_data_accuracy),width=35,height=3,font=("Tempus Sanc ITC",16))
    label5.place(x=95,y=165)
    
    joblib.dump(RFC_spyder_Classifier,"RFC_spyder_Classifier.joblib")
    
    

#-----------------------------------------------Test Function-----------------------------------------------------------------


def ok():
    
    frame2.tkraise();    
    rf = joblib.load('RFC_spyder_Classifier.joblib')
    
    from tkinter.filedialog import askopenfilename
    
    fileName = askopenfilename(initialdir='E:/DDOS Attack 27 Feb 2023/DDOS Attack', title='Select DataFile For INTRUSION Testing',
                                        filetypes=[("all files", "*.csv*")])
    
    file =pd.read_csv(fileName)
    file.drop(["Src IP","Src Port","Dst IP","Flow ID","Protocol","Timestamp"], axis=1, inplace = True)
    file.drop(columns = "Label", axis=1,inplace=True)
    # input_data = (80,7,0,2,0,0,0,0,0,0,0,0,0,0,0,285714.2857,7,0,7,7,0,0,0,0,0,7,7,0,7,7,0,0,0,0,0,40,0,285714.2857,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,-1,0,0,0,0,0,0,0,0,0,0,0)
   
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(file)
    
    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    
    prediction = rf.predict(input_data_reshaped)
    print(prediction)
    
    if (prediction[0] == "BENIGN"):
      # print('normal')
        frame2.tkraise();
        output = 'DDOS Attack Not Detected'
        frame2.configure(fg_color = 'green')
        
        attack = ctk.CTkLabel(frame2,text=str(output),width=30,font = ("Roboto",40,'bold'))
        attack.place(x=220,y=180)
    else:
      # print('DDoS')
        frame5.tkraise()
        output = 'DDOS Attack Detected'
        frame5.configure(fg_color = 'red')
        attack = ctk.CTkLabel(frame5,text=str(output),width=30,font = ("Roboto",40,'bold'))
        attack.place(x=220,y=180) 

def EXIT():
    root.destroy()


#-----------------------------------------------Button UI-----------------------------------------------------------------

button1 = ctk.CTkButton(frame,command= ok,text="TEST",width=210,corner_radius=6,fg_color="blue", font=("Roboto",10,"bold"))
button1.place(x=35,y=150)

button2 = ctk.CTkButton(frame,command= RF,text="TRAIN",width=210,corner_radius=6,fg_color="blue", font=("Roboto",10,"bold"))
button2.place(x=35,y=200)

button3 = ctk.CTkButton(frame,command=EXIT,text="EXIT",width=210,corner_radius=6,fg_color="yellow",font=("Roboto",10,"bold"))
button3.place(x=35,y=250)


root.mainloop()
