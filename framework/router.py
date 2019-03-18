import re
import sys
from webob import Request, exc

var_regex = re.compile('''
        \{
        (\w+)
        (?::([^}]+))?
        \}
    ''', re.VERBOSE)

def template_to_regex(template):
    '''
        input: /a/static/path
        output: ^\/a\/static\/path$
    '''
    regex = ''
    last_pos = 0
    for match in var_regex.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex    




def load_controller(string):
    '''
        Импортирует модуль и функцию из него
    '''
    module_name, func_name = string.split(':', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    func = getattr(module, func_name)
    return 
    


class Router:

    def __init__(self):
        self.routes = []

    def add_route(self, template, controller, **vars):
        '''
            Добавляем роут
        '''
        if isinstance(controller, str):
            controller = load_controller(controller)
        self.routes.append((re.compile(template_to_regex(template), controller, vars)))


    def __call__(self, environ, start_response):
        '''
            вызываем контроллер и его функцию (controller action)
        '''
        req = Request(environ)
        for regex, controller, vars in self.routes:
            match = regex(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)

if __name__ == '__main__':
    print(template_to_regex('controller:name'))
