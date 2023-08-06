# Jacob Smith
# CYB600 - Secure Software Engineering
# Lab 1 - Python Webserver


from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

# hostName - Name of the host.
# portNum - Port number to use.
# currTime - Gets the current time.

hostName = "localhost"
portNum = 8080
currTime = datetime.now()


def reformat(inTime):
    """
    Takes in an input datetime in form YYYY-DD-MM HH:MM:SS:MS and formats it to be in the form HH:MM <AM/PM>.

    Input must be a datetime object generated with datetime.now().
    """
    timeStr = str(inTime)               # creates datetime string
    timeList = reformatHelper(timeStr)  # helper function gets the necessary data from the datetime string

    # hours -> hours portion of the timestamp
    # minutes -> minutes portion of the timestamp
    # daytime -> AM/PM

    hours = int(timeList[0])
    minutes = int(timeList[1])
    daytime = 'AM'

    if hours == 0:            # corrects UTC 00:00 to 12:00 AM
        hours = hours + 12
    elif hours == 12:         # corrects UTC 12:00 to 12:00 PM
        daytime = 'PM'
    elif hours > 12:          # corrects UTC > 12:00 to normal time (i.e. 23:00 becomes 11:00 PM)
        daytime = 'PM'
        hours = hours - 12

    # corrects the minutes if < 10 (i.e. displays 1:04 PM instead of the incorrect 1:4 PM)
    if minutes < 10:
        finalStr = str(hours) + ':' + '0' + str(minutes) + ' ' + daytime
    else:
        finalStr = str(hours) + ':' + str(minutes) + ' ' + daytime
    return finalStr


def reformatHelper(inStr):
    """
    Helps format the time into HH:MM <AM/PM> form.

    Input string must be a datetime object generated with datetime.now(), converted to a string with str().
    """
    # first time split, separates the date and time and discards the date
    t1 = inStr.split(' ')
    s1 = t1[1]

    # second time split, discards the milliseconds
    t2 = s1.split('.')
    s2 = t2[0]

    # third time split, splits hours, minutes, and seconds
    t3 = s2.split(':')
    return t3


realTime = reformat(currTime)


class TimeServer(BaseHTTPRequestHandler):
    """
        Class to create a webserver that tells the current time.
        Webpage looks like:

        Welcome to the Time Server!
        Current Time: XX:XX AM/PM
    """
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Current Time</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Welcome to the Time Server!<p>", "utf-8"))
        self.wfile.write(bytes("<p>Current Time: %s</p>" % realTime, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


def createServer():
    # instantiates a server object and starts the server
    timeServer = HTTPServer((hostName, portNum), TimeServer)
    # server started message
    print("Server started at http://%s:%s" % (hostName, portNum))
    print("Press CTRL+C to stop")

    # check for keyboard interrupts
    try:
        timeServer.serve_forever()
    except KeyboardInterrupt:
        timeServer.server_close()

    timeServer.server_close()
    print("Server stopped")


if __name__ == '__main__':
    createServer()

