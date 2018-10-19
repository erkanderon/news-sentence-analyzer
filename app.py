from flask import Flask, render_template, request, send_file
from .crawler import *
import json

app = Flask(__name__, static_folder="files")

datas = get_datas()

@app.route('/')
def get_func():
	return render_template("index.html", data = datas)

@app.route('/download', methods=['POST'])
def get_down():

	folia_creator('username',json.loads(request.form['val']), 'user_selections.xml')
	try:
		#return send_file('./files/user_selections.xml', attachment_filename="user_selections.xml", as_attachment="True")
		return redirect("/files/user_selections.xml")
	except Exception as e:
		return str(e)
	#for i in request.args:
	#	print(request.args[i])
	#return render_template("index.html", data = datas)


@app.route('/files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
	return send_file('./files/user_selections.xml', attachment_filename="user_selections.xml", as_attachment="True", add_etags=False)    
    #return send_from_directory(directory='files', filename=filename)