from utils import control_user_choice
from hash_check import hash_sub_menu
from url_check import review_analysis
from utils import CSV


def main():
    """
    Controls the main flow of the programme. Offers the user the choice of checking either:
    - Hash value via manual upload or generating a hash from a file within the same directory
    - File report on a URL which a user uploads manually

    This programme makes API calls to VirusTotal, in order to generate results.
    Results are saved to completed_searches.csv, for audit trailing and a permanent search history.

    Contains control flow and logic to keep the user from creating an error in the programme
    Uses control_user_choice from utils to allow users to safely navigate the Menu
    """

    # Initialise the CSV file - File used as an audit trail of hash/url searches
    CSV.initialise_csv()

    while True:
        print("\n --- Main Menu ---")
        print("1 - Get a file report on a hash value")
        print("2 - Get a file report on a URL")
        print("3 - Quit the programme.")

        user_choice = control_user_choice("Enter here: ", range(1,4))

        if not user_choice:
            print("Input cannot be empty. Please choose an option from the Menu 1-3.")
            continue

        if user_choice == 1:
            hash_sub_menu()

        elif user_choice == 2:
            review_analysis()

        elif user_choice == 3:
            print("Exiting programme... Goodbye!")
            break


if __name__ == "__main__":
    main()
