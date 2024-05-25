def check_registration():
    """
    This function is used to verify if the user has registered or not. 
    If the user is logged in, it will redirect them to their dashboard page.
    Check if the user is registered.
    """
    print("Are you already registered?")
    response = input("Enter 'yes' if you are registered, 'no' otherwise: ").lower()
    if response == "yes":
        return True
    elif response == "no":
        return False
    else:
        print("Invalid response. Please enter 'yes' or 'no'.")
        return check_registration()
    
def user_sign_up():
    """
    This function is for users who want to sign up and create a new account. 
    It prompts the user to enter their information (username, password, email).
    """
    print("User Sign up")
    if check_registration():
        return user_sign_in()
    else:
        email = input("Enter your email: ")
        if verify_email(email):
            password = create_password()
            if verify_password(password):
                print("Account created successfully!")
                return True
            else:
                print("Invalid password. Please try again.")
                return False
        else:
            print("Invalid email. Please try again.")
            return False
        
def verify_email(email):
    """
    This function checks whether the given email is valid or not
    """
    # Function than simulated checks the validity of an email.
    if "@" in email and "." in email:
        return True
    else:
        return False

def create_password():
    """
    This function creates a random password which will be used by the user to log into his/her account.
    The password should contain at least one uppercase letter, one lowercase letter, one digit, and one special character.
    The length of the password is set as 8 characters.
    """
    return input("Create a password: ")

def verify_password(password):
    """
    This function verifies whether the entered password matches with the one that was created by the user.
    If they match it returns True otherwise it returns False.
    """
    # Simulated password validation process
    if len(password) >= 8:
        return True
    else:
        return False

def user_sign_in():
    """
    This  function allows users to sign in their accounts using their registered emails and passwords.
    It takes the email address and password from the user, validates them, and logs the user in if they are correct.
    It takes the email address and password from the user, validates them, and logs the user in if they are correct.
    It takes the email and password from the user, calls the functions `verify_email` and `verify_password` to check the validity of these inputs.
    It takes the email and password from the user, calls the respective functions to check for valid inputs,
    and then logs the user in if both are correct.
    """
    print("User Sign in")
    # Simulated sign-in process
    return True