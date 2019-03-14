from webob import Request
from paste import httpserver

# веб приложение 
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    # print(environ)
    return [b'<b>Hello World</b>']


def main():
    # запуск сервера
    httpserver.serve(application,  host='127.0.0.1', port=8080)

main()