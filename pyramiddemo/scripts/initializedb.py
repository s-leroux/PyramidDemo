import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
#    MyModel, # <- Supprimé
    Item,     # <- Ajouté
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
#        model = MyModel(name='one', value=1) # <- Supprimé
#        DBSession.add(model)                 # <- Supprimé

         # ↓ Ajouter es lignes suivantes ↓
         item = Item(user='sylvain', ean13='9781933988788',
                     description='Erland and OTP in Action (book)')
         DBSession.add(item)  
         item = Item(user='bob', ean13='9780321349606',
                     description='Java Concurrency in Practice (book)')
         DBSession.add(item)  
