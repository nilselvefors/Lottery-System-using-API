import threading,time,random,datetime, random
import pandas as pd
from Email import Email
from threading import Thread
from threading import Event
from datetime import datetime, timedelta, time
from time import sleep


class LotteryDrawer(threading.Thread):

    def __init__(self, lock):
        Thread.__init__(self)
        self.condition = Event()
        self.email = Email()
        self.lock = lock

        print("Started LotteryDrawer thread!")


    def stop(self):
        self.condition.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        print("LotteryDrawer thread is running")
        while not self.condition.is_set():
            if(datetime.now().minute == 00):
                print("Picking winners.....")
                self.lock.acquire()

                totalPot = pd.read_csv('bets/totalPot.csv')
                bets = pd.read_csv('bets/bets.csv')

                bets['DATE'] = bets['DATE'].astype(str)
                bets['TIME'] = bets['TIME'].astype(str)
                totalPot['DATE'] = totalPot['DATE'].astype(str)
                totalPot['TIME'] = totalPot['TIME'].astype(str)

                winningNumber = random.randint(0,255)
                currentDate = datetime.today().strftime('%Y-%m-%d')
                currentTime = datetime.today().strftime('%H')

                winnersResult = bets.loc[(bets['DATE'] == currentDate)
                                         & (bets['TIME'] == currentTime)]

                print("Winning number is " + str(winningNumber))
                if(len(winnersResult.index.tolist()) > 0):

                    print("Found winners...")
                    emailList = winnersResult["EMAIL"].tolist()
                    nameList = winnersResult["NAME"].tolist()
                    totalWinnings = int(totalPot.loc[(totalPot['DATE'] == currentDate) & (
                        totalPot['TIME'] == currentTime)]["TOTALPOT"].tolist()[0])
                    winningsPerPerson = totalWinnings / len(emailList)
                    print(winningsPerPerson)

                    winners = pd.read_csv('bets/winners.csv')

                    for index, row in winnersResult.iterrows():

                        newRow = {'NAME': row["NAME"], 'DATE': row["DATE"], 'TIME': row["TIME"],
                                  'NUMBER': row["NUMBER"], 'EMAIL': row["EMAIL"], 'WINNINGS': str(winningsPerPerson)}
                        winners = winners.append(newRow, ignore_index=True)

                    winners['DATE'] = pd.to_datetime(winners['DATE'], format='%Y-%m-%d')
                    winners.sort_values(by=['DATE'], inplace=True, ascending=False)
                    winners.to_csv("bets/winners.csv", index=False, header=True)

                    print("Sending Email to winners now....")
                    self.email.sendMail(emailList,nameList,winningsPerPerson,winningNumber,currentDate,currentTime)

                else:
                    print("No winners this round....")
                    currentDrawing = totalPot.loc[(totalPot['DATE'] == currentDate) & (
                        totalPot['TIME'] == currentTime)]

                    if(len(currentDrawing.index.tolist()) > 0):

                        currentPot = currentDrawing["TOTALPOT"].tolist()[0]
                        currentTime = datetime.now().replace(minute=00,second=00 ,microsecond=00)
                        nextPotDate = currentTime + timedelta(hours=1)


                        nextpot = totalPot.loc[(totalPot['DATE'] == nextPotDate.strftime('%Y-%m-%d')) & (
                            totalPot['TIME'] == nextPotDate.strftime('%H'))]

                        if(len(nextpot.index.tolist()) > 0):
                            totalPot.at[nextpot.index.tolist()[0],'TOTALPOT']= totalPot.at[nextpot.index.tolist()[0],'TOTALPOT'] + int(currentPot)

                        else:
                            newRow = {'DATE': nextPotDate.strftime('%Y-%m-%d'), 'TIME': nextPotDate.strftime('%H'), 'TOTALPOT': currentPot}
                            totalPot = totalPot.append(newRow, ignore_index=True)


                    totalPot['DATE'] = pd.to_datetime(totalPot['DATE'], format='%Y-%m-%d')
                    totalPot.sort_values(by=['DATE'], inplace=True, ascending=False)
                    totalPot.to_csv ("bets/totalPot.csv", index = False, header=True)

                self.lock.release()



        print("Ending thread")

















#
