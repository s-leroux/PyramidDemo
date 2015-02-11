from sqlalchemy.sql import text
from hashlib import sha256

from .models import (
    DBSession,
    )

user_query = text("SELECT COUNT(*) FROM USER "
                  "WHERE LOGIN=:login "
                  "AND PASSWD=:passwd")

# In this sample system, all users will have
# the same group membership.
# We only have to check for user existance.
group_query = text("SELECT COUNT(*) FROM USER "
                  "WHERE LOGIN=:login")

def is_valid_user(username, password):
    """Check if the given user/password is a valid
    user for the system.
    """
    salted_password = username + ":" + password
    print(salted_password)
    passwd = sha256(salted_password.encode("utf-8")).hexdigest()
    return DBSession.execute(user_query,
                             dict(login=username, passwd=passwd)).scalar() == 1

def groupfinder(username, request):
    """Authentication policy callback.

    *    If the userid exists in the system, it will return a sequence of group identifiers (or an empty sequence if the user isn't a member of any groups).
    *    If the userid does not exist in the system, it will return None.

    See http://docs.pylonsproject.org/docs/pyramid/en/latest/tutorials/wiki/authorization.html#add-users-and-groups
    """
    print('user_group:',username,request)
    existing_user = \
        DBSession.execute(group_query, dict(login=username)).scalar()

    return ['editor'] if existing_user else None
