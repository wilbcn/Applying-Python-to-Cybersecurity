import csv
import os


class CSV:
    """
    CSV class handles our log 'completed_searches.csv', and contains class methods to add data to this file.
    """
    CSV_FILE = "completed_searches.csv"
    COLUMNS = ["date", "search", "query", "result"]

    # Initialise the CSV
    @classmethod
    def initialise_csv(cls):
        """
        Check the CSV file exists and with the correct headers
        :return:
        """
        try:
            if not os.path.exists(cls.CSV_FILE):
                with open(cls.CSV_FILE, mode="w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=cls.COLUMNS)
                    writer.writeheader()
        except Exception as e:
            print(f"Error initialising the CSV file: {e}")

    @classmethod
    def log_entry(cls, date, search, query, result):
        """
        Adds a new log entry after the user performs a search on a hash or url
        :param date: The date of the search
        :param search: The type of search (HASH/URL)
        :param query: The hash/url searched
        :param result: The result of the search
        :return:
        """

        # Format the result (dict) neatly for the CSV log entry
        format_result = ", ".join([f"{key}: {value}" for key, value in result.items()])

        new_entry = {
            "date": date,
            "search": search,
            "query": query,
            "result": format_result
        }

        # Take a dict and write it into the CSV file (CSV WRITER)
        try:
            with open(cls.CSV_FILE, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
                writer.writerow(new_entry)
            print("Entry added successfully.")
        except Exception as e:
            print(f"Error writing to CSV file: {e}")


def retry_func(prompt=" "):
    """
    A simple retry function providing the user the option to cancel a process or continue in the event the user
    inputs something by mistake or in an erroneous API call etc.
    """
    while True:
        try:
            print(f"1 - Continue: {prompt}")
            print("2 - Cancel")
            retry = int(input(f"Choice: "))
            if retry == 1:
                return True
            elif retry == 2:
                return False
            else:
                print("Please choose either 1 or 2.")
        except ValueError:
            print("Choice cannot be empty or text. Please choose a number.")


def control_user_choice(prompt, menu_range):
    """
    Validates user input to help navigate Menus and user sub menus throughout the programme.
    Range can be specified to neatly display the user menus
    Handles exceptions and errors when using menus and sub menus
    """
    while True:
        try:
            print(f"Please choose an option from the menu. {menu_range.start}-{menu_range.stop-1}")
            user_choice = input(prompt).strip()

            # Check for empty input
            if not user_choice:
                print("Choice cannot be empty. Please choose a number")
                continue

            # Check input is numeric
            if not user_choice.isdigit():
                print("Please choose a number from the Menu.")
                continue

            # Convert user choice to an integer
            user_choice = int(user_choice)

            # Check input is within the menu range of options
            if user_choice not in menu_range:
                print(f"Please choose a valid menu option: {menu_range.start}-{menu_range.stop-1}")
                continue

            # Return the user menu choice
            return user_choice

        except ValueError:
            print("An error has occurred, please try again with a valid number.")


