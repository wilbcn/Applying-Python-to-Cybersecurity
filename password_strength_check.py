# Python script to check if user password meets specific requirements
# Criteria:
# Password must meet minimum length requirements: 12+
# Presence of uppercase and lowercase
# Presence of numeric values and special characters
# Provide feedback on the strength of the password: Weak, Moderate, Strong
# Provide improvements

# set special characters
special_characters = set("~`!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/")

# Create an empty list to provide password strength feedback

feedback = []

def check_pw_strength():

    password = input("Please enter a password:  ")

    if not len(password) >= 12:
        feedback.append("Password should be 12 characters or more.")

    if not any(letter.isupper() for letter in password):
        feedback.append("Password must contain at least one uppercase letter.")

    if not any(letter.islower() for letter in password):
        feedback.append("Password must contain at least one lowercase letter.")

    if not any(char.isdigit() for char in password):
        feedback.append("Password must contain at least one numeric character.")

    if not any(char in special_characters for char in password):
        feedback.append(f"Password must contain at least one special character.: {special_characters}")

    if feedback:
        print("Password does not meet the following criteria")
        for error in feedback:
            print(f"-{error}")
    else:
        print("Password has been accepted!")


# Testing the function

check_pw_strength()

