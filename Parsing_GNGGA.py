# Calling UART
from machine import Pin, UART, I2C
# Calling time because of sleep
import utime, time
from bme280 import BME280

# We are setting the txPin = 0, rxPin = 1, baudrate = 9,600
# At U-center we're able to know baudrate of Neo-M8Q-0-10 Module that we used
gpsModule = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
i2c = I2C(0, sda = Pin(4), scl = Pin(5), freq = 400000)
# We are setting the sda = 4, scl = 5
# print(gpsModule)
# if you want UART status, delete #
# We will create a byte array object called buff to store the NMEA sentences
buff = bytearray(255)

TIMEOUT = False
FIX_STATUS = False

# Following variables will store the GPS param including latitude, longitude, number of satellites
# Additionally store the UTC time and altitude
firstLatitude = ""
secondLatitude = ""
thirdLatitude = ""
fourthLatitude = ""
fifthLatitude = ""
#Latitude = ""
firstLongitude = ""
secondLongitude = ""
thirdLongitude = ""
fourthLongitude = ""
fifthLongitude = ""
# longitude = ""
satellites = ""
altitude = ""
GPStime = ""
latitudeIndicator = ""
longitudeIndicator = ""
hourGPStime = ""
minuteGPStime = ""
secondGPStime = ""
intAltitude = ""
floatAlititude = ""
# The following function obtains the GPS coordinates.
# We are running a while loop to obtain the GPS data from the basic NMEA sentence $GNGGA.
# Latitude, Longitude, Satellites and time will be acquired from the NMEA sentence accordingly and saved in their respective variables.
def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime, altitude, latitudeIndicator, longitudeIndicator
    global firstLatitude, secondLatitude, thirdLatitude, fourthLatitude, fifthLatitude
    global firstLongitude, secondLongitude, thirdLongitude, fourthLongitude, fifthLongitude
    global hourGPStime, minuteGPStime, secondGPStime, intAltitude, floatAltitude
    timeout = time.time() + 20
    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        # before buff = str(gpsModule.readline())
        parts = buff.split(',')
        
        # parts[0] = $GNGGA
        # parts[1] = Time of Greenwich 
        # parts[2] = Latitude
        # parts[3] = N/S Indicator
        # parts[4] = Longitude
        # parts[5] = E/W Indicator
        # parts[7] = Number of Satellites
        # parts[9] = Altitude
        # parts[11] = Geoidal Separation //Not Altitude 

        if (parts[0] == "b'$GNGGA" and len(parts) == 15):
            if(parts[0] and parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[7] and parts[9]):
                if (parts[3] == 'S'):
                    parts[3] = 0
                    latitudeIndicator = parts[3]
                else :
                    parts[3] = 1
                    latitudeIndicator = parts[3]
                # longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    parts[5] = 0
                    longitudeIndicator = parts[5]
                else :
                    parts[5] = 1
                    longitudeIndicator = parts[5]
                parts[1] = list(map(float, parts[1]))
                parts[1] = list(map(int, parts[1]))
                parts[2] = list(map(float, parts[2]))
                parts[2] = list(map(int, parts[2]))
                # parts[3] = list(map(float, parts[3]))
                # parts[3] = list(map(int, parts[3]))
                parts[4] = list(map(float, parts[4]))
                parts[4] = list(map(int, parts[4]))
                # parts[5] = list(map(float, parts[5]))
                # parts[5] = list(map(float, parts[5]))
                parts[7] = list(map(float, parts[7]))
                parts[7] = list(map(int, parts[7]))
                parts[9] = list(map(float, parts[9]))
                parts[9] = list(map(int, parts[9]))
                # Converting float before converting int
                
                firstLatitude = parts[2][0] * 10 + parts[2][1]
                secondLatitude = parts[2][2] * 10 + parts[2][3]
                thirdLatitude = parts[2][4] * 10 + parts[2][5]
                fourthLatitude = parts[2][6] * 10 + parts[2][7]
                fifthLatitude = parts[2][8] * 10 + parts[2][9]
                
                firstLongitude = parts[4][0] * 100 + parts[4][1] * 10 + parts[4][2]
                secondLongitude = parts[4][3] * 10 + parts[4][4]
                thirdLongitude = parts[4][5] * 10 + parts[4][6]
                fourthLongitude = parts[4][7] * 10 + parts[4][8]
                fifthLongitude = parts[4][9] * 10 + parts[4][10]
                # latitude = convertToDegree(parts[2])
                parts[0] = "$GNGGA"
                #parts = list(map(int, parts))
                
                # If indicator was South or West, we're converting to 1
                satellites = parts[7][0] * 10 + parts[7][1]
                # GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                # parts[1] = [a, b, c, d, f, e]
                # parts[1][0:2] = Hour
                # parts[1][2:4] = Minute
                # parts[1][4:6] = Second

                hourGPStime = parts[1][0] * 10 + parts[1][1] + 9
                minuteGPStime = parts[1][2] * 10 + parts[1][3] 
                secondGPStime = parts[1][4] * 10 + parts[1][5]
                
                if len(parts[9]) == 5:
                    intAltitude = parts[9][0] * 100 + parts[9][1] * 10 + parts[9][2]
                    floatAltitude = parts[9][3] * 10 + parts[9][4]
                elif len(parts[9]) == 4 :
                    intAltitude = parts[9][0] * 10 + parts[9][1]
                    floatAltitude = parts[9][2] * 10 + parts[9][3]
                elif len(parts[9]) == 3 :
                    intAltitude = parts[9][0]
                    floatAltitude = parts[9][1] * 10 + parts[9][2]
                    
                FIX_STATUS = True
                break
                
        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)
# The following function is responsible to convert the raw longitude and latitude data to actual values.
def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.9f}'.format(Converted) 
    return Converted
    # Return type of Latitude & Longitude is String type

# Inside the infinite loop we will call the getGPS(gpsModule) function first. 
# If the GPS data is not acquired within the time set within the program, then “No GPS data is found” message is printed on the shell console instead.
while True:
    #try:
        getGPS(gpsModule)
        if(FIX_STATUS == True):
            print("Latitude: {} {} {} {} {} {} {} {}".format(hex(18), hex(latitudeIndicator), hex(firstLatitude), hex(secondLatitude), hex(thirdLatitude), hex(fourthLatitude), hex(fifthLatitude), hex(52)))
            print("Longitude: {} {} {} {} {} {} {} {}".format(hex(18), hex(longitudeIndicator), hex(firstLongitude), hex(secondLongitude), hex(thirdLongitude), hex(fourthLongitude), hex(fifthLongitude), hex(52)))
            print("Satellites: {} {} {}".format(hex(18), hex(satellites), hex(52)))     
            print("Altitude : {} {} {} {}".format(hex(18), hex(intAltitude), hex(floatAltitude), hex(52)))
            print("Time = {} {} {} {} {}".format(hex(18), hex(hourGPStime), hex(minuteGPStime), hex(secondGPStime), hex(52)))
            bme = BME280(i2c = i2c)
            print(bme.values)
            print()
            FIX_STATUS = False

        if(TIMEOUT == True):
            print("No GPS data")
            TIMEOUT = False
