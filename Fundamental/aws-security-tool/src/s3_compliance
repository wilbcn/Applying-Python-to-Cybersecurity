import boto3
import pandas as pd
import time
import os
from datetime import datetime, timedelta, timezone

class S3Compliance:
    """Handles S3 Compliance checks."""

    def __init__(self):
        self.s3_client = boto3.client('s3')  # Initialise the S3 client

    def list_s3_buckets(self):
        """Lists the S3 buckets in our AWS account"""

        my_buckets = self.s3_client.list_buckets()
        bucket_list = []

        for bucket in my_buckets['Buckets']:
            bucket_name = bucket['Name']
            bucket_list.append(bucket_name)

        return bucket_list

    def is_bucket_public(self):
        """Checks if the S3 Bucket is publicly accessible."""

        # Get the list of Buckets
        my_buckets = self.list_s3_buckets()
        public_buckets = []

        try:
            for bucket in my_buckets:
                acl = self.s3_client.get_bucket_acl(Bucket=bucket)

                # Check the ACL for public access
                for grant in acl['Grants']:
                    grantee = grant.get('Grantee', {})
                    permission = grant.get('Permission', "")

                    if grantee.get('Type') == 'Group':
                        if grantee.get('URI') == "http://acs.amazonaws.com/groups/global/AllUsers":
                            # Add the offending bucket to our public bucket list.
                            public_buckets.append({'bucket_name': bucket, 'permission': permission})

        except Exception as e:
            print(f"Error checking status of bucket {e}")

        if public_buckets:
            print("Displaying S3 Buckets with public access security concerns.")
            time.sleep(2)
            for bucket in public_buckets:
                print(f"Bucket: {bucket['bucket_name']} is publicly accessible.")
                print(f"Reason: A permission in its ACL: {bucket['permission']},"
                      f" allows public access.")
                print("Review and update this buckets ACL to restrict public access.\n")
                time.sleep(2)
        else:
            print("There were no buckets identified with public access security concerns")
            time.sleep(2)

        time.sleep(3)
        print("Returning to S3 Menu..")
        time.sleep(3)

    def check_bucket_has_encryption(self):
        """Checks if our S3 Buckets have encryption enabled."""

        my_buckets = self.list_s3_buckets()
        print("Data stored in S3 should be encrypted for data confidentiality,"
              " compliance, and risk mitigation.")
        time.sleep(3)
        print("Displaying encryption information on your S3 buckets:")
        time.sleep(2)

        try:
            for bucket in my_buckets:
                response = self.s3_client.get_bucket_encryption(Bucket=bucket)
                item = response['ServerSideEncryptionConfiguration']

                for rule in item['Rules']:
                    encryption = rule['ApplyServerSideEncryptionByDefault']
                    bucket_key = rule['BucketKeyEnabled']

                    print(f"Bucket: {bucket} has encryption enabled {encryption}"
                          f" and default bucket key enabled: {bucket_key}.\n")
                    time.sleep(2)

            time.sleep(2)
            print("Investigate any buckets that do not have at least the default 'server side"
                  " encryption' enabled.")

            print("Returning to S3 Main Menu..")
            time.sleep(2)

        except Exception as e:
            print(f"Error {e}")

    def check_bucket_version(self):
        """Checks S3 buckets for bucket versioning enabled"""

        print("Checking your S3 buckets..")
        time.sleep(2)
        my_buckets = self.list_s3_buckets()
        print("Bucket versioning ensures data protection and recovery. Investigate"
              " any buckets without versioning enabled.")
        time.sleep(3)

        for bucket in my_buckets:
            response = self.s3_client.get_bucket_versioning(Bucket=bucket)

            if 'Status' not in response:
                print(f"Bucket versioning is not configured in this bucket: {bucket}")
                time.sleep(2)

            else:
                status = response['Status']

                if status == 'Enabled':
                    print(f"Bucket {bucket} has bucket versioning enabled.")

                elif status == 'Suspended':
                    print(f"Bucket {bucket} has bucket versioning suspended.")

        print("Returning to S3 Main Menu..")
        time.sleep(2)

    def s3_sub_menu(self):
        """Provides a sub menu for checking S3 security concerns."""
        print("Loading S3 menu..")
        time.sleep(2)
        print("Choose an option from the Menu.")

        while True:
            try:
                print("1 - Check for S3 Public Access")
                print("2 - Check S3 Buckets have encryption")
                print("3 - Check for S3 versioning enabled")
                print("4 - Main Menu")
                user_choice = int(input("Enter here: "))

                if user_choice == 1:
                    self.is_bucket_public()

                elif user_choice == 2:
                    self.check_bucket_has_encryption()

                elif user_choice == 3:
                    self.check_bucket_version()

                elif user_choice == 4:
                    print("Returning to Main Menu")
                    time.sleep(2)
                    break

                else:
                    print("Invalid menu choice. Please choose a number from the options.")

            except ValueError:
                print("Invalid input. Please enter a number.")
