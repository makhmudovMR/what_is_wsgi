from webob import Request
from paste import httpserver

# веб приложение 
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    # Except error
    if 'error' in environ['PATH_INFO'].lower():
        raise Exception('Detect "error" in URL path')

    # Session
    session = environ.get('paste.session.factory', lambda: {})()
    if 'count' in session:
        count = session['count']
    else:
        count = 1
    session['count'] = count + 1

    # Generate response
    return [b'You have been here %d times!\n' % count, ]



def main():
    # запуск сервера
    httpserver.serve(application,  host='127.0.0.1', port=8080)

main()