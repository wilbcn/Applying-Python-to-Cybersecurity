import boto3
import pandas as pd
import time
import os
from datetime import datetime, timedelta, timezone


class IamSecurity:
    """Handles IAM related security checks."""

    def __init__(self):
        self.iam_client = boto3.client('iam')  # Initialise the IAM client
        self.last_report_generated_time = None  # Initialise a timestamp variable

    @staticmethod  # Does not depend on any instance-specific data (self)
    def check_existing_report():
        """Checks if the credentials report has been generated or not"""
        if not os.path.exists("credentials_report.csv"):
            print("No credentials report was found. Please generate one!")
            return False
        return True

    def iam_credentials_report(self):
        """Generates a Credential Report for all IAM Users."""

        print("Getting the credentials report from AWS...")
        time.sleep(2)

        while True:
            try:
                gen_iam_report = self.iam_client.generate_credential_report()
                if gen_iam_report['State'] == 'COMPLETE':
                    print("Report generation status: COMPLETE")
                    # Save the current time that the report was generated
                    self.last_report_generated_time = datetime.now()
                    break
                else:
                    print("Report generation is still in process..")
                    time.sleep(3)

            except self.iam_client.exceptions.LimitExceededException as e:
                print(f"API call limit has been exceeded. {e}")
                break

            except self.iam_client.exceptions.ServiceFailureException as e:
                print(f"API call has failed. Try again later.")
                print(f"Failure encountered: {e}")
                break

            except Exception as e:
                print(f"An error has occurred: {e}")
                break

        # This method returns a dictionary containing various pieces of metadata and the actual report content.
        get_iam_report = self.iam_client.get_credential_report()
        # The report is encoded as binary. Here we decode it as grab the Contents via the Content Key.
        file_content = get_iam_report['Content'].decode('utf-8')
        return file_content

    def transform_data(self):
        """Fetches the report, saves it to a file, and loads it into a Pandas DF"""
        report = self.iam_credentials_report()

        # Save the report to a CSV file
        with open("credentials_report.csv", 'w') as file:
            file.write(report)
        print("Report was saved as credentials_report.csv")
        time.sleep(2)
        print("Returning to IAM Menu..")
        time.sleep(2)

    def users_without_mfa(self):
        """Identifies and prints out users without MFA enabled"""

        # Checks that a credentials report exists.
        if not self.check_existing_report():
            print("Please generate a IAM credentials report first.")
            time.sleep(2)
            return None

        user_data = pd.read_csv("credentials_report.csv")
        # Empty list to add users without MFA
        users_without_mfa = []
        # Iterate over each row in the DataFrame
        for index, row in user_data.iterrows():
            if row['mfa_active'] == False:
                users_without_mfa.append({'user': row['user'], 'mfa_active': row['mfa_active'], 'arn': row['arn']})

        print("Calculating..")
        time.sleep(2)
        if not users_without_mfa:
            print("All users have MFA enabled!")
            time.sleep(2)
            return None

        print("Users without MFA enabled:")
        for index, item in enumerate(users_without_mfa, start=1):
            print(f"\n{index} - {item['user']}: MFA Status: {item['mfa_active']}")

        time.sleep(3)
        print("Configure MFA for these users!")
        time.sleep(3)
        print("Returning to IAM Menu..")
        time.sleep(3)

    def check_for_old_passwords(self):
        """Identifies users that have passwords older than 2 months."""

        # Checks that a credentials report exists.
        if not self.check_existing_report():
            print("Please generate a IAM credentials report first.")
            time.sleep(2)
            return None

        user_data = pd.read_csv("credentials_report.csv")
        # Get today's date and also set the 2-month difference
        today = datetime.now()
        two_months_ago = today - timedelta(days=60)
        list_of_users = []  # Store users who have not changed their password in 2 months

        for index, row in user_data.iterrows():
            if pd.isna(row['password_last_changed']):  # Skips rows to avoid errors with null values
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
        for index, item in enumerate(list_of_users, start=1):
            print(f"\n{index} - User: {item['user']}\nPassword last changed: {item['password_last_changed']}")
        time.sleep(4)
        print("Please investigate and prompt these users to update their passwords.")
        time.sleep(3)
        print("Returning to IAM Menu..")
        time.sleep(3)

    def list_aws_users(self):
        """Provides us with a list of our aws users"""

        show_users = self.iam_client.list_users()
        my_users = []

        for user in show_users['Users']:
            user_name = user['UserName']
            my_users.append(user_name)

        # Returns a list of our AWS users.
        return my_users

    def list_aws_groups(self):
        """Provides us with a list of our aws groups"""

        show_groups = self.iam_client.list_groups()
        my_groups = []

        for group in show_groups['Groups']:
            group_name = group['GroupName']
            my_groups.append(group_name)

        # Returns a list of our AWS Groups
        return my_groups

    def check_attached_user_policies(self):
        """Lists the attached policies on our aws users"""

        aws_users = self.list_aws_users()  # Get all aws users
        attached_policies = {}

        for user in aws_users:
            get_list = self.iam_client.list_attached_user_policies(UserName=user)

            # Ensure the user is there even with an empty list if no policies
            attached_policies[user] = attached_policies.get(user, [])

            # Add the users policies to their list in the dict.
            for item in get_list['AttachedPolicies']:
                policy = item['PolicyName']
                attached_policies[user].append(policy)

        # Output users and policies if they have policies.
        for user, policies in attached_policies.items():
            print(f"For user: {user}")

            if policies:
                print(f"Attached policies are: {policies}")
            else:
                print("There were no attached policies found.")
                time.sleep(3)
                continue

        return attached_policies

    def check_attached_group_policies(self):
        """Checks which managed policies are attached to our groups"""

        iam_groups = self.list_aws_groups()
        admin_groups = {}

        for group in iam_groups:
            group_policies = self.iam_client.list_attached_group_policies(GroupName=group)

            for item in group_policies['AttachedPolicies']:
                policy = item['PolicyName']

                if policy == 'AdministratorAccess':
                    # Only add the group to admin_groups if it has AdministratorAccess
                    admin_groups[group] = admin_groups.get(group, [])
                    admin_groups[group].append(policy)

        print("Displaying groups found..")
        time.sleep(2)
        for group, policy in admin_groups.items():
            print(f"\nGroup name: {group} - Attached policies: {policy}")
            time.sleep(1)
        time.sleep(3)

        return admin_groups

    def users_in_admin_groups(self):
        """Identify which users are part of Admin groups"""

        aws_users = self.list_aws_users()  # Get all AWS Users
        groups_with_admin_access = self.check_attached_group_policies()  # Get Admin groups with Admin access

        users_with_admin = []  # List to store users that have admin access

        for user in aws_users:
            # Get the groups all users belong to
            user_groups = self.iam_client.list_groups_for_user(UserName=user)

            # Get the GroupName each user is part of.
            print("Checking for users in found groups")
            time.sleep(3)
            for group in user_groups['Groups']:
                group_name = group['GroupName']

                if group_name in groups_with_admin_access:  # Python interprets this as .keys() by default.
                    users_with_admin.append(user)
                    print(f"\nUser {user} has Admin privileges because they belong to group {group_name}.")
                    time.sleep(1)
                time.sleep(3)

            return users_with_admin

        if not users_with_admin:
            print("No users were found with Admin privileges.")
            return None

    def check_for_admin(self):
        """Calls our various methods to look for Admin privileges in our aws users/groups."""

        print("Checking for Admin rights via attached user policies")
        time.sleep(3)
        self.check_attached_user_policies()
        time.sleep(4)
        print("Checking for Admin rights via IAM Groups.")
        time.sleep(3)
        admin_via_group = self.users_in_admin_groups()
        if admin_via_group:
            print("Verify that these users should have Admin rights via their group.")
            time.sleep(3)
        else:
            print("Verify there are 0 users with Admin rights via groups.")
            time.sleep(3)

        print("Returning to IAM Main Menu..")
        time.sleep(3)

    def check_access_keys(self):
        """
        Checks the access keys of IAM users and outputs users with keys older than 2 months
        Also checks access keys that have not been used in the last two months
        """

        print("It is recommended to change IAM users access keys every 90 days or less. Many"
              " compliance frameworks require regular credential rotation.")
        time.sleep(4)
        print("Checking access keys..")
        time.sleep(3)
        today = datetime.now(timezone.utc)
        two_months_ago = today - timedelta(days=60)

        iam_users = self.list_aws_users()

        for user in iam_users:
            response = self.iam_client.list_access_keys(UserName=user)

            for data in response['AccessKeyMetadata']:
                key_id = data.get('AccessKeyId')
                status = data.get('Status')
                date = data.get('CreateDate')

                if date < two_months_ago:
                    print(f"The access key for user: {user} has not been changed in"
                          f" over two months. Last changed: {date}. Status: {status}.")
                    time.sleep(3)

                response_2 = self.iam_client.get_access_key_last_used(AccessKeyId=key_id)

                #  Here .get incase key has not been used.
                last_used = response_2['AccessKeyLastUsed'].get('LastUsedDate')
                if last_used:
                    if last_used < two_months_ago:
                        print(f"The access key for user: {user} has not been used in over two months. Last"
                              f" used date {last_used}")

        print("Please check any flagged users with old or inactive access keys.")
        time.sleep(3)
        print("Returning to IAM Main Menu..")
        time.sleep(3)

    def iam_sub_menu(self):
        """Provides a sub menu for checking IAM security concerns."""
        print("Loading IAM menu..")
        time.sleep(2)
        print("Choose an option from the Menu.")

        while True:
            try:
                last_generated = (
                    self.last_report_generated_time.strftime("%Y-%m-%d %H:%M:%S")
                    if self.last_report_generated_time
                    else "Never"
                )
                print(f"1 - Generate Credentials Report. (Last Generated: {last_generated})")
                print("2 - Check for users without MFA.")
                print("3 - Check for old passwords.")
                print("4 - Verify Admin access.")
                print("5 - Check access keys.")
                print("6 - Main Menu.")
                user_choice = int(input("Enter here: "))

                if user_choice == 1:
                    # Downloads a credentials report and prepares it for our other methods.
                    self.transform_data()

                elif user_choice == 2:
                    # Checks users in the credentials report to see if they have MFA enabled or not.
                    self.users_without_mfa()

                elif user_choice == 3:
                    self.check_for_old_passwords()

                elif user_choice == 4:
                    self.check_for_admin()

                elif user_choice == 5:
                    self.check_access_keys()

                elif user_choice == 6:
                    print("Returning to Main Menu")
                    time.sleep(2)
                    break

                else:
                    print("Invalid menu choice. Please choose a number from the options.")

            except ValueError:
                print("Invalid input. Please enter a number.")
