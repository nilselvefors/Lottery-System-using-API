from flask import *
import threading, re, datetime, numpy
from threading import Thread
from CustomThreading import *
import pandas as pd
from datetime import date
from LotteryDrawer import LotteryDrawer


def readBets(lock, parameters):
    lock.acquire()

    returnJSON = {}
    returnJSON["DATE"] = {}

    bets = pd.read_csv('bets/bets.csv')
    winners = pd.read_csv('bets/winners.csv')

    bets['DATE'] = pd.to_datetime(bets['DATE'], format='%Y-%m-%d')
    winners['DATE'] = pd.to_datetime(winners['DATE'], format='%Y-%m-%d')

    if("end" in parameters and "start" in parameters):
        endDate = datetime.datetime.strptime(parameters["end"], '%Y-%m-%d')
        startDate = datetime.datetime.strptime(parameters["start"], '%Y-%m-%d')

    else:
        startDate = min(bets['DATE']).strftime('%Y-%m-%d')
        endDate = max(bets['DATE']).strftime('%Y-%m-%d')


    if(len(bets.index) == 0):
        error = {}
        error["Error"] = "No bets placed yet."
        return json.loads(json.dumps(error))

    betMask = (bets['DATE'] >= startDate) & (bets['DATE'] <= endDate)
    betsResult = bets.loc[betMask]

    for index, row in betsResult.iterrows():

        if(row["DATE"].strftime('%Y-%m-%d') not in returnJSON["DATE"]):

            returnJSON["DATE"][str(row["DATE"].strftime('%Y-%m-%d'))] = {}
            returnJSON["DATE"][str(
                row["DATE"].strftime('%Y-%m-%d'))]["Bets"] = {}
            returnJSON["DATE"][str(
                row["DATE"].strftime('%Y-%m-%d'))]["Winners"] = {}

        if(str(row["TIME"]) not in returnJSON["DATE"][str(row["DATE"].strftime('%Y-%m-%d'))]["Bets"]):

            returnJSON["DATE"][str(row["DATE"].strftime(
                '%Y-%m-%d'))]["Bets"][str(row["TIME"])] = []
            returnJSON["DATE"][str(row["DATE"].strftime(
                '%Y-%m-%d'))]["Winners"][str(row["TIME"])] = []

        returnJSON["DATE"][str(row["DATE"].strftime('%Y-%m-%d'))]["Bets"][str(row["TIME"])].append(
            {"Name": str(row["NAME"]), "Number": int(row["NUMBER"]), "Email": str(row["EMAIL"])})

    winnerMask = (winners['DATE'] >= startDate) & (winners['DATE'] <= endDate)
    winnerResult = winners.loc[winnerMask]
    for index, row in winnerResult.iterrows():
        returnJSON["DATE"][str(row["DATE"].strftime('%Y-%m-%d'))]["Winners"][str(row["TIME"])].append(
            {"Name": str(row["NAME"]), "Number": int(row["NUMBER"]), "Email": str(row["EMAIL"])})

    returnJSON["Time span"] = []

    if(not isinstance(startDate,str)):
        startDate = startDate.strftime('%Y-%m-%d')

    if(not isinstance(endDate,str)):
        endDate = endDate.strftime('%Y-%m-%d')


    returnJSON["Time span"].append({"Start": startDate})
    returnJSON["Time span"].append({"End": endDate})

    returnJSON = json.loads(json.dumps(returnJSON))
    lock.release()
    return returnJSON


def createBet(lock, data):
    lock.acquire()
    returnMessage = {}
    logedBets = []
    bets = pd.read_csv('bets/bets.csv')
    bets['NAME'] = bets['NAME'].astype(str)
    bets['DATE'] = pd.to_datetime(bets['DATE'], format='%Y-%m-%d')
    bets['TIME'] = bets['TIME'].astype(str)
    bets['NUMBER'] = bets['NUMBER'].astype(int)
    bets['EMAIL'] = bets['EMAIL'].astype(str)

    for index, date in enumerate(data.getlist("DATE")):

        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        time = str(int(data.getlist("TIME")[index]))
        number = int(data.getlist("NUMBER")[index])
        name = str(data["NAME"])
        email = str(data["EMAIL"])
        pastBets = bets.index[(bets['NAME'] == name) & (bets['DATE'] == date) & (
            bets['TIME'] == time) & (bets['EMAIL'] == email)].tolist()

        if(len(pastBets) > 0):
            betInfo = [date, time, number]
            logedBets.append(betInfo)

    if(len(logedBets) > 0):
        returnMessage["SUCCESS"] = False
        returnMessage["MESSAGE"] = "You have already placed a bet on the following numbers. Remove them from the query to place the other bets"
        returnMessage["REMOVE THE FOLLOWING BETS"] = []
        for logedbet in logedBets:
            betInfo = {
                "DATE": logedbet[0].strftime('%Y-%m-%d'),
                "TIME": logedbet[1],
                "NUMBER": logedbet[2],
            }
            returnMessage["REMOVE THE FOLLOWING BETS"].append(betInfo)

        lock.release()
        return json.dumps(returnMessage)


    for index, date in enumerate(data.getlist("DATE")):

        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        time = str(int(data.getlist("TIME")[index]))
        number = int(data.getlist("NUMBER")[index])
        name = str(data["NAME"])
        email = str(data["EMAIL"])

        newRow = {
            'NAME': name,
            'DATE': date,
            'TIME': time,
            'NUMBER': number,
            'EMAIL': email
        }
        bets = bets.append(newRow, ignore_index=True)

        totalPot = pd.read_csv('bets/totalPot.csv')

        totalPot['DATE'] = pd.to_datetime(
            totalPot['DATE'], format='%Y-%m-%d')
        totalPot['TIME'] = totalPot['TIME'].astype(str)
        totalPot['TOTALPOT'] = totalPot['TOTALPOT'].astype(int)

        pastPot = totalPot.index[(totalPot['DATE'] == date) & (
            totalPot['TIME'] == time)].tolist()

        if(len(pastPot) == 0):
            newRow = {'DATE': date, 'TIME': time, 'TOTALPOT': 100}
            totalPot = totalPot.append(newRow, ignore_index=True)

        else:
            totalPot.at[pastPot[0],
                        'TOTALPOT'] = totalPot.at[pastPot[0], 'TOTALPOT'] + 100

        bets.sort_values(by=['DATE'], inplace=True, ascending=False)
        totalPot.sort_values(by=['DATE'], inplace=True, ascending=False)

        bets.to_csv("bets/bets.csv", index=False, header=True)
        totalPot.to_csv("bets/totalPot.csv", index=False, header=True)

    returnMessage["SUCCESS"] = True
    returnMessage["MESSAGE"] = "Bet is now placed"
    lock.release()
    return json.dumps(returnMessage)


def validDate(dateText):
    try:
        datetime.datetime.strptime(dateText, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validTime(timeText):
    try:
        if(len(timeText) < 2):
            return False

        datetime.datetime.strptime(timeText, '%H')
        return True
    except ValueError:
        return False


def errorInPostParameters(data):

    #bool, name, number, email, date, time
    errors = [False, "", "", "", "", ""]
    betsInQuery = []

    # Check name
    if("NAME" in data):
        if(not isinstance(data["NAME"], str)):
            errors[1] = "Parameter NAME needs to be string"
    else:
        errors[1] = "Enter  name"

    # Check Email
    if("EMAIL" in data):
        if(not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data["EMAIL"])):
            errors[3] = "Parameter EMAIL needs valid email"
    else:
        errors[3] = "Enter email"

    if(len(data.getlist("NUMBER")) == 0):
        errors[2] = "Enter number"

    if(len(data.getlist("DATE")) == 0):
        errors[4] = "Enter date"

    if(len(data.getlist("TIME")) == 0):
        errors[5] = "Enter time"

    if(errors[2] == "" and errors[4] == "" and errors[5] == ""):

        if(len(data.getlist("NUMBER")) == len(data.getlist("DATE")) == len(data.getlist("TIME"))):

            for index, date in enumerate(data.getlist("DATE")):
                date = str(date)
                time = str(data.getlist("TIME")[index])
                number = str(data.getlist("NUMBER"))

                for bet in betsInQuery:
                    if(bet[0] == date and bet[1] == time and bet[2] == number):
                        errors[2] = "You can't bet multiple times on the same number at the same date and time"

                betsInQuery.append([date,time,number])

            for number in data.getlist("NUMBER"):
                if(isinstance(number, str)):
                    if(int(number) < 0 or int(number) > 255):
                        errors[2] = "All numbers in parameter NUMBER needs to be between 0-255"

                else:
                    errors[2] = "All numbers in parameter NUMBER needs to be string"

            for date in data.getlist("DATE"):
                if(validDate(date) == False):
                    errors[4] = "All dates in paramter DATE needs to be in format 'yyyy-mm-dd' ex '2023-12-01' "
                else:
                    if(datetime.datetime.strptime(date, '%Y-%m-%d').date() < datetime.date.today()):
                        errors[4] = "You can't place bets on past dates"

            for time in data.getlist("TIME"):
                if(validTime(time) == False):
                    errors[5] = "All dates in paramter TIME needs to be in 24-hour-format (01-00)  ex: '00', '18', '05', '16'"
        else:
            errors[2] = "Parameter NUMBER needs to be the same size as paramters DATE and TIME"
            errors[4] = "Parameter DATE needs to be the same size as paramters NUMBER and TIME"
            errors[5] = "Parameter TIME needs to be the same size as paramters NUMBER and DATE"

    for i in range(1, len(errors)):
        if(errors[i] != ""):
            errors[0] = True

    return errors


def generatePostErrorMsgJSON(errorList):
    dict = {}
    if(errorList[0] == True):
        dict["ERROR"] = errorList[0]

    if(errorList[1] != ""):
        dict["NAME"] = errorList[1]

    if(errorList[2] != ""):
        dict["NUMBER"] = errorList[2]

    if(errorList[3] != ""):
        dict["EMAIL"] = errorList[3]

    if(errorList[4] != ""):
        dict["DATE"] = errorList[4]

    if(errorList[5] != ""):
        dict["TIME"] = errorList[5]

    return json.dumps(dict)


def validGetQuery(parameters):

    #bool, start, end
    errors = [True, "", ""]

    if("start" in parameters and not "end" in parameters):
        errors[2] = "You have to specify an 'end date'"

    if(not "start" in parameters and "end" in parameters):
        errors[2] = "You have to specify an 'start date'"

    if("start" in parameters and "end" in parameters):

        if(not validDate(parameters["start"])):
            errors[1] = "Start parameter is not a valid date! Enter valid date in format 'yyyy-mm-dd' ex '2023-12-03'"

        if(not validDate(parameters["end"])):
            errors[2] = "End parameter is not a valid date! Enter valid date in format 'yyyy-mm-dd' ex '02023-12-03'"

        if(errors[1] == "" and errors[2] == ""):
            startDate = datetime.datetime.strptime(
                parameters["start"], '%Y-%m-%d').date()
            endDate = datetime.datetime.strptime(
                parameters["end"], '%Y-%m-%d').date()

            if(startDate < endDate):

                if(endDate >= date.today()):
                    errors[2] = "End date needs to be before todays date"

            else:
                errors[1] = "Start date needs to be before end date"

    for i in range(1, len(errors)):
        if(errors[i] != ""):
            errors[0] = False

    return errors


def generateGetErrorMsgJSON(errorList):
    dict = {}
    if(errorList[0] == True):
        dict["ERROR"] = errorList[0]

    if(errorList[1] != ""):
        dict["start"] = errorList[1]

    if(errorList[2] != ""):
        dict["end"] = errorList[2]

    return json.loads(json.dumps(dict))


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle():

    if(request.method == 'GET'):

        if(validGetQuery(request.args)[0] == False):

            return generateGetErrorMsgJSON(validGetQuery(request.args))

        readThread = ThreadWithReturnValue(
            target=readBets, args=(lock, request.args,))
        readThread.start()
        jsonData = readThread.join()
        return jsonData

    if(request.method == 'POST'):
        data = request.form

        if(errorInPostParameters(data)[0]):
            print("FAIL")
            return generatePostErrorMsgJSON(errorInPostParameters(data))

        writeThread = ThreadWithReturnValue(
            target=createBet, args=(lock, data))
        writeThread.start()
        result = writeThread.join()


        return result


if __name__ == '__main__':
    try:
        lock = threading.Lock()
        winnerPicker = LotteryDrawer(lock)
        winnerPicker.start()
        app.run(host='localhost', port=8081, debug=False)
        print()
        input("Press CTRL-C one more time to stop all the threads and close the program.")

    except KeyboardInterrupt:
        print()
        print('Stopping threads')
        winnerPicker.stop()
        winnerPicker.join()
