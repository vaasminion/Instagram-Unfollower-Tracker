from utils.GetParameter import getParameter
def get_UserDetails(connection):
    loginuser = getParameter('INSTAGRAM_LOGIN_USERNAME',connection)
    loginpassword = getParameter('INSTAGRAM_LOGIN_PASSWORD',connection)
    username = getParameter('INSTAGRAM_USERNAME',connection)
    return loginuser,loginpassword,username