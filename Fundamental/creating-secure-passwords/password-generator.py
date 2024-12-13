# Python script to generate a secure password
# Criteria
# Advise the user on recommendations to set a strong password
# User defines the length of the password (min/max) (8/16)
# Include upper/lower case, special characters, or numbers?

import random
import string

# Advice on setting a strong password
def pass_advice():
    print("--------------------")
    print("This is a random password generator!.")
    print("To set a strong password, use a minimum of 8 characters and maximum of 16.")
    print("It is recommended you include at least 1 uppercase and 1 lowercase letter.")
    print("You should also include at least one digit, and one special character.")
    print("--------------------")

# Define the desired length of the random password
def pass_length():
    while True:
        p_length_str = input("Please enter the desired length of your password!")
        if p_length_str.isdigit():
            p_length_int = int(p_length_str)
            if p_length_int < 8 or p_length_int > 16:
                print("Password must be between 8 and 16 characters.")
            else:
                print(f"Valid length: {p_length_int}")
                return p_length_int
        else:
            print("Please enter a valid number.")


# Define lower casing or not
def pass_low_casing():
    while True:
        p_lower = input("Do you want to include lowercase letters? (y/n): ")
        if p_lower.lower() == 'y':
            print("Password will include lowercase letters.")
            return True
        elif p_lower.lower() == 'n':
            p_lower_no = p_lower
            print("Password will not include lowercase letters.")
            return False
        else:
            print("Please enter either 'y' for yes for 'n' for no.")


# Define high casing or not
def pass_high_casing():
    while True:
        p_higher = input("Do you want to include uppercase letters? (y/n): ")
        if p_higher.lower() == 'y':
            print("Password will include uppercase letters.")
            return True
        elif p_higher.lower() == 'n':
            print("Password will not include uppercase letters.")
            return False
        else:
            print("Please enter either 'y' for yes for 'n' for no.")


# Include Special Characters
def pass_special():
    while True:
        p_special = input("Do you want to include special characters? (y/n): ")
        if p_special.lower() == 'y':
            print("Password will include special characters.")
            return True
        elif p_special.lower() == 'n':
            print("Password will not include special characters.")
            return False
        else:
            print("Please enter either 'y' for yes for 'n' for no.")


# Include numbers or not
def pass_digits():
    while True:
        p_num = input("Do you want to include numbers? (y/n): ")
        if p_num.lower() == 'y':
            print("Password will include numbers.")
            return True
        elif p_num.lower() == 'n':
            print("Password will not include numbers.")
            return False
        else:
            print("Please enter either 'y' for yes for 'n' for no.")


# Function to generate the password
def generate_password(length, inc_lower, inc_higher, inc_special, inc_digits):
    # Check user preferences and include those that are true in our password data.
    password_data = ''
    password_mandatory = []

    if inc_lower:
        password_data += string.ascii_lowercase
        password_mandatory.append(random.choice(string.ascii_lowercase))
    if inc_higher:
        password_data += string.ascii_uppercase
        password_mandatory.append(random.choice(string.ascii_uppercase))
    if inc_special:
        password_data += string.punctuation
        password_mandatory.append(random.choice(string.punctuation))
    if inc_digits:
        password_data += string.digits
        password_mandatory.append(random.choice(string.digits))

    # Check if password_data is empty
    if not password_data:
    # Lowercase by default
        password_data = string.ascii_lowercase
        print("No character types selected. Using lowercase letters by default.")

    # Ensure we meet the minimum length requirement
    while len(password_mandatory) < length:
        password_mandatory.append(random.choice(password_data))

    # Shuffle to avoid potential predictable patterns
    random.shuffle(password_mandatory)

    # Truncate to the desired length in case it exceeds
    return ''.join(password_mandatory[:length])

# Main function
def main():
    # Tell the user advice for setting a password
    pass_advice()

    # Set user password preferences
    length = pass_length()
    inc_lower = pass_low_casing()
    inc_higher = pass_high_casing()
    inc_special = pass_special()
    inc_digits = pass_digits()

    # Generate the password based on user's input/preferences
    newpassword = generate_password(length, inc_lower, inc_higher, inc_special, inc_digits)

    print(f"Your generated password is: {newpassword}")

if __name__ == "__main__":
    main()
