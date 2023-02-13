This project was made by Nils Elvefors

The user can place bets and see old historical information
about past bets and winners
The API communicates via JSON
The API sends an email to all the winners each round

The API draws a winner each hole hour of every day, 24/7.
If there is a winner with the correct number the API will email the
winner about the winnings!
If there is no winner, the pot of money will get transferred to the new waffle.

(The email will probably end up in the "trash" folder)

To close the program, press CTRL-C two times!!!

instructions of usage:

Place a bet:

To place a bet you will need to send a POST-request to the server with the
following parameters:
(All of the parameter-names needs to be in uppercase letters!!!)

NAME: Your name
NUMBER: The number you want to guess
EMAIL: Your email address
DATE: The date you want guess the specific number (format yyyy-mm-dd)
TIME: The specific time of that day you want guess the specific number (format HH)

Example:
I think number 100 will win the raffle at 19th of December 2024 at 15:00
My parameters will be the following:
NAME: Nils Elvefors
NUMBER: 100
EMAIL: nils@elvefors.com
DATE: 2024-12-19
TIME: 15


To place multiple bets with one query, specify the date, time and number for
each bet you want to create.

Example:
I want to place 3 bets:

Number 10 at 15:00, 2020-01-01
Number 77 at 10:00, 2020-11-07
Number 100 at 00:00, 2027-01-07

Correct query for this is:
NAME: Nils Elvefors
NUMBER: [10, 77, 100]
EMAIL: nils@elvefors.com
DATE: [2020-01-01,2020-11-07,2027-01-07]
TIME: [15, 10, 00]



Get historical data:

To get historical data you will need to preform a GET-request to the server.
You don't need to use any parameters but you can if you want a
more specific time period to look at.
If you don't use any parameters you will get all the bets and winners ever made
to the server.


If you want a more specific time period you use parameters named "start"
and "end".
You have to use both of them.

The "start" parameter indicates the date at which you want to start the
historical data from.
The "end" parameter indicates the date at which you want to stop the
historical data.

Example:
Get historical data from 2010-12-01 until 2020-01-20

start: 2010-12-01
end:   2020-01-20
