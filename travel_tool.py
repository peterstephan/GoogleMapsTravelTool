# This script is developed to get the distance and time for travel from A to B
# It uses the Google Maps Distance Matrix API
# It uses the XML data format output version of the API (as opposed to JSON format)
# Details about the API and its parameters are here:
# W: https://developers.google.com/maps/documentation/distance-matrix/intro
#
# Script developed by Peter Stephan, 2017


# SPECIFY INPUT CSV FILE
# Populate this using the Excel file inputs.xlsx
input_file = 'inputs_example.csv'
# SPECIFY OUTPUT CSV FILE
output_file = 'outputs_filename.csv'
# INSERT YOUR GOOGLE MAPS API KEY BELOW
your_key = "insert_your_api_key_here"

# DEPENDENCIES
import requests
import datetime as dt
import csv
from bs4 import BeautifulSoup
# to install the Beautiful Soup library: pip install bs4


# WRITE THE HEADINGS IN THE OUTPUT FILE BEFORE STARTING FOR LOOP
with open(output_file, 'a') as csvfile:
    # The 'a' setting means 'append' the data i.e. add new row
    writer = csv.writer(csvfile)
    writer.writerow([
                                'id',
                                'orig_street',
                                'orig_suburb',
                                'orig_state',
                                'orig_postcode',
                                'orig_country',
                                'dest_street',
                                'dest_suburb',
                                'dest_state',
                                'dest_postcode',
                                'dest_country',
                                'mode',
                                'transit_mode',
                                'transit_routing_preference',
                                'avoid',
                                'year',
                                'month',
                                'day',
                                'hour',
                                'minute',
                                'time_zone',
                                'traffic_model',
                                'orig_output',
                                'dest_output',
                                'duration (minutes)',
                                'distance (km)',
                                'average_speed (km/hr)'
                            ])


# READ INPUT PARAMETERS AND START A FOR LOOP
with open(input_file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        # EXTRACT AND SET PARAMETERS
        id = row['id']

        #Parameter [0] Origin Address
        orig_street = row['orig_street']
        orig_suburb = row['orig_suburb']
        orig_state = row['orig_state']
        orig_postcode = row['orig_postcode']
        orig_country = row['orig_country']
        orig_raw = orig_street + " " + orig_suburb + " " + orig_state + " " + orig_postcode + " " + orig_country
        orig = orig_raw.replace(" ","+")
        print(orig)

        #Parameter [1] Destination Address
        dest_street = row['dest_street']
        dest_suburb = row['dest_suburb']
        dest_state = row['dest_state']
        dest_postcode = row['dest_postcode']
        dest_country = row['dest_country']
        dest_raw = dest_street + " " + dest_suburb + " " + dest_state + " " + dest_postcode + " " + dest_country
        dest = dest_raw.replace(" ","+")
        print(dest)

        #Parameter [2]
        units = "metric"
        # either "metric" or "imperial"
        # Specifies the unit system to use when expressing distance as text.

        #Parameter [3]
        language = "en-EN"
        # english

        #Parameter [4]
        mode = row['mode']
        #options...
        # "driving" (default) indicates distance calculation using the road network.
        # "walking" requests distance calculation for walking via pedestrian paths & sidewalks (where available).
        # "bicycling" requests distance calculation for bicycling via bicycle paths & preferred streets (where available).
        # "transit" requests distance calculation via public transit routes (where available).
        # This value may only be specified if the request includes an API key or a
        # Google Maps APIs Premium Plan client ID. If you set the mode to transit you
        # can optionally specify either a departure_time or an arrival_time. If neither
        # time is specified, the departure_time defaults to now (that is, the departure
        # time defaults to the current time). You can also optionally include a
        # transit_mode and/or a transit_routing_preference.

        #Parameter [5]
        transit_mode = row['transit_mode']
        # Specifies one or more preferred modes of transit. This parameter may only be
        # specified for requests where the mode is transit.
        # The parameter supports the following arguments:
        # >>"bus" indicates that the calculated route should prefer travel by bus.
        # >>"subway" indicates that the calculated route should prefer travel by subway.
        # >>"train" indicates that the calculated route should prefer travel by train.
        # >>"tram" indicates that the calculated route should prefer travel by tram and light rail.
        # >>"rail" indicates that the calculated route should prefer travel by train,
        # tram, light rail, and subway. This is equivalent to transit_mode=train|tram|subway.

        #Parameter [6]
        transit_routing_preference = row['transit_routing_preference']
        # Specifies preferences for transit requests. Using this parameter, you can
        # bias the options returned, rather than accepting the default best route
        # chosen by the API. This parameter may only be specified for requests where
        # the mode is transit. The parameter supports the following arguments:
        # >>"less_walking" indicates that the calculated route should prefer limited amounts of walking.
        # >>"fewer_transfers" indicates that the calculated route should prefer a limited number of transfers.

        #Parameter [7]
        avoid = row['avoid']
        # Introduces restrictions to the route. Valid values are specified in the
        # Restrictions section of this document. Only one restriction can be specified.
        # Distances may be calculated that adhere to certain restrictions.
        # Restrictions are indicated by use of the avoid parameter, and an argument to
        # that parameter indicating the restriction to avoid.
        # The following restrictions are supported:
        # >>"tolls"
        # >>"highways"
        # >>"ferries"
        # >>"indoor"
        # Note: the addition of restrictions does not preclude routes that include the
        # restricted feature; it simply biases the result to more favorable routes.

        #Parameter 8 - Time
        # You can specify either departure_time or arrival_time, but not both.
        # Specifies the desired time of arrival for transit requests, in seconds since
        # midnight, January 1, 1970 UTC. Note that arrival_time must be specified as an integer.
        # Alternatively, you can specify a value of now, which sets the departure time
        # to the current time (correct to the nearest second).
        # .........
        # Time A - January 1, 1970
        a = dt.datetime(1970,1,1,0,0,0)
        print(a)
        # Time B - input value
        year = int(row['year'])
        month = int(row['month'])
        day = int(row['day'])
        hour = int(row['hour']) #24-hour time
        minute = int(row['minute'])
        #time_zone = int(row['time_zone']) #e.g. Brisbane = +10... could be based on Location Input...
        time_zone = 0
        hour_utc = hour + time_zone
        b = dt.datetime(year,month,day,hour_utc,minute,0)
        print(b)
        #Parameter [8-A] Arrival Time... Not set here
        arrival_time = ""
        # or
        #Parameter [8-B] Departure Time
        #departure_time = "now" #if you want the depart time to be now, when run
        departure_time = int((b-a).total_seconds())
        print(departure_time)

        #Parameter [10]
        traffic_model = row['traffic_model'] # (defaults to best_guess)
        # Specifies the assumptions to use when calculating time in traffic. This
        # setting affects the value returned in the duration_in_traffic field in
        # the response, which contains the predicted time in traffic based on
        # historical averages. The traffic_model parameter may only be specified for
        # requests where the travel mode is driving, and where the request includes a
        # departure_time, and only if the request includes an API key or a Google Maps
        # APIs Premium Plan client ID. The available values for this parameter are:

        # >>"best_guess" (default) indicates that the returned duration_in_traffic
        # should be the best estimate of travel time given what is known about both
        # historical traffic conditions and live traffic. Live traffic becomes more
        # important the closer the departure_time is to now.

        # >>"pessimistic" indicates that the returned duration_in_traffic should be
        # longer than the actual travel time on most days, though occasional days with
        # particularly bad traffic conditions may exceed this value.

        # >>"optimistic" indicates that the returned duration_in_traffic should be
        # shorter than the actual travel time on most days, though occasional days with
        # particularly good traffic conditions may be faster than this value.


        #Parameter [11]
        # API Key:
        # Rate limiting (requests/day) applies to the FREE tier of API use
        # Free up to 2,500 requests per day.
        # If billing is enabled: $0.50 USD / 1,000 additional requests, up to 100,000 daily
        key = your_key


        # GENERATE the URL of where to scrape
        url_base = "https://maps.googleapis.com/maps/api/distancematrix/xml?"
        url_parameters = "origins={0}&destinations={1}&units={2}&language={3}&mode={4}&transit_mode={5}&transit_routing_preference={6}&avoid={7}&departure_time={8}&traffic_model={9}&key={10}".format(str(orig),str(dest),str(units),str(language),str(mode),str(transit_mode),str(transit_routing_preference),str(avoid),str(departure_time),str(traffic_model),str(key))
        url_target = url_base + url_parameters

        print(url_target)

        # SCRAPE the HTML
        response = requests.get(url_target)
        xml_output = BeautifulSoup(response.content, 'xml')
        print()
        print(xml_output)
        print()

        # Extract parsed origin and destination
        orig_output = xml_output.origin_address.string
        dest_output = xml_output.destination_address.string
        print("Origin Address Output: ", orig_output)
        print("Destination Address Output: ", dest_output)

        # Extract and print the duration of the trip in seconds and convert to minutes
        duration_seconds = xml_output.row.element.duration.value.string
        duration = float(duration_seconds) / 60 # convert to minutes
        print("Duration (min): ", duration)

        # Extract and print the distance of the trip in metres and convert to km
        distance_metres = xml_output.row.element.distance.value.string
        distance = float(distance_metres) / 1000 #convert to km
        print("Distance (km): ", distance)
        print()

        # Calculate average travel speed
        speed = float (distance / (duration / 60))


        # WRITE RESULTS TO A CSV FILE
        with open(output_file, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                                id,
                                orig_street,
                                orig_suburb,
                                orig_state,
                                orig_postcode,
                                orig_country,
                                dest_street,
                                dest_suburb,
                                dest_state,
                                dest_postcode,
                                dest_country,
                                mode,
                                transit_mode,
                                transit_routing_preference,
                                avoid,
                                year,
                                month,
                                day,
                                hour,
                                minute,
                                time_zone,
                                traffic_model,
                                orig_output,
                                dest_output,
                                duration,
                                distance,
                                speed
                            ])

print("")
print("")
print("Script finished")
