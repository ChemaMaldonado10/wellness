from flask import Flask, request, abort, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_caching import Cache

import json
import mysql.connector
import csv

# Our app name.
api = Flask(__name__)

# Cache configuration

# In this hypothetical case of cache use we set a timeout for 5 minutes
# so we can storage some data in that amount of time for a quick use.
config = {
    "DEBUG": False,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

cache = Cache(api)

# Database params.
mydb = mysql.connector.connect(
      host="localhost",
      user="chema",
      password="ddbb")

# JWT configuration for Login Auth.
api.config['JWT_SECRET_KEY'] = 'secret_seed'
jwt = JWTManager(api)

# REQUIRED

# Creating Database and tables.
# Import CSV file into database.
@api.route("/import_csv", methods=['GET'])
def import_csv():

    mycursor = mydb.cursor()

    # Create database and table.
    mycursor.execute("DROP DATABASE IF EXISTS example")
    mycursor.execute("CREATE DATABASE example")
    mycursor.execute("USE example")

    mycursor.execute("CREATE TABLE stats (date VARCHAR(20), energy DECIMAL(24,5), reactive_energy DECIMAL(24,5), power DECIMAL(24,5), maximeter DECIMAL(24,5), reactive_power DECIMAL(24,5), voltage DECIMAL(24,5), intensity DECIMAL(24,5), power_factor DECIMAL(24,5));")

    # Importing csv data.
    with open("csv_data/report.csv", mode='r') as csv_data:
        reader = csv.reader(csv_data, delimiter=',')
        next(reader)
        csv_data_list = list(reader)

        for row in csv_data_list:
            for i in range(0, len(row)):
                if row[i] == '':
                    row[i] = '0.000'

            print(row)

            mycursor.execute("""
                INSERT INTO stats(
                date, energy, reactive_energy, power, maximeter, reactive_power, voltage, intensity, power_factor)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

            mydb.commit()

    return {'msg': 'csv imported!'}

# Obtaining requested data in the picture.
@api.route("/data_example", methods=['GET'])
def data_example():

    mycursor = mydb.cursor()
    mycursor.execute("USE example")
    mycursor.execute("SELECT * FROM stats ORDER BY date ASC LIMIT 1")

    result = mycursor.fetchall()
    print (result)

    return {'data_example': str(result)}

# Obtaining individual data for a statistic in order to make the graph
@api.route("/graph_example", methods=['GET'])
def graph_example():

    mycursor = mydb.cursor()
    mycursor.execute("USE example")

    mycursor.execute("SELECT date, energy FROM stats ORDER BY date ASC limit 15")
    result = mycursor.fetchall()
    print (result)

    return {'graph_example': str(result)}


# OPTIONAL

#Auth system.
@api.route("/login", methods=['POST', 'GET'])
def login():

    # Obtaining email and password from POST.
    email = str(request.form.get('email'))
    password = str(request.form.get('password'))

    # Check the basics from both of them.
    result = checkCredentials(email, password)

    # Assuming password is hashed (for security reason) in this part of the code
    # we should check with the database if the hashed password is correct using
    # using libraries as bcrypt for python.

    # If all the checks were correct it´s time to create a token in order to speed up
    # future user data management. We can do it using JWT (Json Web Token).

    access_token = create_access_token(identity = email)

    # To make it real in this test we return an error (True) if credentials are wrong
    # or our session token if everything were great.

    if result == False:
        return {'token': 'Wrong credentials', 'error': True}


    else:
        return {'msg': 'Hello mate!', 'token': access_token, 'error': False}

# Basics check for login credentials.
def checkCredentials(email, password):
    if(email == "" or password == "" or '@' not in email):
        return False
    return True


# Cache endpoint.
@api.route('/cache_example', methods = ['GET'])
# Simply use cache decorator to cache the function below
@cache.cached(timeout=300)
def cache_example():
    return {'cached_time': '300s'}



if __name__ == '__main__':
    api.run(host='138.68.90.90', port=8080, debug=True)
