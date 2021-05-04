from flask import Flask
from flask import render_template, redirect, url_for
from flask import request, Response


from imutils.video import VideoStream

import cv2
import os
import time
import imutils

app = Flask(__name__)



#Inicializamos Pagina en index
@app.route("/")

def index():
   
    return render_template("index.html")

#Funcion para el administrador Se pienza darle opciones de entrenar el modelo y conservar los datos.
@app.route("/Administrador")
def fnAdmin():
    return 'Hola Administrador'

# Definimos una ruta para el Invitado Este usuario se verifica en list
@app.route('/invitado/<nInvitado>')
def fnInvitado(nInvitado):     
    pack='Base/'
    archivo= os.listdir(pack)

    if nInvitado in archivo:
        print('usuario valido proceda a login facial')
        print('Hola %s!! identificamos tu usuario por favor proceda  a LOGIN FACIAL' % nInvitado) 
        return redirect(url_for('index'))  
    else:
        print('no encontrado por favor registrarse')
        print ('Hola %s !! No identificamos tu usuario, por favor REGISTRESE' % nInvitado)
        #return redirect(url_for('registro'))
        return redirect(url_for('fnRegistro',user = nInvitado))
        #return Response(generateFrames(nInvitado), mimetype='multipart/x-mixed-replace; boundary=frame')


#Funcion registro
@app.route("/registro/<user>")
def fnRegistro(user):
    print(user)    
    
    return Response(generateFrames(user), mimetype='multipart/x-mixed-replace; boundary=frame')
    VideoStream.stop()  


#Funcion para servicio login
@app.route("/servicio",methods=['POST', 'GET'])
def servicio():
      # Verifico que metodo es
    if request.method == 'POST':
        # Obtiene el Usuario
        usuario = request.form['nombre']
        print("Usando POST ...")
        print(usuario)
    else:
        # Obtiene el Usuario
        usuario = request.args.get("nombre")
        print("Usando GET ...")
        print(usuario)
    # Se compara
       
    if (usuario=="Einer"):
        return redirect(url_for('fnAdmin'))
    else:
        return redirect(url_for('fnInvitado',nInvitado = usuario))



##Funcion para proyectar video y registar imagenes.
def generateFrames(user):
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    videoStream = VideoStream(src=0).start()
    
    usuario=user
    folder="Base"
    folderUsuario=folder+'/'+usuario
    if not os.path.exists(folderUsuario):
        os.makedirs(folderUsuario)
    count=0
    while True:

        frame = videoStream.read()
        frame = imutils.resize(frame, width=600)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()
        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:

            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(folderUsuario+'/rostro_{}.jpg'.format(count),rostro)
            count = count +1
            #frame = cv2.imencode('.jpg', frame)[1].tobytes()
            cv2.rectangle(frame,(10,5),(450,25),(255,255,255),-1)
            cv2.putText(frame,'Registrando rostro por favor no se mueva.. un momento',(10,20), 2, 0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.imshow('frame',frame)              

        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

        time.sleep(0.05)

        if count >= 20:
	        break
            

if __name__=="__main__":
    app.run(debug = True)


    
