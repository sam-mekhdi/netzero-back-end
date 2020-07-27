import json

from flask import Flask, abort, request

app = Flask(__name__)

#import users json file
with open('./mockdata.json', 'r') as jsonfile:
    file_data = json.load(jsonfile)

#import food json file
with open('./foodData.json', 'r') as jsonfile:
    food_data = json.load(jsonfile)

#display all userdata
@app.route('/users', methods =['GET'])
def alldata():
        return file_data

#take in studentID, check if it exists, if so, return all data, if not, return 404 error
@app.route('/users/<studentID>/', methods =['GET', 'POST'])
def transactions(studentID):
    #POST new student number
    print(studentID)
    if request.method == 'POST':
        if doesStudentExist(studentID) == True:
            abort(404)
        else:
            newuser = initStudent(studentID)
            file_data['Transactions'].append(newuser)
        return file_data
    #GET all data associated with student if it exists
    else:
      return getData(studentID)

#get student totalfootprint score
@app.route('/users/<studentID>/getpoints', methods =['GET'])
def getpoints(studentID):
    param = getData(studentID)
    return param['totalFootPrint']

#get latest transaction info !!DEPRECIATED!!
@app.route('/users/<studentID>/latest', methods =['GET'])
def lasttrans(studentID):
    param = getData(studentID)
    return param['transactions'][len(param['transactions']) - 1]

#get individual transaction info for the last transaction !!DEPRECIATED!!
@app.route('/users/<studentID>/getdata', methods =['GET'])
def getdata(studentID):
    params = request.args.get('params', None)
    if params == None:
        userData = lasttrans(studentID)
    return userData[params]

#post new transaction !!DEPRECIATED!!
@app.route('/users/<studentID>/transactions/createTransaction', methods =['POST'])
def newtrans(studentID):
    transdata = request.get_json()
    param = getData(studentID)
    param['transactions'].append(transdata)
    return param

#get specific transactionID
@app.route('/users/<studentID>/transactions', methods =['GET', 'POST', 'DELETE'])
def transID(studentID):
    if request.method == 'GET':
        transactionID = request.args.get('transactionID', None)
        field = request.args.get('param', None)
        param = getData(studentID)
        #returns specific transaction if given transactionID
        print(transactionID)
        if transactionID == None:
            param = lasttrans(studentID)
        #if not given transactionID, return latest transaction
        else:
            for transSize in param['transactions']:
                if (transSize['transactionID']) == transactionID:
                    param = transSize
        #if no param, return whole transaction
        if field == None:
            return param
        #else if given param, return that param
        else:
            return param[field]
    #delete a transaction 
    elif request.method == 'DELETE':
        itemName = request.args.get('itemName', None)
        user = getData(studentID)
        param = getUserItem(studentID, itemName)
        print(param)
        user['transactions'].remove(param)
        return file_data
    else:
        print("enter postrequest")
        itemName = request.args.get('itemName', None)
        transdata = getFoodData(itemName)
        param = getData(studentID)
        print(param)
        param['transactions'].append(transdata)
        return file_data
#################################################################
#display all fooddata
@app.route('/food', methods =['GET'])
def allfooddata():
        return food_data

#delete an item from my transactions (ingredients)

#add an ingredient to my transactions

#food Search
@app.route('/food/<itemName>/', methods =['GET', 'POST', 'DELETE'])
def food(itemName):
    #search for and get food item
    if request.method == 'GET':
        return getFoodData(itemName)
    #delete an item from the food database
    elif request.method == 'DELETE':
        param = getFoodData(itemName)
        food_data['food'].remove(param)
        return food_data
    #post new item to food database
    else:
        itemData = request.get_json()
        food_data['food'].append(itemData)
        return food_data
        


#initialize a new user
def initStudent(studentID):
    newuser =  {"studentNumber": "", "totalFootPrint": "0", "transactions": []}
    newuser['studentNumber'] = str(studentID)
    return newuser

#check if student number exists in database
def doesStudentExist(studentID):
    result = False
    for transSize in file_data['Transactions']:
        if (transSize['studentNumber']) == studentID:
            return True
            break
    return result

#check if food item exists in database
def doesItemExist(itemName):
    result = False
    for transSize in food_data['food']:
        if (transSize['itemName']) == itemName:
            return True
            break
    return result

#get all data for a specific student
def getData(studentID):
    param = None
    for transSize in file_data['Transactions']:
        if (transSize['studentNumber']) == studentID:
            param = transSize
    if param == None:
        abort(404)
    else:
        return param

#get specific item from a users data
def getUserItem(studentID, itemName):
    user = getData(studentID)
    for transSize in user['transactions']:
        if (transSize['itemName']) == itemName:
            param = transSize
    return param

#get all data for a specific student
def getFoodData(itemName):
    param = None
    for transSize in food_data['food']:
        if (transSize['itemName']) == itemName:
            param = transSize
    if param == None:
        abort(404)
    else:
        return param
    

if __name__ == '__main__':
    app.run(debug=True)