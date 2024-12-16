from iam_security import IamSecurity
from s3_compliance import S3Compliance
from ec2_security import EC2Security

class SecurityTool:
    """Coordinates the execution of security checks across our AWS services.

    This class serves as the main user interface for navigating the programme. The user
    can carry out security checks on a variety of AWS Services. It initialises and
    organises the service-specific class and provides a menu so users can carry out their
    security checks
    """

    def __init__(self):
        """Initialises dependencies for our Classes"""
        self.iam = IamSecurity()
        self.s3 = S3Compliance()
        self.ec2 = EC2Security()

    def security_menu(self):
        """Provides the Main Menu interface for navigating the programme."""
        print("Loading programme...")
        time.sleep(2)

        while True:
            try:
                print("Choose a AWS Service from the Menu to look for security concerns.")
                time.sleep(2)
                print("Main Menu")
                print("1 - IAM")
                print("2 - S3")
                print("3 - EC2")
                print("4 - Quit.")

                # Get the users menu choice as in integer.
                user_choice = int(input("Enter here: "))

                if user_choice == 1:
                    self.iam.iam_sub_menu()

                elif user_choice == 2:
                    self.s3.s3_sub_menu()

                elif user_choice == 3:
                    self.ec2.ec2_sub_menu()

                elif user_choice == 4:
                    print("Exiting the application..")
                    time.sleep(2)
                    print("Bye!")
                    break

                else:
                    print("Invalid choice. Please choose a number that corresponds to a menu choice.")

            except ValueError:
                print("Please input a number.")


def main():
    security_tool = SecurityTool()
    security_tool.security_menu()


if __name__ == "__main__":
    main()
