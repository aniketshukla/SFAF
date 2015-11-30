from flask import Flask,render_template,request,session,g,redirect,url_for
from flask import abort,render_template,flash,make_response 
from flask_restful import Resource,Api
import os
import json
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
import pybrain
import warnings
import librosa
import numpy as np
with warnings.catch_warnings():
    warnings.warn("ignore")
import random
from pydub import AudioSegment



DEBUG=True
SECRET_KEY='root'
USERNAME='aniket'
PASSWORD='root'
FNN_PATH='../train.xml'
app=Flask(__name__)
api=Api(app)
app.debug=True
FNN_PATH='../train.xml'

def mapper(mfcc):
	return mfcc[-1292:]


@app.route('/')
def adder():
	return render_template('booga.html')




@app.route('/sent',methods=['POST'])
def getSent():
	voice=request.files['file']
	format_audio=request.form['audio_format']
	name=str(random.randint(1,200000))
	path=name+voice.filename
	voice.save(name+voice.filename)
	temp=exec("AudioSegment.from_"+str(format_audio)+"("+path+")")
	temp.export("path"+str(1),format="mp3",bitrate="64k")
	y,sr=librosa.load(path+str(1))
	os.remove(path)
	os.remove(path+str(1))
	print('y sr computed')
	mfcc=librosa.feature.mfcc(y=y,sr=sr,n_mfcc=13)
	mfcc=np.array(map(mapper,mfcc))
	mfcc=mfcc.max(axis=0)
	fnn=NetworkReader.readFrom(FNN_PATH)
	fnn=fnn.activate(mfcc)
	max_index=0
	max_value=fnn[0]
	for foo in range(1,len(fnn)):
		if fnn[foo]>max:
			max_index=foo
			max_value=fnn[foo]
	if max_index==0:
		return "{emotion:Happy}"
	elif max_index==1:
		return "{emotion:Angry}"







		


if __name__=='__main__':
	app.run()


