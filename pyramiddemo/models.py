from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    CHAR,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Item(Base):
    __tablename__ = 'ITEMS'
    id = Column(Integer, primary_key=True)
    user = Column(String(16))
    ean13 = Column(CHAR(13))
    description = Column(Text)

Index('ITEMS_IDX', Item.ean13, unique=True)

def is_valid_ean13(ean13):
    if len(ean13) != 13:
        return False

    # See http://en.wikipedia.org/wiki/International_Standard_Book_Number#ISBN-13_check_digit_calculation
    weights = '1313131313131'
    try:
        cksum = 0
        for w,n in zip(weights,ean13):
            cksum += int(w)*int(n)

        return cksum%10 == 0
    except:
        # any exception is assumed to be caused by
        # malformed ean13 code
        return False
