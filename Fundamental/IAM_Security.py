import boto3
import pandas as pd
import time
import os
from datetime import datetime, timedelta

def check_existing_report():
    """Checks if the credentials report has been generated or not"""
    if not os.path.exists("credentials_report.csv"):
        print("No credentials report was found. Please generate one!")
        return False
    return True
def get_credentials_report():
    """Creates a client to interact with AWS IAM service. String 'iam' specifies which service."""
    print("Creating client for AWS IAM Service")
    time.sleep(2)
    iam_client = boto3.client('iam')

    # This method requests AWS to create the report
    print("Generating User Credentials Report")
    while True:
        gen_iam_report = iam_client.generate_credential_report()
        if gen_iam_report['State'] == 'COMPLETE':
            print("Report generation status: COMPLETE")
            break
        else:
            print("Report generation is still in process..")
            time.sleep(3)

    # This method returns a dictionary containing various pieces of metadata and the actual report content.
    get_iam_report = iam_client.get_credential_report()
    # The report is encoded as binary. Here we decode it as grab the Contents via the Content Key.
    file_content = get_iam_report['Content'].decode('utf-8')
    return file_content

def transform_data():
    """Fetches the report, saves it to a file, and loads it into a Pandas DF"""
    report = get_credentials_report()

    # Save the report to a CSV file
    with open("credentials_report.csv", 'w') as file:
        file.write(report)
    print("Report was saved as credentials_report.csv")
    time.sleep(2)

def users_without_mfa():
    """Identifies and prints out users without MFA enabled"""
    if not check_existing_report():
        return

    user_data = pd.read_csv("credentials_report.csv")
    # Empty list to add users without MFA
    users_without_mfa = []
    # Iterate over each row in the DataFrame
    for index, row in user_data.iterrows():
        if row['mfa_active'] == False:
            users_without_mfa.append({'user': row['user'],'mfa_active': row['mfa_active'], 'arn': row['arn']})

    print("Calculating..")
    time.sleep(2)
    if not users_without_mfa:
        print("All users have MFA enabled!")
        time.sleep(2)
        return None

    print("Users without MFA enabled:")
    for index, user in enumerate(users_without_mfa,start=1):
        print(index, user)
        time.sleep(2)
    time.sleep(2)
def check_user_passwords():
    """Identifies users that have passwords older than 2 months."""
    if not check_existing_report():
        return

    user_data = pd.read_csv("credentials_report.csv")
    # Get today's date and also set the 2-month difference
    today = datetime.now()
    two_months_ago = today - timedelta(days=60)
    list_of_users = [] # Store users who have not changed their password in 2 months

    for index, row in user_data.iterrows():
        if pd.isna(row['password_last_changed']): # Skips rows to avoid errors with null values
            continue

        last_changed = datetime.strptime(row['password_last_changed'], "%Y-%m-%dT%H:%M:%SZ")
        if last_changed < two_months_ago:
            list_of_users.append({'user': row['user'], 'password_last_changed': row['password_last_changed']})

    print("Calculating..")
    time.sleep(2)
    if not list_of_users:
        print("There are no users with passwords older than 2 months.")
        return None
    print("Displaying users with passwords older than 2 months")
    for index, user in enumerate(list_of_users,start=1):
        print(index, user)
        time.sleep(2)
    time.sleep(2)
    
def security_sub_menu():
    print("Here you can check for security concerns for IAM Users.")
    time.sleep(2)

    while True:
        try:
            print("Menu options")
            print("1 - Check IAM users without MFA")
            print("2 - Check IAM user passwords")
            print("3 - Not sure yet")
            print("4 - Return to Main Menu")
            user_choice= int(input("Enter here: "))

            if user_choice == 1:
                users_without_mfa()

            elif user_choice == 2:
                check_user_passwords()
                time.sleep(2)
                break

            elif user_choice == 3:
                print("Not yet")
                time.sleep(2)
                break

            elif user_choice == 4:
                print("Returning to Main Menu")
                time.sleep(2)
                break
            else:
                print("Invalid Menu Choice. Please select a number from the Menu.")

        except ValueError:
            print("Menu choice must be a number.")
def security_menu():
    print("Main Menu")
    print("Choose an option to continue")

    while True:
        try:
            print("1 - Generate new user report")
            print("2 - Check for security concerns")
            print("3 - Quit")
            user_choice = int(input("Enter here: "))
            if user_choice == 1:
                transform_data()
                continue

            elif user_choice == 2:
                security_sub_menu()

            elif user_choice == 3:
                print("Exiting programme..")
                time.sleep(2)
                break

            else:
                print("Invalid Menu Choice. Please select a number from the Menu.")
        except ValueError:
            print("Menu choice must be a number.")

def main():
    security_menu()

if __name__ == "__main__":
    main()

