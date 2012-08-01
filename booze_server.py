#!/usr/bin/env python


import webapp2
import handlers


urlmap = [
  webapp2.Route(r'/', handler=handlers.Status),
  webapp2.Route(r'/indexes', handler=handlers.IndexesHandler),
  webapp2.Route(r'/index/<name>/', handler=handlers.IndexHandler),
]


app = webapp2.WSGIApplication(urlmap, debug=True)
