from flask import Flask
from flask import render_template, redirect, url_for,flash
from flask import request, Response

import cv2
import os
import time
import imutils
import numpy as np
from imutils.video import VideoStream

app = Flask(__name__)


faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
videoStream = VideoStream(src=0).start()
#frameCapt = cv2.VideoCapture(src=0,cv2.CAP_DSHOW)
#frameCapt = cv2.VideoCapture(0)
#Inicializamos Pagina en index
@app.route("/")

def index():
   
    return render_template("index.html")

#Funcion para el administrador Se pienza darle opciones de entrenar el modelo y conservar los datos.
@app.route("/Administrador")
def fnAdmin():
    return 'Hola Administrador'


# Definimos una ruta para el Invitado Este usuario se verifica en list
@app.route('/<nInvitado>/<Accion>')
def fnInvitado(nInvitado, Accion,methods=["GET", "POST"]):     
    
    print("Invitado")
    print(nInvitado)
    print(Accion)
 
    pack='Base/'
    archivo= os.listdir(pack)

    if nInvitado in archivo and Accion=='Login':
               
        print('usuario valido proceda a login facial')
        print('Hola %s!! identificamos tu usuario por favor proceda  a LOGIN FACIAL' % nInvitado)
        return redirect(url_for('logue',user = nInvitado))
        #Redirigir llamar funcion de login y comparar
        #return redirect(url_for('index'))  
        #return 'LOGIN USUARIO YA REGISTRADO'
    if nInvitado in archivo and Accion=='LoginFacial':
               
        print('Procediendo a LOGINFACIAL')
        print('Hola %s!! identificamos tu usuario por favor proceda  a LOGIN FACIAL' % nInvitado)
        #return redirect(url_for('RecFacial'))
        return redirect(url_for('RecFacial',user = nInvitado))

    if nInvitado in archivo and Accion=='Registrar':
        print('no encontrado por favor registrarse')        
        print ('Hola %s !! No identificamos tu usuario, por favor REGISTRESE' % nInvitado)
        return 'USUARIO YA REGISTRADO INTENTE CON OTRO NOMBRE DE USUARIO'
             #return redirect(url_for('registro'))
            #return redirect(url_for('fnRegistro',user = nInvitado))
             #return Response(generateFrames(nInvitado), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    
    if not nInvitado in archivo and Accion=='Registrar':   
        #return redirect(url_for('index'))
        print('REGISTRANDO')
        return redirect(url_for('fnRegistro',user = nInvitado))
    
    if not nInvitado in archivo and Accion=='Login':   
        #return redirect(url_for('index'))
        return('USUARIO NO ENCONTRADO POR FAVOR REGISTRAR')
        #return redirect(url_for('fnRegistro',user = nInvitado))
                


@app.route("/logeo",methods=["GET", "POST"])
def logeo():
    if "login" in request.form():
        print("login")
        return redirect(url_for('index'))
    if "reg" in request.form():
        print("Regis")
        return redirect(url_for('index'))
    
#Funcion registro
@app.route("/<user>")
def fnRegistro(user):
    print(user)    
    return Response(generateFrames(user,'reg'), mimetype='multipart/x-mixed-replace; boundary=frame')
    

#Funcion para servicio login
@app.route("/servicio",methods=['POST', 'GET'])
def servicio():
      # Verifico que metodo es
    if request.method == 'POST':
        # Obtiene el Usuario
        usuario = request.form['nombre']
        boton = request.form['botn']
        print("Usando POST ...")
        print(usuario)
        print(boton)

    else:
        # Obtiene el Usuario
        usuario = request.args.get("nombre")
        print("Usando GET ...")
        print(usuario)
    # Se compara
       
    if (usuario=="Einer"):
        return redirect(url_for('fnAdmin'))
    else:
        return redirect(url_for('fnInvitado',nInvitado = usuario, Accion = boton))


##Funcion para proyectar video y registar imagenes.

def generateFrames(user,registro):
    print('gfram')
    print(registro)
    R=registro 
    usuario=user
    folder="Base"
    #frameCapt = cv2.VideoCapture(0)
    print(usuario)
        
    folderUsuario=folder+'/'+usuario
    
    if not os.path.exists('Reciente'):
        os.makedirs('Reciente')
    
    if usuario =='fnRegistro'or usuario=='favicon.ico':
        folder='Reg'
        folderUsuario=folder+'/'+usuario
        if not os.path.exists(folderUsuario):
            os.makedirs(folderUsuario)
    else:
        folder='Base'  
    
    folderUsuario=folder+'/'+usuario          
    if not os.path.exists(folderUsuario):
        os.makedirs(folderUsuario)
        print('se crea folder')
        print(folderUsuario)
    count=0
    contReci=0
    
    while True:
        
        #ret,frame = frameCapt.read()
        frame = videoStream.read()
        frame = imutils.resize(frame, width=600,height=400, conts=3)
        #(w, h, c) = frame.shape
        #syntax: cv2.resize(img, (width, height))
        #frame = cv2.resize(frame,(400, h))
        #print(w, h)
        #print(frame.shape)        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)        
        auxFrame = frame.copy()
        faces = faceClassif.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:

            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150), interpolation=cv2.INTER_CUBIC)                          
            
            
            if usuario!='fnRegistro' and count<=50:
                #cv2.imwrite(folderUsuario+'/rostro_{}.jpg'.format(count),rostro)
                #count = count +1
                if usuario!='favicon.ico' and count<=50:
                    cv2.imwrite(folderUsuario+'/rostro_{}.jpg'.format(count),rostro)
                    count = count +1

            #frame = cv2.imencode('.jpg', frame)[1].tobytes()
            cv2.rectangle(frame,(10,5),(450,25),(255,255,255),-1)
            cv2.putText(frame,'Rostro detectado... Por favor ingrese su usuario',(10,20), 2, 0.5,(0,0,0),1,cv2.LINE_AA)
            while contReci<3:
                cv2.imwrite('Reciente'+'/rostroAct_{}.jpg'.format(contReci),rostro)
                contReci= contReci+1
            contReci=0
            #cv2.imshow('frame',frame)              

        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

        time.sleep(0.05)
        
        if count>=50 and R=='reg':
            
            print('USUARIO REGISTRADO')
            break   
    #frameCapt.release()        
        
    dataPath = 'Base' #Cambia a la ruta donde hayas almacenado Data
    peopleList = os.listdir(dataPath)
    print('Lista de personas: ', peopleList)

    labels = []
    facesData = []
    label = 0

    for nameDir in peopleList:
        personPath = dataPath + '/' + nameDir
        print('Leyendo las imágenes')

        for fileName in os.listdir(personPath):
            print('Rostros: ', nameDir + '/' + fileName)
            labels.append(label)
            facesData.append(cv2.imread(personPath+'/'+fileName,0))
    
    
        label = label + 1

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    print("Entrenando...")
    face_recognizer.train(facesData, np.array(labels))
    face_recognizer.write('modelo/modeloLBPHFace.xml')
    print("Modelo almacenado...")

#funcion para comparar con LBPHFACE
@app.route("/machine/<user>",methods=["POST", "GET"])
def RecFacial(user):
    invi=user
    
    dataPath = 'Base' #Cambia a la ruta donde hayas almacenado Data
    imagePaths = os.listdir(dataPath)
    print('reconociendo rostro %s' %invi)
    print('imagePaths=',imagePaths) 
    
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('modelo/modeloLBPHFace.xml')
    
    img = cv2.imread("Reciente/rostroAct_0.jpg")
    img = cv2.resize(img,(150,150),interpolation= cv2.INTER_CUBIC)
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    auxFrame = gray.copy()       
           
    result = face_recognizer.predict(auxFrame)
        
    print('Resultado',result)
         
    print(imagePaths[result[0]])
    if result[1] < 80 and imagePaths[result[0]]==invi:  
          
        invitado=imagePaths[result[0]]

        return('Bienvenido %s a nuestra plataforma' %invitado)      
    else:
        print('Desconocido')
        return('No se logra detectar tu rostro intentalo de nuevo')
    
 
#logueo
@app.route('/logue/<user>',methods=['POST', 'GET'])
def logue(user):    
    """Video streaming home page.""" 
    print('Logue %s'% user)

    return render_template('log.html')    
    
def gen():
    """Video streaming generator function."""
    #cap = cv2.VideoCapture('768x576.avi')
    dataPath = 'Base' #Cambia a la ruta donde hayas almacenado Data
    imagePaths = os.listdir(dataPath)
    print('imagePathsGen=',imagePaths) 
          
    img = cv2.imread("Reciente/rostroAct_0.jpg")
    img = cv2.resize(img,(150,150),interpolation= cv2.INTER_CUBIC)
    frame = cv2.imencode('.jpg', img)[1].tobytes()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    

@app.route('/img_feed')
def img_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')    
    
    

if __name__=="__main__":
    app.run()


    
