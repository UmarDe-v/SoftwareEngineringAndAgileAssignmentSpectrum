class TokenExpiredException(Exception):
    pass

class InvalidTokenException(Exception):
    pass

class UserAlreadyLoggedInException(Exception):
    pass

class PermissionDeniedException(Exception):
    pass

class UsernameAlreadyRegisteredException(Exception):
    pass

class EmailAlreadyRegisteredException(Exception):
    pass

class InvalidEmailException(Exception):
    pass

class InvalidUsernameException(Exception):
    pass

class InvalidCompanyException(Exception):
    pass

class InvalidCredentialsException(Exception):
    pass

class AdminNotfound(Exception):
    pass

class UserNotfound(Exception):
    pass

class PasswordSame(Exception):
    pass

class NoSprectrumLicense(Exception):
    pass

class ConfirmException(Exception):
    pass

class SpectrumLicensesFound(Exception):
    pass

class ExistingUserException(Exception):
    pass

class SubbandRangeException(Exception):
    pass

class PowerLevelException(Exception):
    pass

class GeographicalAreaException(Exception):
    pass

class LicenceAlreadyRevokedException(Exception):
    pass


# This file defines custom exceptions to handle specific errors in the app, like invalid tokens, duplicate usernames/emails, permission issues, 
# or missing data. Using these makes error handling clearer and helps return meaningful messages to users. Each exception corresponds to a particular 
# problem the system might encounter.