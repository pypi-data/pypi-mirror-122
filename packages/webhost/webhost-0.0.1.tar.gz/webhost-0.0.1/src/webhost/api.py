# api.py #

import os
import inspect
from os import system
from parse import parse
from whitenoise import WhiteNoise
from webob import Request, Response
from wsgiref.simple_server import make_server
from jinja2 import Environment, FileSystemLoader

class init:
    def __init__(self):

        self.routes = {}
        self.Http404 = "404 Page not found!"
        self.templatesDir = "templates"
        self.staticDir = "static"
        self.exception_handler = None
  
        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(self.templatesDir)))
        self.whitenoise = WhiteNoise(self.wsgi_app, root=self.staticDir)

    def url(self, path, handler):
        assert path not in self.routes, "Such route already exists."

        self.routes[path] = handler

    def route(self, path):
        def wrapper(handler):
            self.url(path, handler)
            return handler

        return wrapper

    def config(self, dic):
        self.Http404 = dic.get("Http404", "404 Page not found!")
        self.templatesDir = dic.get("TemplatesDir", "templates")
        self.staticDir = dic.get("StaticDir", "static")

    def wsgi_app(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)


    def usetemplate(self, template_name, context=None):

        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def exceptionHandler(self, exception_handler):
        self.exception_handler = exception_handler

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        try:
            if handler is not None:
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError("Method now allowed", request.method)

                handler(request, response, **kwargs)
            else:
                self.default_response(response)
        except Exception as e:
            if self.exception_handler is None:
                raise e
            else:
                self.exception_handler(request, response, e)

        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = self.Http404



class Server:

    def runtime(self, host, port, cls=True):
        
        if cls:
            system("cls")
        else:
            pass

        print(f"[CITE] Running web application")
        print(f"[SERVER] Running on '{host}:{port}'")
        print(f"Hit Ctrl + C to quit application...\n")

    def run(self, func, host='127.0.0.1', port=5000, cls=True):

        with make_server(host, port, func) as server:

            if cls:
                self.runtime(host=host, port=port)
            else:
                self.runtime(host=host, port=port, cls=False)

            server.serve_forever()

server = Server()

