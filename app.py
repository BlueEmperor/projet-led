from flask import Flask, jsonify, request, render_template
import board
from neopixel import NeoPixel
from time import sleep
from threading import Thread

pixels=NeoPixel(board.D18,60,auto_write=False)
fps=60
led_nb=60

class led:
    def __init__(self):
        self.state=True
        self.color=[0,0,0]
        self.mode=1
        self.lock=False
        self.roue=0

l=led()

def rgb(color, a):
    if(color[0]==255 and color[1]<255 and color[2]==0):
        color[1]+=a
    elif(color[0]>0 and color[1]==255):
        color[0]-=a
    elif(color[1]==255 and color[2]<255):
        color[2]+=a
    elif(color[1]>0 and color[2]==255):
        color[1]-=a
    elif(color[2]==255 and color[0]<255):
        color[0]+=a
    elif(color[2]>0 and color[0]==255):
        color[2]-=a
    for i in range(3):
        if(color[i]>255):
            color[i]=255
        elif(color[i]<0):
            color[i]=0
    return(color)

def update():
    while(True):
        if(l.state):
            if(l.mode=="unicolore"):
                for i in range(led_nb):
                    pixels[i]=l.color

            elif(l.mode=="rainbow"):
                l.color=rgb(l.color,32)
                pixels[0]=l.color
                for i in range(1,led_nb):
                    pixels[led_nb-i]=pixels[led_nb-i-1]

            elif(l.mode=="jaune rouge"):
                l.roue+=1
                if(0<=l.roue<10):
                    l.color=[0,0,0]
                elif(10<=l.roue<12):
                    l.color=[0,150,255]
                else:
                    l.roue=0
                    l.color=[0,0,0]
                pixels[0]=l.color
                for i in range(1,led_nb):
                    pixels[led_nb-i]=pixels[led_nb-i-1]

            if(not(l.lock)):
                pixels.show()
                    
        else:
            for i in range(led_nb):
                pixels[i]=[0,0,0]
            pixels.show()
    
        sleep(1/fps)
        
app = Flask(__name__)

@app.route('/')
def main():
    return(render_template('index.html'))

@app.route('/switch', methods=['GET'])
def switch():
    status = request.args.get('status')

    if(status == "off"):
        l.state=False
        l.lock=False

    elif(status == "on"):
        l.state=True
    
    return(jsonify({"message":"switch"}))

@app.route('/lock', methods=['GET'])
def lock():
    status = request.args.get('status')
    
    if(status == "off"):
        l.lock=False

    elif(status == "on"):
        l.lock=True

    return(jsonify({"message":"lock"}))

@app.route('/color', methods=['GET'])
def color():
    color = request.args.get('color')

    r=int(color[0:2],base=16)
    g=int(color[2:4],base=16)
    b=int(color[4:6],base=16)
    l.color=[r,g,b]
    l.mode="unicolore"

    return(jsonify({"message":"color"}))

@app.route('/script', methods=['GET'])
def script():
    script = request.args.get('script')
    if(script=="stop"):
        l.mode="unicolore"
    l.color=[255,0,0]
    l.mode=script
    
    return(jsonify({"message":"script"}))

th = Thread(target=update)
th.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)