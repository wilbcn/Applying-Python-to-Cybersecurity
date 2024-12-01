# Python script to check if user password meets specific requirements
# Criteria:
# Password must meet minimum length requirements: 12+
# Presence of uppercase and lowercase characters
# Presence of numeric values and special characters
# Provide feedback on the strength of the password: Weak, Moderate, Strong
# Provide improvements


# Building the function
def check_pw_strength():

    feedback = []  # Create an empty list to provide password strength feedback
    score = 0      # Initialize score counter
    special_characters = set("~`!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/")

    password = input("Please enter a password:  ")

    # Check criteria and update feedback and score
    if len(password) < 12:
        feedback.append(f"Password should be 12 characters or more. You have entered a password with {len(password)} characters")
        score += 1

    if not any(letter.isupper() for letter in password):
        feedback.append("Password must contain at least one uppercase letter.")
        score += 1

    if not any(letter.islower() for letter in password):
        feedback.append("Password must contain at least one lowercase letter.")
        score += 1

    if not any(char.isdigit() for char in password):
        feedback.append("Password must contain at least one numeric character.")
        score += 1

    if not any(char in special_characters for char in password):
        feedback.append("Password must contain at least one special character.")
        score += 1

    # Provide feedback on password strength based on score
    if score == 0:
        print("Your password strength is: STRONG")
        print("Password accepted")
    elif score <= 2:
        print("Your password strength is: MODERATE")
    elif score <= 4:
        print("Your password strength is: WEAK")
    else:
        print("SUPER INSECURE PASSWORD!")

    # Print detailed feedback if criteria are not met
    if feedback:
        print("Password does not meet the following criteria:")
        for error in feedback:
            print(f"- {error}")

# Testing the function
check_pw_strength()
