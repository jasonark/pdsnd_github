import time
import pandas as pd
import numpy as np

# Define files to be used in this program
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    while True:
        try:
            global city  # Set global variable for city to be used in raw_data function
            city = input("Please enter a city you would like to see bikeshare data for:\nChicago\nNew York City\nWashington\n")
            city = city.lower()  # Set user input to lower case so that case won't matter for user input
            if city in CITY_DATA.keys():
                break  # Will break out of loop if valid city is chosen
            else:
                print("\nThat's not a valid city\n")  # Print message if invalid city is entered and return to beginning of loop
        except ValueError:
            print("Please only enter letters")  # Will print message if string data isn't entered and return to beginning of loop

    # Get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please enter the number for the month you would like to see data for. Data can be viewed from January - June (1 - 6).\nExample: January = 1, February = 2, etc.\nYou can enter all if you would like to see the data for all months.\n")
            if month == "1" or month == "2" or month == "3" or month == "4" or month == "5" or month == "6" or month == "all":
                break  # Will break out of loop if valid month is chosen
            else:
                print("\nThat's not a valid month\n") # Will print message if invalid month is entered and start over loop
        except ValueError:
            print("Invalid string") # Will print message if the expected data type isn't entered (string)

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Please enter a day of the week that you would like to see data for.  (Example: Monday, Tuesday, etc.)\nYou can enter all if you would like to see the data for all days of the week\n")
            day = day.lower()  # Set user input to lower case so that case won't matter for user input
            if day == "monday" or day == "tuesday" or day == "wednesday" or day == "thursday" or day == "friday" or day == "saturday" or day == "sunday" or day == "all":
                break  # Will break out of loop if valid city is chosen
            else:
                print("\nThat's not a valid day of the week\n")  # Will print message if invalid day is entered and start over loop
        except ValueError:
            print("Please only enter letters")  # Will print message if the expected data type isn't entered (string)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA.get(city))  # creates Pandas dataframe from file chosen by user
    df['Start Time'] = pd.to_datetime(df['Start Time'])  # converts column 'Start Time' to datetime format
    df['End Time'] = pd.to_datetime(df['End Time'])  # converts column 'End Time' to datetime format
    df['Month'] = df['Start Time'].dt.month  # extracts the month from the 'Start Time' column
    if month != "all":
        df = df[df["Start Time"].dt.month == int(month)]  # filters dataframe to only include month that user chose
    #  Extract the day of week from 'Start Time' column and put it in new column 'Day Of Week'
    df['Day Of Week'] = df['Start Time'].dt.strftime('%A')
    if day != "all":
        df = df[df["Day Of Week"] == day.title()]  # filters dataframe to only include day of week that user chose
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    Most_Common_Month = str(df[["Month"]].mode())[-1]
    print("The most common month is: {}".format(Most_Common_Month))
    # Display the most common day of week
    Most_Common_Day = str(df[["Day Of Week"]].mode())
    Most_Common_Day = Most_Common_Day.split()[-1]
    print("The most common day is: {}".format(Most_Common_Day))

    # Display the most common start hour
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

# Find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    # Sets "Start Station" column to string data type and returns the most common Start Station
    Most_Common_Start_Station = str(df[["Start Station"]].mode())
    # Filters out some unnecessary output to clean data
    Most_Common_Start_Station = Most_Common_Start_Station[Most_Common_Start_Station.find("0")+1:]
    #  Prints most commonon start station in clean format
    print("The most commonly used start station is: {}".format(Most_Common_Start_Station))


    # Display most commonly used end station
     # Sets "Most_Common_End_Station" column to string data type and returns the most common End Station
    Most_Common_End_Station = str(df[["End Station"]].mode())
    # Filters out some unnecessary output to clean data
    Most_Common_End_Station = Most_Common_End_Station[Most_Common_End_Station.find("0")+1:]
    #  Prints most commonon end station in clean format
    print("The most commonly used end station is: {}".format(Most_Common_End_Station))

    # Display most frequent combination of start station and end station trip
    # Create new dataframe to only include the columns "Start Station" and "End Station"
    df1 = df[["Start Station", "End Station"]]
    # Create new dataframe to only include rows where the columns "Start Station" and "End Station" are the same
    df2 = df[df1.eq(df1.iloc[:, 0], axis=0).all(axis=1)]
    # Converts column "Start Station" in new df2 dataframe to string and returns the mode of this column.
    Most_Common_Start_End = str(df2[["Start Station"]].mode())
    # Filters out some unnecessary output to clean data
    Most_Common_Start_End = Most_Common_Start_End[Most_Common_Start_End.find("0")+1:]
    #  Prints most commonon combination of start station and end station in clean format
    print("The most frequent combination of start start station and end station trip is: {}".format(Most_Common_Start_End))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    Total_Travel_Time = df["Trip Duration"].sum()
    print("The total travel time in seconds is: {}".format(Total_Travel_Time))
    # Display mean travel time
    Mean_Travel_Time = df["Trip Duration"].mean()
    print("The mean travel time in seconds is: {}".format(Mean_Travel_Time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    User_Type_Counts = df["User Type"].value_counts()
    print("Below are the counts for each of the user types:\n\n{}\n".format(User_Type_Counts)[:-30])

    # Display counts of gender for all cities except Washington
    if city != "washington":
        # Creates new dataframe and replaces Null values with the text "Unspecified"
        df1 = df[["Gender"]].fillna("Unspecified", inplace=False)
        # Sets new variable include a count of each of the different values in the "Gender" column
        Gender_Counts = df1["Gender"].value_counts()
        # Prints a count for each gender in a clean format
        print("Below are the counts for each gender:\n\n{}\n".format(Gender_Counts)[:-27])


    # Display earliest, most recent, and most common year of birth for all cities except Washington
    if city != "washington":

        df1 = df["Birth Year"]  # Creates new dataframe with only the "Birth Year" column
        df1 = df1[~pd.isnull(df1)]  # Removes null values from new dataframe
        Birth_Year = np.array(df1)  # Creates numpy array of new df1 dataframe
        # Only include values in array that are >= 1940 and <= 2000 to filter out erroneous data
        Birth_Year = Birth_Year[np.logical_and(Birth_Year>=1940,Birth_Year<=2000)]

        Min_Birth_Year = int(np.min(Birth_Year)) # Returns the earliest birth year in new variable
        print("The earliest birth year is {}.".format(Min_Birth_Year)) # Prints earliest birth year

        Max_Birth_Year = int(np.max(Birth_Year)) # Returns the latest birth year in new variable
        print("The most recent birth year is {}.".format(Max_Birth_Year)) # Prints latest birth year

        Mode_Birth_Year = int(df["Birth Year"].mode()) # Returns the most common birth year in new variable
        print("The most common year of birth is {}.".format(Mode_Birth_Year)) # Prints most common birth year


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ Displays raw data 5 lines at a time if user wishes. """
    # Begin first loop
    while True:
        try:
            # Ask user if they want to see raw data
            user_input = input("Would you like to see the raw data?  Please enter Yes or No.\n")
            # Set user input to lower case so that case won't matter
            user_input = user_input.lower()
            # Begin conditions based on user input
            if user_input == "yes":
                # Open data file that user chose in the beginning if the users chooses to view raw data
                with open((CITY_DATA.get(city)), "r") as file:
                    # Returns a list of all lines in the file and returns that list in a new variable 'lines'
                    lines=file.readlines()
                    # Sets start_line variable to 0 to begin with reading from the first line of the file
                    start_line = 0
                    # Sets end_line variable to 5 to read to the 5th line (index 4) of the file
                    end_line = 5
                    # Prints the first 5 lines of the file
                    print(lines[start_line:end_line])
                    # Begin second loop
                    while True:
                        try:
                            # Asks user if they would like to see additional raw data
                            user_input_q2 = input("Would you like to see additional raw data?  Please enter Yes or No.\n")
                            # Sets user input to lower case so that case won't matter in user response
                            user_input_q2 = user_input_q2.lower()
                            # Begin conditions on user input
                            if user_input_q2 == "yes":
                                # Increment start_line variable by 5 to start reading from where previously left off
                                start_line += 5
                                # Increment end_line variable by 5 to stop reading 5 lines from new value of start_line variable
                                end_line += 5
                                # Print next 5 lines of file
                                print(lines[start_line:end_line])
                            elif user_input_q2 == "no":
                                # End 2nd loop if user enters "no"
                                break
                            else:
                                # Print message if user enters invalid response
                                print("\nPlease enter Yes or No.\n")
                        except ValueError:
                            # Print message if user enters invalid data type (different than string)
                            print("Please only enter letters")
            elif user_input == "no":
                # Break from 1st loop if user doesn't wish to view raw data
                break
            else:
                # Print message if user enters invalid response
                print("\nPlease enter Yes or No.\n")
        except ValueError:
            # Print message if user enters invalid data type (different than string)
            print("Please only enter letters")






def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Please enter Yes or No.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
