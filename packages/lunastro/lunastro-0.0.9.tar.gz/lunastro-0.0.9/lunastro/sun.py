import math
import datetime


# start by calculating julian date
class Sun:
    def __init__(self):

        self.dayMs = 1000 * 60 * 60 * 24
        self.J1970 = 2440588
        self.J2000 = 2451545

    def toJulian(self, date):
        return date.timestamp() / self.dayMs - 0.5 + self.J1970

    def fromJulian(self, j):
        return datetime.datetime.fromtimestamp((j + 0.5 - self.J1970) * self.dayMs)

    def toDays(self):
        date = datetime.datetime.now()
        return self.toJulian(date) - self.J2000

    def get_julian_date(self):
        date = None
        # If no date is provided, use the current date and time
        if date is None:
            date = datetime.datetime.now()

        # Convert the date to a timestamp in milliseconds
        timestamp = date.timestamp() * 1000

        # Calculate the timezone offset in minutes
        if date.utcoffset():
            timezone_offset = date.utcoffset().total_seconds() // 60
        else:
            timezone_offset = 0

        # Calculate the Julian date and return it
        julian_date = (timestamp / 86400000) - (timezone_offset / 1440) + 2440587.5
        return julian_date

    def solardistance(self):
        juliandate = self.get_julian_date()
        # days since greenwich noon
        n = juliandate - 2451545
        # positions
        meanlong = 280.460 + 0.9856474 * n
        # g is mean anomaly
        g = 357.528 + 0.9856003 * n
        tmp = math.cos(g)
        temptwo = math.cos(2 * g)
        # solar distance is in astronomical units
        solardistance = 1.00014 - 0.01671 * tmp - 0.00014 * temptwo
        return solardistance * 92955807.3  # miles

    def declination(self, l, b):
        e = (math.pi / 180) * 23.4397
        return math.asin(math.sin(b) * math.cos(e) + math.cos(b) * math.sin(e) * math.sin(l))



    def eclipticlongitude(self, anomaly):
        tmp = math.pi / 180 * (
        1.9148 * math.sin(anomaly) + 0.02 * math.sin(2 * anomaly) + 0.0003 * math.sin(3 * anomaly))
        sectemp = math.pi / 180 * 102.9372
        return tmp + sectemp + math.pi



    def rightAscension(self, l, b):
        e = math.pi / 180 * 23.4397
        return math.atan2(math.sin(l) * math.cos(e) - math.tan(b) * math.sin(e), math.cos(l))

    def azimuth(self, h, phi, declination):
        return math.atan2(math.sin(h), math.cos(h) * math.sin(phi) - math.tan(declination) * math.cos(phi))



    def hourangle(self):
        # it is approximate (doesn't take into account minutes)
        if datetime.datetime.now().hour > 12:
            return 15 * (datetime.datetime.now().hour - 12)
        else:
            return 15 * (-(datetime.datetime.now().hour) + 12)
            
    def mean_solar_time(self, longitude):
        solartime = self.get_julian_date() - longitude/360
        return solartime # returns in approximate mean solar time
   
    def solar_mean_anomaly(self, longitude):
        solartime = self.mean_solar_time(longitude)
        anomaly = (357.5291 + 0.98560028 * solartime)%360
        return anomaly
    
    def center_equation(self, longitude):
        m = self.solar_mean_anomaly(longitude)
        c = 1.9148*math.sin(m) + 0.02 * math.sin(2 * m) + 0.0003*math.sin(3*m)
        return c
    
   def calculate_sunrise(self, latitude, longitude, date):
        """
        Calculates the time of sunrise for a given latitude, longitude, and date.

        Arguments:
        latitude -- the latitude of the location (in decimal degrees)
        longitude -- the longitude of the location (in decimal degrees)
        date -- the date for which to calculate sunrise (as a datetime object)

        Returns:
        A datetime object representing the time of sunrise on the given date at the given location.
        """

        # Calculate the number of days since January 1st of the current year
        N = date.timetuple().tm_yday

        # Calculate the local apparent solar time
        time_offset = (longitude / 15.0)
        solar_time = datetime.datetime.combine(date, datetime.time(12)) - datetime.timedelta(hours=time_offset)

        # Calculate the hour angle at sunrise
        hour_angle = math.degrees(math.acos((math.sin(math.radians(-0.83)) - math.sin(math.radians(latitude)) * math.sin(math.radians(23.44))) / (math.cos(math.radians(latitude)) * math.cos(math.radians(23.44))))

        # Calculate the time of sunrise
        sunrise = solar_time + datetime.timedelta(minutes=hour_angle * 4)

        return sunrise



        
        
