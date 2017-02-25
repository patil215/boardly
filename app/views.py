from flask import redirect, render_template, render_template_string, Blueprint
from flask import request, url_for, flash, Response, jsonify
import time
from app.init_app import app
import random


@app.route("/")
def home_page():
    return render_template('pages/home_page.html')
