'''
    Маршрутизатор просто передает запрос контроллеру, поэтому сами контроллеры являются приложениями WSGI
'''

from webob import Request, Response
from webob import exc
import router

def controller(func):
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException, e:
            resp = e
        if isinstance(resp, str):
            resp = Response(body=resp)
        return resp(environ, start_response)
    return replacement

@controller
def index(req):
    return 'this is application'

@controller
def hello(req):
    if req.method == 'POST':
        return 'Hello %s!' % req.params['name']
    elif req.method == 'GET':
        return '''<form method="POST">
            Your name: <input type="text" name="name">
            <input type="submit">
            </form>'''

hello_world = router.Router()
hello_world.add_route('/', controller=index)
hello_world.add_route('/hello', controller=hello)