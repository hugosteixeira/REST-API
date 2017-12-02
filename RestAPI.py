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


@app.route('/registrarUsuario', methods=['POST'])
def registrarUsuario():
    if request.method == 'POST':  
        json = request.get_json()
        idUsuario = inserirUsuario(json)
        
        if (idUsuario):
            return jsonify({'Resposta' : {"Id_Usuario":str(idUsuario)}})
        else:
            return jsonify({'Error' : 'Não foi possivel cadastar'})

@app.route('/verificarUsuarioCadastrado', methods=['POST'])
def verificarUsuario():
    if request.method == 'POST':  
        json = request.get_json()
        idUsuario = verificarUsuarioCadastrado(json)
        
        if (idUsuario):
            return jsonify({'Resposta' : {"Id_Usuario":str(idUsuario)}})
        else:
            return jsonify({'Resposta' : 0})


@app.route('/registrarAlerta', methods=['POST'])
def registrarAlerta():
    if request.method == 'POST':  
        json = request.get_json()
        idAlerta = inserirAlerta(json)
        
        if (idAlerta):
            return jsonify({'Resposta' : {"Id_Alerta":str(idAlerta)}})
        else:
            return jsonify({'Error' : 'Não foi possivel cadastar'})

@app.route('/registrarGrupo', methods=['POST'])
def registrarGrupo():
    if request.method == 'POST':  
        json = request.get_json()
        idGrupo = inserirGrupo(json)
        
        if (idGrupo):
            return jsonify({'Resposta' : {"Id_Grupo":str(idGrupo)}})
        else:
            return jsonify({'Error' : 'Não foi possivel cadastar'})

@app.route('/getTodosGrupos', methods=['GET'])
def pegarTodosGrupos():
    if request.method == 'GET':
        resp = getTodosGrupos ()
        if (resp):
            
            return jsonify(resp)
        else:
            return jsonify({'error' : 'Não foi possivel listar grupos'})
        



if __name__ == '__main__' :
    app.run()

