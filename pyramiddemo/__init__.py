from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import (
    DBSession,
    Base,
    )

from .security import (
    groupfinder,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    authn_policy = AuthTktAuthenticationPolicy(
            settings['pyramiddemo.secret'],
            callback=groupfinder,
            hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()


    config = Configurator(settings=settings,
                         root_factory='.resources.Root')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
#   config.add_route('home', '/')                     # <- À supprimer
    config.add_route('login', '/')                    # <- À ajouter
    config.add_route('item_action', '/item/{action}') # <- À ajouter
    config.scan()
    return config.make_wsgi_app()
