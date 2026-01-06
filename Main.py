"""
Andrew Brown
ID: #011512148
WGU Email: abr3374@wgu.edu
7/16/2025
C950 - Data Structures and Algorithms II
"""

# import statements
import csv, datetime
from Package import Package
from HashTable import HashTable

# data structures to read in the distances between addresses the trucks will visit
addresses = {}
distances = []

# "truck" lists to represent the trucks delivering packages
truck1 = []
truck2 = []
truck3 = []


# "add_packages" function to read the package data into the hash table
def add_packages(table):
    with open(
            'CSV/WGUPS Package Table.csv') as package_file:  # opens the "WGU Package Table" file containing the package data
        reader = csv.reader(package_file)  # declares a "reader" to read the data from the file
        packages = list(reader)  # creates a list containing each line ("package") in the file
        for package in packages:  # loops through the list of packages in the file

            new_package = Package(int(package[0]), package[1], package[2], package[3], package[4], package[5],
                                  package[6], package[7], package[8], package[9], package[10], package[11],
                                  package[12])  # creates a "Package" object with the data read from the file
            table.insert(int(package[0]), new_package)  # inserts the package data into the hash table


# "add_distances" function to read in the address and distance data
def add_distances():
    with open(
            'CSV/WGUPS Distance Table.csv') as distances_file:  # opens the "WGU Distance Table" file containing the address and distance data
        reader = csv.reader(distances_file)  # declares a "reader" to read the data from the file
        lines = list(reader)  # creates a list containing each line ("package") in the file
        index = 0  # index variable to assign an index to each address
        for line in lines:  # loops through the list of addresses in the file
            address = line[0]  # collects the address from the file
            line.pop(0)  # "pops" the address off of the line
            addresses.update({address: index})  # adds the address and its index to the "addresses" dictionary
            index += 1  # increments the index variable
            distances.append(line)  # appends the distance data to the "distances" list


# "print_header" function that displays a key for the info displayed in the UI
def print_header():
    print('---KEY---')
    print(
        '[PACKAGE ID, DELIVERY STATUS, ADDRESS, CITY, ZIP CODE, DELIVERY DEADLINE, WEIGHT, LOADING_TIME, TRUCK, DRIVER, PACKAGE NOTES]')


# "updates" function to handle special updates during the delivery simulation
def updates(table, timestamp):
    if datetime.timedelta(hours=8, minutes=50) < timestamp < datetime.timedelta(hours=9,
                                                                                minutes=10):  # if it is time for the delayed packages to arrive at the hub...
        print('\033[33m' + str(datetime.timedelta(hours=9,
                                                  minutes=5)) + ': Delayed packages 6, 25, 28, and 32 arrive at the hub' + '\033[0m')  # ...print an update message to the output console
    elif datetime.timedelta(hours=10) < timestamp < datetime.timedelta(hours=10,
                                                                       minutes=20):  # if it is time to update the address of package 9...
        # ...update package 9's address and print an update message to the output console
        table.get(9).address = '410 S State St'
        table.get(9).zipcode = '84111'
        print('\033[33m' + str(
            datetime.timedelta(hours=10, minutes=20)) + ": Package 9's address is updated to " + table.get(
            9).address + ', ' + table.get(9).city + ', ' + table.get(9).zipcode + '\033[0m')


# "load" function to add an individual package to a truck
def load(truck, package):
    truck.append(package)  # append the package to the truck list
    # assign the appropriate truck to the package data
    if truck == truck1:
        package.truck = 'Truck 1'
    elif truck == truck2:
        package.truck = 'Truck 2'
    elif truck == truck3:
        package.truck = 'Truck 3'


# "load_trucks" function to load all 40 packages onto all 3 trucks
def load_trucks(table):
    # Truck 1
    load(truck1, table.get(1))
    load(truck1, table.get(4))
    load(truck1, table.get(7))
    load(truck1, table.get(13))
    load(truck1, table.get(14))
    load(truck1, table.get(15))
    load(truck1, table.get(16))
    load(truck1, table.get(19))
    load(truck1, table.get(20))
    load(truck1, table.get(21))
    load(truck1, table.get(29))
    load(truck1, table.get(30))
    load(truck1, table.get(31))
    load(truck1, table.get(34))
    load(truck1, table.get(39))
    load(truck1, table.get(40))

    # Truck 2
    load(truck2, table.get(3))
    load(truck2, table.get(5))
    load(truck2, table.get(6))
    load(truck2, table.get(18))
    load(truck2, table.get(25))
    load(truck2, table.get(26))
    load(truck2, table.get(36))
    load(truck2, table.get(37))
    load(truck2, table.get(38))

    # Truck 3
    load(truck3, table.get(2))
    load(truck3, table.get(8))
    load(truck3, table.get(9))
    load(truck3, table.get(10))
    load(truck3, table.get(11))
    load(truck3, table.get(12))
    load(truck3, table.get(17))
    load(truck3, table.get(22))
    load(truck3, table.get(23))
    load(truck3, table.get(24))
    load(truck3, table.get(27))
    load(truck3, table.get(28))
    load(truck3, table.get(32))
    load(truck3, table.get(33))
    load(truck3, table.get(35))


# "deliver_packages" function to deliver the packages using the nearest-neighbor algorithm
def deliver_packages(table, truck, departure_time, driver):
    # variables to hold important data for the algorithm
    packages_delivered = []  # a list to hold the packages once they have been delivered
    hub = addresses['4001 South 700 East']  # a variable to hold the address of the hub
    current_location = hub  # a variable to hold the current location of the truck
    total_distance = 0.0  # a variable to hold the total distance covered by the truck
    total_time = departure_time  # a variable to hold the total time used by the truck

    # print a header for the UI
    print('---' + truck[0].truck + '---')
    print(str(departure_time) + ': ' + truck[0].truck + ' leaves the hub')

    # nearest-neighbor algorithm
    for i in range(0, len(truck)):  # loop through each package on the truck
        # variables to hold important data for the algorithm
        closest_distance = 100.0  # a variable to hold the closest distance for the truck to drive
        closest_location = None  # a variable to hold the closest location to the truck
        next_delivery = None  # a variable to hold the next package to be delivered

        # distance calculator
        for package in truck:  # loop through each package on the truck again for comparison purposes
            # variables to hold important data for the algorithm
            package.driver = driver  # assign the truck driver to each package on the truck
            package.loading_time = departure_time  # assign the departure time to the package
            package_address = addresses[
                table.get(package.package_id).address]  # a variable to hold the address of the package

            # find the distance between the package's address and the truck's current location
            try:
                distance = float(distances[package_address][current_location])
            except IndexError:  # a special error handling due to the unique design of the "WGUPS Distance Table" file
                distance = float(distances[current_location][package_address])
            if distance < closest_distance:  # if the distance is the closest one yet...
                # ...update the appropriate variables
                closest_distance = distance
                closest_location = package_address
                next_delivery = package

        # update the lists and variables
        packages_delivered.append(next_delivery)  # add the next delivery to the "packages_delivered" list
        truck.remove(next_delivery)  # remove the next delivery from the truck
        total_distance += closest_distance
        current_location = closest_location
        total_time += datetime.timedelta(
            hours=closest_distance / 18)  # The truck drives at 18 mph, so factor this into the time calculation

        next_delivery.delivery_time = total_time  # timestamp the delivered package with its delivery time
        print(str(total_time) + ': ' + next_delivery.truck + ' delivers package ' + str(
            next_delivery.package_id) + ' to address "' + next_delivery.address + '"')  # print an update to the UI
        updates(table, total_time)  # check for special updates regarding unique packages

    # return the truck to the hub and update the time and distance data accordingly
    return_to_hub = float(distances[current_location][hub])
    total_distance += return_to_hub
    total_time += datetime.timedelta(
        hours=return_to_hub / 18)  # The truck drives at 18 mph, so factor this into the time calculation
    print(str(total_time) + ': ' + packages_delivered[0].truck + ' returns to the hub')  # print an update to the UI

    # print the truck's statistics to the UI
    print()
    print(packages_delivered[0].truck + "'s total deliveries: " + str(len(packages_delivered)) + ' packages')
    print(packages_delivered[0].truck + "'s total distance: " + str(round(total_distance)) + ' miles')
    print(packages_delivered[0].truck + "'s total time: " + str(total_time - departure_time))

    # return the truck's total distance and total time for use by the UI
    return total_distance, total_time


# "Main" class that holds the primary UI that will interact with the user directly
class Main:
    # instantiate the hash table and the address and distance lists
    myTable = HashTable()
    add_packages(myTable)
    add_distances()

    # declare times for when each truck leaves the hub
    first_departure = datetime.timedelta(hours=8)
    second_departure = datetime.timedelta(hours=9, minutes=15)
    third_departure = datetime.timedelta(hours=10, minutes=30)

    # Actual UI starts here
    print('Welcome to the Western Governors University Parcel Service (WGUPS)')  # print a header to the user
    print()

    while True:  # loop the UI until the user quits the program
        input_key = input(
            'Please type in one of the options below:\n-) "d" - run delivery simulation\n-) "q" - quit\n')  # take an input key from the user
        if input_key == 'd':  # if the user wants to run the delivery simulation...
            # ...print a header
            print('Running delivery simulation...')
            print()

            # load the trucks and deliver the packages
            load_trucks(myTable)
            (truck_1_distance, truck_1_time) = deliver_packages(myTable, truck1, first_departure, 'Driver 1')
            print()
            (truck_2_distance, truck_2_time) = deliver_packages(myTable, truck2, second_departure, 'Driver 2')
            print()
            (truck_3_distance, truck_3_time) = deliver_packages(myTable, truck3, third_departure, 'Driver 1')
            print()

            # print the overall statistics for all three trucks
            print('Deliveries completed!')
            print('Total distance covered by all three trucks: ' + str(
                round(truck_1_distance + truck_2_distance + truck_3_distance)) + ' miles')
            print('Total time taken by all three trucks: ' + str(
                (truck_1_time - first_departure) + (truck_2_time - second_departure) + (
                        truck_3_time - third_departure)))
            print()

            # package lookup section of the UI
            while True:  # loop the UI until the user restarts the program
                next_input = input(
                    'Please type in one of the options below:\n-) "p" - print package data for a given time\n-) "r" - restart program\n')  # take an input key from the user
                if next_input == 'p':  # if the user wants to look up package data...
                    try:
                        input_time = input(
                            'Please enter a time in the following 24hr format: HH:MM:SS\n')  # take an input time from the user
                        (hours, minutes, seconds) = input_time.split(':')  # split the input into appropriate variables
                        lookup_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(
                            seconds))  # convert the user's input into a "timedelta" variable
                        select_key = input(
                            'Please type in one of the options below:\n-) "i" for an individual package\n-) "a" for all packages\n-) "q" to quit\n')  # take another input key from the user
                        if select_key == 'i':  # if the user just wants data for an individual package...
                            try:
                                package_input = int(input(
                                    'Please type in a package ID number: '))  # take an input package id from the user
                                package = myTable.get(
                                    package_input)  # find the package identified by the user in the hash table
                                package.update(lookup_time)  # update the package's data based on the given time
                                print_header()  # print a header with a key for the package data
                                print(str(package))  # print the package's data to the UI
                            except ValueError:  # if the user input an invalid ID number...
                                print('ERROR: Invalid input')  # print an error message
                                continue  # continue the loop
                        elif select_key == 'a':  # if the user wants data for all the packages at once...
                            print_header()  # ...print a header with a key for the package data
                            for package_id in range(1, 41):  # loop over each package in the hash table
                                package = myTable.get(package_id)  # find the package in the hash table
                                package.update(lookup_time)  # update the package's data based on the given time
                                print(str(package))  # print the package's data to the UI
                        elif select_key == 'q':  # if the user wants to quit the lookup...
                            continue  # ...continue the loop
                        else:  # if the user inputs an invalid value...
                            print('ERROR: Invalid input')  # ...print an error message
                            continue  # continue the loop
                    except ValueError:  # if the user inputs an invalid time...
                        print('ERROR: Invalid input')  # ...print an error message
                        continue  # continue the loop
                elif next_input == 'r':  # if the user wants to restart the program (return to the main menu)...
                    print('Restarting program...')  # ...print a message to the UI
                    break  # exit the inner loop
                else:  # if the user inputs an invalid value...
                    print('ERROR: Invalid input')  # ...print an error message
                    continue  # continue the loop
        elif input_key == 'q':  # if the user wants to quit the program...
            print('Have a nice day :)')  # ...print a message to the UI
            break  # exit the outer loop (exits the program)
        else:  # if the user inputs an invalid value...
            print('ERROR: Invalid input')  # ...print an error message
            continue  # continue the loop
