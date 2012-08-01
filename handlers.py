#!/usr/bin/env python


import os
import jinja2
import json
import webapp2

from google.appengine.api import search

template_path = os.path.join(os.path.dirname(__file__), 'templates')
env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))


def _list_to_documents(documents):
  result = []
  # TODO (singhsays): handler conversion of fields to search fieldtypes here.
  for d in documents:
    result.append(search.Document(d))
  return result


class TemplateHandler(webapp2.RequestHandler):

  def render(self, template_name, data=None, mime_type='text/html'):
    if data is None:
      data = {}
    template = env.get_template(template_name)
    self.response.headers['Content-Type'] = mime_type
    self.response.out.write(template.render(data))

  def render_json(self, data=None):
    self.response.headers['Content-Type'] = 'application/json'
    if data is None:
      data = []
    self.response.out.write(json.dumps(data))


class Status(TemplateHandler):
  def get(self):
    self.render('index.html')


class IndexesHandler(TemplateHandler):
  def get(self):
    indexes = search.list_indexes().indexes
    response = []
    for i in indexes:
      response.append({'name': i.name})
    self.render_json(response)


class IndexHandler(TemplateHandler):
  def post(self, name, consistency=search.Index.GLOBALLY_CONSISTENT):
    index = search.Index(name=name, consistency=consistency)
    index.add(search.Document(fields=[search.TextField(name="testfield", value="testvalue")]))
    if index:
      self.render_json({'result': 'success', 'name': index.name})
    else:
      # TODO(singhsays): return actual errors.
      self.render_json({'result': 'error', 'errors': []})

  def delete(self, indexname):
    #delete index indexname
    pass


class DocumentHandler(TemplateHandler):
  def post(self, documents, index_name='default-index', consistency=search.Index.GLOBALLY_CONSISTENT):
    index = search.Index(name=index_name)
    documents = _list_to_documents(documents)
    try:
      index.add(documents)
    except search.Error:
      self.render_json({'result': 'error', 'errors': []})
      return
    self.render_json({'result': 'success'})
