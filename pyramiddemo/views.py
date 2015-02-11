from pyramid.response import Response
from pyramid.view import view_config

from .security import is_valid_user
from pyramid.security import (
    remember,
    )

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Item,
    is_valid_ean13,
    )

from pyramid.httpexceptions import (
    HTTPFound,
    )


@view_config(route_name='login', renderer='templates/login.pt')
def login_view(request):
    url = request.route_url('login')
    login = ''
    message = ''

    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if is_valid_user(login,password):
            headers = remember(request, login)
            return HTTPFound(location = request.route_url('item_action', action='view'),
                             headers = headers)

        message = 'Wrong username/password'


    return dict(url=url, login=login, message=message)

@view_config(route_name='item_action', match_param='action=view',
             renderer='templates/item_view.pt',
             permission='view')
def item_view(request):
    items = DBSession.query(Item).order_by(Item.ean13)
    return dict(items=items)


@view_config(route_name='item_action', match_param='action=add',
             renderer='templates/item_add.pt',
             permission='edit')
def item_add(request):
    url = request.route_url('item_action',action='add')
    messages = []
    ean13 = ''
    ean13_error = ''
    description_error = ''
    description = ''
    if 'form.submitted' in request.params:
        ean13 = request.params['ean13']
        description = request.params['description']

        # Add some validation
        if len(description) < 10:
            description_error='error'
            messages.append("La description doit faire plus de 10 caractères")

        if not is_valid_ean13(ean13):
            ean13_error='error'
            messages.append("EAN13 invalide")

        if not ean13_error and not description_error:
            item = Item(ean13=ean13, description=description,
                        user= request.authenticated_userid)
            DBSession.add(item)

            return HTTPFound(location = request.route_url('item_action',
                                                          action='view'))


    return dict(messages=messages,
                ean13=ean13,
                ean13_error=ean13_error,
                description_error=description_error,
                description=description,
                url=url)
