# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 08:31:08 2019

@author: Admin
"""

import pygal
import MySQLdb
from flask import Flask, render_template, redirect, url_for, request, jsonify
import json

from flask_wtf import Form
from wtforms import SelectField, SubmitField



def dbConnect():
    host = "127.0.0.1"
    user = "root"
    password = "root"
    dbName = "smartcity"
    con = MySQLdb.connect (host = host, user = user, passwd = password, db = dbName)
    return con

def closeCon(con, cursor):
    cursor.close()
    con.close()

def get_parameters_names():
    
    con = dbConnect()
    cursor = con.cursor()
    query = "SELECT DISTINCT REPLACE(UPPER(parameter),'_',' ') FROM smartcity.5_parameters;"
    cursor.execute (query)
    # fetch a single row using fetchone() method.
    rows = cursor.fetchall()
    parameter_names_list = [i[0] for i in rows]
    return parameter_names_list

def get_11_parameters_names():
    con = dbConnect()
    cursor = con.cursor()
    query = "SELECT DISTINCT REPLACE(UPPER(parameter),'_',' ') FROM smartcity.11_parameters;"
    cursor.execute (query)
    # fetch a single row using fetchone() method.
    rows = cursor.fetchall()
    parameter_names_list = [i[0] for i in rows]
    return parameter_names_list
    
    
def get_city_names():
    
    con = dbConnect()
    cursor = con.cursor()
    query = "SELECT DISTINCT UPPER(city) FROM smartcity.5_parameters;"
    cursor.execute (query)
    # fetch a single row using fetchone() method.
    rows = cursor.fetchall()
  
    city_names_list = [(i[0],i[0].upper()) for i in rows]
    return city_names_list

def get_11_city_names():
    
    con = dbConnect()
    cursor = con.cursor()
    query = "SELECT DISTINCT UPPER(city) FROM smartcity.11_parameters;"
    cursor.execute (query)
    # fetch a single row using fetchone() method.
    rows = cursor.fetchall()
  
    city_names_list = [(i[0],i[0].upper()) for i in rows]
    return city_names_list

def get_value_for_city(city_name):
    
    con = dbConnect()
    cursor = con.cursor()
    query = "SELECT value FROM smartcity.5_parameters WHERE city='{}'".format(city_name)
    cursor.execute (query)
    # fetch a single row using fetchone() method.
    rows = cursor.fetchall()
  
    city_names_list = [i[0] for i in rows]
    return city_names_list

def get_11_value_for_city(city_name):
    
    con = dbConnect()
    cursor = con.cursor()
    query = "SELECT value FROM smartcity.11_parameters WHERE city='{}'".format(city_name)
    cursor.execute (query)
    # fetch a single row using fetchone() method.
    rows = cursor.fetchall()
  
    city_names_list = [i[0] for i in rows]
    return city_names_list

def get_data_by_city_parameter(city_name, parameter_name):
    
    con = dbConnect()
    cursor = con.cursor()
    query = "SELECT value FROM smartcity.11_parameters WHERE city='{}' AND parameter='{}'".format(city_name, parameter_name)
    cursor.execute (query)
    # fetch a single row using fetchone() method.
    rows = cursor.fetchall()
  
    city_names_list = [i[0] for i in rows]
    return city_names_list

def get_city_and_value(city_name):
    
    con = dbConnect()
    cursor = con.cursor()
    query = "SELECT value, parameter FROM smartcity.11_parameters WHERE city='{}'".format(city_name)
    cursor.execute (query)
    # fetch a single row using fetchone() method.
    rows = cursor.fetchall()
  
    city_names_list = [i[0] for i in rows]
    return city_names_list
    
def get_5_parameter_data_by_city(city_name):
  
    con = dbConnect()
    cursor = con.cursor()
    query = "SELECT UPPER(parameter), value FROM smartcity.5_parameters WHERE city='{}'".format(city_name)
    cursor.execute (query)
    # fetch a single row using fetchone() method.
    rows = cursor.fetchall()
  
    #city_names_list = [i[0] for i in rows]
    temp_dict = {}
    overall = 0
    for row in rows:
      print(row[0])
      temp_dict["CITY"] = city_name.upper()
      temp_dict[row[0]] = row[1]
      overall += row[1]
    temp_dict['OVERALL'] = "{0:.2f}".format(overall/5)
    return temp_dict
  
class benchmark_form(Form):
    
    city_names_list = get_city_names()
    
    city1 = SelectField("City Name 1", choices=city_names_list)
    city2 = SelectField("City Name 2", choices=city_names_list)
    submit = SubmitField("Send")

class city_profile_form(Form):
    
    city_names_list = get_city_names()
    
    city = SelectField("City Name", choices=city_names_list)
    submit = SubmitField("Send")

app = Flask(__name__, template_folder='templates')
app.secret_key = 'development key'

@app.route('/get_ranking_data')
def get_ranking_data():
  # Assume data comes from somewhere else
  
  data_list = []
  
  for city_name in get_city_names():
    data_dict = get_5_parameter_data_by_city(city_name[0].lower())
    data_list.append(data_dict)
    print(data_list)
  data = {
    "data": data_list
  }
  return jsonify(data)

@app.route('/why_smart_cities', methods = ['POST', 'GET'])
def why_smart_cities():
  
  return render_template("why_smart_cities.html")

@app.route('/smart_cities_model', methods = ['POST', 'GET'])
def smart_cities_model():
  
  return render_template("smart_cities_model.html")

@app.route('/benchmark', methods = ['POST', 'GET'])
def benchmark():
  form = benchmark_form()
  print(request.method)
  render_data = []

  if request.method == 'POST':
  
      city1 = request.form['city1']
      city2 = request.form['city2']
      
      line_chart = pygal.Bar()
      line_chart.title = city1.upper() + " Vs " + city2.upper()
      line_chart.x_labels = get_parameters_names()
      
      city1Values = get_value_for_city(city1)
      city2Values = get_value_for_city(city2)
      
      line_chart.add(city1, city1Values)
      line_chart.add(city2, city2Values)
      
      '''
      radar_chart = pygal.Radar()
      radar_chart.title = city1.upper() + " Vs " + city2.upper()
      
      city1Values = get_value_for_city(city1)
      city2Values = get_value_for_city(city2)
      
      radar_chart.x_labels = get_parameters_names()
      radar_chart.add(city1, city1Values)
      radar_chart.add(city2, city2Values)
      '''
      
      render_data.append(line_chart.render_data_uri())
      
  return render_template("benchmark.html", form=form, render_data=render_data)

@app.route('/city_profile', methods = ['POST', 'GET'])
def city_profile():
    
  form = city_profile_form()
  print(request.method)
  render_data = []
  overall_graph_data = []
  print(request)
  if request.method == 'POST':
      
      cityName = request.form['city']
      print(cityName)
      values = get_city_and_value(cityName)
      names = get_11_parameters_names()
      bar_chart = pygal.HorizontalStackedBar()
      bar_chart.title = cityName
      bar_chart.x_labels = map(str, names)
      bar_chart.add("", values)
      overall_graph_data = bar_chart.render_data_uri()
    
      parameters_names = get_11_parameters_names()
    
      render_data = []
    
      for majorParameterName in parameters_names:
        values1 = get_data_by_city_parameter(cityName, majorParameterName)
        bar_chart = pygal.HorizontalStackedBar()
        bar_chart.title = majorParameterName
        bar_chart.x_labels = map(str, names)
        bar_chart.add("", values1)
        render_data.append(bar_chart.render_data_uri())

  return render_template("city_profile.html", form=form, graph_data = overall_graph_data, render_data = render_data)

@app.route('/ranking', methods = ['POST', 'GET'])
def ranking():
    
    return render_template("ranking.html")



if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)
