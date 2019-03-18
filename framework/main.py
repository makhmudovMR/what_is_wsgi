from paste import httpserver

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Hello World!']

def main():
    httpserver.serve(application, host='127.0.0.1', port=8080)


main()