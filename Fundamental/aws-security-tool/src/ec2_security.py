import boto3
import pandas as pd
import time
import os
from datetime import datetime, timedelta, timezone

class EC2Security:
    """Handles EC2 security checks."""
    def __init__(self):
        self.ec2_client = boto3.client('ec2')

    def list_security_groups(self):
        """Lists all our security groups with key information"""

        my_security_groups = self.ec2_client.describe_security_groups()
        print("Finding security groups in your AWS account..")
        time.sleep(2)
        # Access Key SecurityGroups with data
        for sg in my_security_groups['SecurityGroups']:
            print(f"\nSecurity Group: {sg['GroupId']}. Group Name: {sg['GroupName']}")
            # Access nested keys within SecurityGroups -> IpPermissions -> Keys
            for rule in sg['IpPermissions']:
                print(f"Protocol: {rule.get('IpProtocol')}")
                print(f"From Port: {rule.get('FromPort')}")
                print(f"To Port: {rule.get('ToPort')}")
                print("CIDR Ranges:")

                for ip_range in rule.get('IpRanges'):
                    print(f" - {ip_range['CidrIp']}")
                    time.sleep(2)

        print("Returning to EC2 Menu..")
        time.sleep(3)

    def check_security_groups(self):
        """Checks for vulnerabilities in the identified Security Groups"""
        my_security_groups = self.ec2_client.describe_security_groups()
        flagged_rules = []  # To store security groups with security concerns.
        critical_ports = {22: 'ssh/sftp', 3389: 'RDP', 80: 'http'}  # Identify the critical ports for investigating.
        print("Looking for vulnerabilities..")
        time.sleep(2)

        for sg in my_security_groups['SecurityGroups']:
            for rule in sg['IpPermissions']:
                from_port = rule.get('FromPort')
                to_port = rule.get('ToPort')
                protocol = rule.get('IpProtocol')

                if from_port is None or to_port is None:
                    continue  # Skip rules without port information.

                # Check if the rule allows unrestricted access
                for ip_range in rule.get('IpRanges', []):
                    cidr = ip_range.get('CidrIp')
                    if cidr == '0.0.0.0/0' or cidr == '::/0':
                        # Ports for ssh,sftp,and rdp.
                        if from_port in [22, 3389, 80]:
                            flagged_rules.append({
                                'GroupId': sg['GroupId'],
                                'GroupName': sg['GroupName'],
                                'FromPort': from_port,
                                'ToPort': to_port,
                                'Protocol': protocol,
                                'CidrIp': cidr
                            })

        if flagged_rules:
            print("\nFlagged Security Groups are:")
            for rule in flagged_rules:
                port_type = critical_ports.get(rule['FromPort'])
                print(f"\nSecurity Group ID: {rule['GroupId']}")
                print(f"This security group allows unrestricted access from {rule['CidrIp']}"
                      f" on port {rule['FromPort']} ({port_type})")
                print(f"Please check security group ID: {rule['GroupId']} - Group Name: {rule['GroupName']}")
                time.sleep(3)
        else:
            print("No security groups with unrestricted critical ports found.")

    def check_for_public_instance(self):
        """Checks if an EC2 instance has public access"""

        my_instances = self.ec2_client.describe_instances()
        num_of_instance = len(my_instances['Reservations'])

        print(f"Checking {num_of_instance} EC2 instances...")
        time.sleep(2)

        public_instances = []

        for reservation in my_instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance.get('InstanceId')
                public_ip = instance.get('PublicIpAddress')
                state = instance['State']['Name']

                if public_ip:
                    public_instances.append({
                        'InstanceId': instance_id,
                        'PublicIp': public_ip,
                        'State': state
                    })

        if public_instances:
            print(f"{len(public_instances)} EC2 instance(s) were found with public access.")
            time.sleep(1)

            for item in public_instances:
                print(f"Instance ID: {item['InstanceId']}")
                print(f"IP Address: {item['PublicIp']}")
                print(f"Current State: {item['State']}")
                time.sleep(3)
                print(f"Should '{item['InstanceId']}' have an assigned public IP? Please check.")
                time.sleep(4)

        else:
            print("No EC2 instances were found with a public IP Address.")
            time.sleep(3)

    def check_key_pair(self):
        """Checks our EC2 Instances for Key-Pairs."""

        print("Checking EC2 instances..")
        time.sleep(3)
        get_instances = self.ec2_client.describe_instances()

        for reservations in get_instances['Reservations']:
            for instances in reservations['Instances']:
                instance_id = instances.get('InstanceId')
                key_name = instances.get('KeyName')

                if not key_name:
                    print(f"Instance: {instance_id} has no key pair. This could"
                          f" compromise the security of your instance.")
                    time.sleep(3)
                    print("Please check these instances.")
                    time.sleep(3)
                    print("Returning to EC2 Menu.")
                    time.sleep(3)

    def ec2_sub_menu(self):
        """Provides a sub menu for checking security concerns with our EC2 instances."""
        print("Loading EC2 menu..")
        time.sleep(2)
        print("Choose an option from the Menu.")

        while True:
            try:
                print("1 - Display details for all EC2 security groups.")
                print("2 - Check for Security Group vulnerabilities.")  # Expansion
                print("3 - Check for EC2 instances with public access.")
                print("4 - Check EC2 Key Pairs.")
                print("5 - Return to Main Menu.")
                user_choice = int(input("Enter here: "))

                if user_choice == 1:
                    self.list_security_groups()

                elif user_choice == 2:
                    self.check_security_groups()

                elif user_choice == 3:
                    self.check_for_public_instance()

                elif user_choice == 4:
                    self.check_key_pair()

                elif user_choice == 5:
                    print("Returning to Main Menu")
                    time.sleep(2)
                    break

                else:
                    print("Invalid menu choice. Please choose a number from the options.")

            except ValueError:
                print("Invalid input. Please enter a number.")
