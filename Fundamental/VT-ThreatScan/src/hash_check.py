import requests
import json
from utils import control_user_choice, retry_func
from datetime import datetime
import os
from dotenv import load_dotenv
import hashlib
from utils import CSV
import time

def validate_hash():
    """
    Asks the user to insert manually the hash file to later generate a report for.
    Validates this hash, by comparing the length of it, to our hash_lengths dictionary
    This dictionary sets the length parameters for the hash types available at VirusTotal

    :return: Returns the inserted hash as a str
    """

    hash_lengths = {
        "MD5": 32,
        "SHA-1": 40,
        "SHA-256": 64
    }

    # Display the available hash types and their expected character lengths
    print("\nPlease select the hash you would like to check. (1,2,3)")
    for index, (hash_name, length) in enumerate(hash_lengths.items(), start=1):
        print(f"{index} - Hash: {hash_name}, Expected length: {length}")

    select_hash = control_user_choice("Enter here: ", range(1,4))
    if 1 <= select_hash <= len(hash_lengths):
        # Map the users choice (index) to a hash and its char length limit
        hash_name, length = list(hash_lengths.items())[select_hash -1]  # -1 for 0 based indexing

        # Get the hash value from the user and validate it via its length
        while True:
            print("\nPlease type or paste in your hash to check.")
            user_hash = input("Hash: ").strip()

            if not user_hash:
                print("Hash cannot be empty. Please try again")
                continue

            if len(user_hash) == length:
                print(f"\n{hash_name} hash been accepted.")
                return user_hash
            else:
                print(f"The entered hash does not match the expected character length: {len(user_hash)}/{length}")
                if not retry_func("Enter a new hash"):
                    return None


def find_local_files():
    """
    Creates an empty list list_of_files and adds to it all identified files within the same directory
    as this programme. Ignores files that are in the ignore_files list, such as .py files.

    :return: Returns our list of intended files for potential file scan via VirusTotal
    """
    list_of_files = []  # Get files to check that are separate from the programme != .py

    # List the files that are in the current directory
    local_files_in_directory = os.listdir(".")

    # Filter to extract only files and not directories
    files_to_check = [f for f in local_files_in_directory if os.path.isfile(f)]

    # Skip files related to programme 
    for file in files_to_check:
        if ".py" in file or ".env" in file:
            continue
        list_of_files.append(file)

    if not list_of_files:
        print("No files to check")
        return None

    return list_of_files


def select_file():
    """
    Grabs our list of files and displays them to the user, leveraging enumerate so that the user can clearly choose
    the file they want to proceed with.
    :return: Returns the file the user has chosen to check
    """
    list_of_files = find_local_files()
    if list_of_files is None:
        return

    for index, file in enumerate(list_of_files, start=1):
        print(f"{index} - {file}")

    while True:
        try:
            print("Choose the file you wish to check i.e. 1")
            user_choice = int(input("File number: "))

            if 1 <= user_choice <= len(list_of_files):
                file_to_check = list_of_files[user_choice - 1]
                return file_to_check

            else:
                print("No file found at that index. Please try again")

        except ValueError:
            print("Invalid input. Please enter a number corresponding to a file.")


def gen_file_hash(algorithm="sha256"):
    """
    Generates a sha256 hash for the selected file chosen by the user.
    :return: Returns it as a str to be used in generating the report.
    """

    file_to_check = select_file()

    if file_to_check is None:
        return

    try:
        new_hash = hashlib.new(algorithm)
        with open(file_to_check, "rb") as f:
            while chunk := f.read(8192):
                new_hash.update(chunk)

        validated_hash = new_hash.hexdigest()
        string_hash = str(validated_hash)
        print(f"Generating SHA256 hash for the selected file '{file_to_check}'")
        print(f"SHA256 Hash: {string_hash}")
        return string_hash

    except Exception as e:
        print(f"An error occurred as: {e}")


def get_hash_report(hash_values, manual_or_file):
    """
    Makes an API call to VirusTotal, using the hash manually inserted from the user, or generated from a local file.

    Works through the response file and appends crucial information to our dict. We then call the log_entry method from
    CSV in order to create a log of this search.

    :param manual_or_file: Specifies whether the hash was inserted manually by the user, or generated from a local file
    :param hash_values: The hash itself as a str
    :return: Returns false only if the user would not like to recheck another file, taking you back to the Main Menu
    """
    url = "https://www.virustotal.com/api/v3/files/"
    hash_to_check = hash_values
    complete_url = url + hash_to_check

    # Securely load the API key
    load_dotenv()
    api_key = os.getenv('VT_API_KEY')

    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }

    response = requests.get(complete_url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} from the API call.")
        return False

    response_data = json.loads(response.text)
    time.sleep(6)  # Allows enough time for the API call.
    hash_info = response_data['data']['attributes']

    if not hash_info:
        print(f"Unable to retrieve information about this hash.")
        return False

    # Extract and display key information back to the user.
    print("\n--- Displaying General Hash information ---")
    print(f"Hash: {hash_to_check}")
    print(f"Name: {hash_info.get('meaningful_name', 'N/A')}")
    print(f"Description: {hash_info.get('magic', 'N/A')}")
    print(f"File Type: {hash_info.get('type_description', 'N/A')}")
    print(f"Size: {hash_info.get('size', 'N/A')} bytes")

    # Convert the first/last seen data into a readable format
    first_seen = hash_info.get('first_submission_date', 'N/A')
    validate_first_seen = datetime.utcfromtimestamp(first_seen).strftime('%d-%m-%Y %H:%M:%S')
    last_seen = hash_info.get('last_analysis_date', 'N/A')
    validate_last_seen = datetime.utcfromtimestamp(last_seen).strftime('%d-%m-%Y %H:%M:%S')

    print(f"First Seen: {validate_first_seen} ")
    print(f"Last Seen: {validate_last_seen}")
    print("\n")
    print("--- Displaying hash analysis results ---")
    last_analysis_info = hash_info['last_analysis_stats']
    last_analysis_results = hash_info['last_analysis_results']['Bkav']

    # Get the total engines
    total_engines = (
            last_analysis_info.get('malicious', 0) +
            last_analysis_info.get('suspicious', 0) +
            last_analysis_info.get('undetected', 0) +
            last_analysis_info.get('harmless', 0) +
            last_analysis_info.get('timeout', 0)
    )

    malicious_count = last_analysis_info.get('malicious', 0)
    suspicious_count = last_analysis_info.get('suspicious', 0)
    undetected_count = last_analysis_info.get('undetected', 0)
    category = last_analysis_info.get('category', 'N/A')
    result = last_analysis_info.get('result', 'N/A')

    print(f"Malicious count: {malicious_count}/{total_engines}")
    print(f"Suspicious count: {suspicious_count}/{total_engines}")
    print(f"Undetected count: {undetected_count}/{total_engines}")
    print(f"Category: {category}")
    print(f"Result: {result}")
    print("\nAnalysis Complete....\n")

    info_to_log = {
        "Hash name": hash_info.get('meaningful_name', 'N/A'),
        "Description": hash_info.get('magic', 'N/A'),
        "First Seen": validate_first_seen,
        "Last Seen": validate_last_seen,
        "Total Engines checked": total_engines,
        "Malicious Count": malicious_count,
        "Suspicious Count": suspicious_count,
        "Undetected Count": undetected_count,
        "Result": result
    }

    # Log the hash search
    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    if manual_or_file == "manual":
        CSV.log_entry(date, "Hash", hash_values, info_to_log)
    elif manual_or_file == "file":
        CSV.log_entry(date, "File", hash_values, info_to_log)

    print("This search has been saved to the log file 'complete_searches.csv'")

    print("Would you like to look up another file?")
    if not retry_func():
        return False
    return


def hash_sub_menu():
    """
    Provides the user with a Hash Sub Menu, for choosing how they would like to generate a file report on a hash.
    :return: N/A
    """
    while True:
        print("\n--- Hash Sub Menu ---")
        print("1 - Insert hash manually")
        print("2 - Check existing file")
        print("3 - Cancel process")

        user_choice = control_user_choice("Enter here: ", range(1, 4))

        if user_choice == 1:
            get_hash = validate_hash()
            if get_hash is None:
                return
            gen_report = get_hash_report(get_hash, manual_or_file="manual")
            if gen_report is False:
                return

        elif user_choice == 2:
            file_hash = gen_file_hash()
            hash_report = get_hash_report(file_hash, manual_or_file="file")
            if hash_report is False:
                return

        elif user_choice == 3:
            return
