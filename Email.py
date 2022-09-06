import smtplib
import ssl
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep


class Email():

    def __init__(self):
        self.senderAddress = 'ProgrammingProjectT5@gmail.com'
        self.senderPass = 'ThisIsAStongPasswordGoogle'
        self.session = smtplib.SMTP('smtp.gmail.com', 587)
        self.session.starttls()
        self.session.login(self.senderAddress, self.senderPass)
        self.message = MIMEMultipart()
        self.message['From'] = "T5 Lottery"
        self.message['Subject'] = 'You have won the lottery!'

    def sendMail(self, receiverAddressList, nameList, winningAmount, pickedNumber, date, time):
        if(len(time) < 2):
            time = "0" + str(time)
        for index,mailAddress  in enumerate(receiverAddressList):

            name = nameList[index]

            text = "Hi " + str(name) + "! \nYou have won the lottery!\nYou bet 100 SEK on number " + str(pickedNumber) + \
                " for date: " + \
                date + " and time: " + str(time) + "\nYou have won a total of " + str(winningAmount) + " SEK!!!!"

            self.message.attach(MIMEText(str(text), 'plain'))
            self.message['To'] = self.senderAddress
            text = self.message.as_string()
            self.session.sendmail(self.senderAddress, str(mailAddress), text)
            sleep(2)
