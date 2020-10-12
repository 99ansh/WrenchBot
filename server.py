from flask import Flask,request
from flask_cors import CORS
import os
import dialogflow_v2 as dialogflow
import mysql.connector
import pandas as pd

app=Flask(__name__)
CORS(app)

mydb = mysql.connector.connect(
  host="dev.wrench.com",
  user="wrench_readwrite",
  password="Wr3nch!",
  database="wrench"
)

mycursor = mydb.cursor(buffered=True)
print("Connected to devDB")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="mychatbotkey.json"

project_id = "wrenchbot-ykrg"
session_id = "temp"
email="temp"
language_code = "en-US"
response_text = ''
session_client = dialogflow.SessionsClient()
session = session_client.session_path(project_id, session_id)


@app.route('/',methods=["POST"])
def receive_request():
    text=request.form["msg"]
    print(text)
    return forward_request(text)
def forward_request(text):   
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    intent = response.query_result.intent.display_name
    print(intent)
    if intent=="Default Welcome Intent":
        return default_welcome_intent(response)
    elif intent=="check-servicearea-intent":
        return check_servicearea_city(response)
    elif intent=="Default Fallback Intent":
        return default_fallback_intent(response)
    elif intent=="negative-intent":
        return negative_intent(response)
    elif intent=="email-intent":
        return email_intent(response)
    elif intent=="total-cost-intent":
        return total_cost_intent(response)
    else:
        return default_fallback_intent(response)
def default_welcome_intent(response):
    response_text=response.query_result.fulfillment_text
    return response_text
def default_fallback_intent(response):
    response_text=response.query_result.fulfillment_text
    return response_text
def about_wrench_intent(response):
    response_text=response.query_result.fulfillment_text
    return response_text
def negative_intent(response):
    response_text=response.query_result.fulfillment_text
    return response_text
def total_cost_intent(response):
    global email
    query="select sum(amount) from Payment where UserId=(select Id from User where email='"+email+"');"
    mycursor = mycursor.execute(query)
    myresult=mycursor.fetchall()
    if len(myresult)>0:
        response_text=myresult[0][0]
    else:
        response_text="User not found!"
    return response_text
    
def check_servicearea_city(response):
    parameter = response.query_result.parameters.fields.get("geo-city").string_value
    query="select count(*) from ZipMap where City like %s"
    temp=("%"+str(parameter)+"%",)
    mycursor.execute(query,temp)
    myresult = mycursor.fetchall()
    if myresult[0][0]>0:
        response_text="Yes we are available"
    else:
        response_text="Sorry, we are not available"
    return response_text
def email_intent(response):
    global session
    global email
    parameter = response.query_result.parameters.fields.get("email").string_value
    email=parameter
    query="select Id from User where email=%s"
    temp=(str(parameter),)
    print(temp)
    mycursor.execute(query,temp)
    myresult = mycursor.fetchall()
    print(myresult)
    if len(myresult)>0:
        session_id=myresult[0][0]
        print("hello")
        session = session_client.session_path(project_id, session_id)
        query="select FirstName from User where email=%s"
        mycursor.execute(query,temp)
        response_text="Welcome "+mycursor.fetchall()[0][0]+"!"
        
    else:
        response_text=forward_request("false")
    return response_text

if __name__ == '__main__': 
    app.run(debug=True) 
