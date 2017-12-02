# coding=utf-8
from flask import Flask, jsonify, request
import requests
from flaskext.mysql import MySQL
from flask_cors import CORS
from DB.DB_helper import *

INIT_API()

app = Flask(__name__)
mysql = MySQL()
CORS(app)
mysql.init_app(app)


@app.route('/registrarusuario', methods=['POST'])
def registrarUsuario():
    if request.method == 'POST':  
        json = request.get_json()
        idUsuario = inserirUsuario(json)
        
        if (idUsuario):
            return str(idUsuario)
        else:
            return str('ERROR')

@app.route('/verificarUsuarioCadastrado', methods=['POST'])
def verificarUsuario():
    if request.method == 'POST':  
        json = request.get_json()
        idUsuario = verificarUsuarioCadastrado(json)
        
        if (idUsuario):
            return str(idUsuario)
        else:
            return str('ERROR')


@app.route('/registrarAlerta', methods=['POST'])
def registrarAlerta():
    if request.method == 'POST':  
        json = request.get_json()
        idAlerta = inserirAlerta(json)
        
        if (idAlerta):
            return str(idAlerta)
        else:
            return str('ERROR')

@app.route('/registrarGrupo', methods=['POST'])
def registrarGrupo():
    if request.method == 'POST':  
        json = request.get_json()
        idGrupo = inserirGrupo(json)
        
        if (idGrupo):
            return str(idGrupo)
        else:
            return str('ERROR')

@app.route('/getTodosGrupos', methods=['GET'])
def pegarTodosGrupos():
    if request.method == 'GET':
        resp = getTodosGrupos ()
        if (resp):
            
            return jsonify(resp)
        else:
            return str('ERROR')
        

@app.route('/login',methods=['POST'])
def login_company():
    if request.method == 'POST':
        json_login = request.get_json()
        print(json_login)
        usuario = getUsuario (json_login)
        if (usuario):
            
            return str(usuario)
        else:
            return str('ERROR')
        


if __name__ == '__main__' :
    app.run(host="10.98.1.107")

