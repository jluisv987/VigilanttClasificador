from flask import Blueprint, jsonify, redirect, url_for, request

views = Blueprint(__name__,"views")

@views.route("/")
def home():
    return "home page"

@views.route("/clasificar",methods=['POST','GET'])
def clasificar():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        print(content) # Do your processing
        return jsonify({'id':'123','incidencias':'5'})
