import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask,render_template,request
from twilio.rest import Client

app=Flask(__name__)

model=load_model("Forest_fire.h5")
def send_message():
  account_sid = 'AC4c6802dceef3f53e86d8f323381b6e9f' 
  auth_token = 'c07d05d7550d4902a879db6160b7f39c' 
  client = Client(account_sid, auth_token) 
 
  message = client.messages.create(  
                              messaging_service_sid='MG39f0273fc2caf682130af0fe591f15ca', 
                              body='forest_fire',      
                              to='+918925643320' 
                          ) 
 
  print(message.sid)
   
  print("Fire Detected")
  print("SMS Sent")
  
@app.route('/')
def index():
    return render_template("index.html")
text=''
@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f=request.files['image']
        basepath=os.path.dirname(__file__)
        filepath=os.path.join(basepath,'uploads',f.filename)
        f.save(filepath)
        img=image.load_img(filepath,target_size=(150,150))
        x=image.img_to_array(img)
        x = np.expand_dims(x,axis=0)
        pred = (model.predict(x))
        if(pred==0):
            send_message()
            
            text='FIRE DETECTED AND SMS TRIGGERED TO RESPECTIVE NUMBER'
        else:
            
            text='NO FIRE'
    return text 
if __name__=='__main__':
    app.run(debug=False)