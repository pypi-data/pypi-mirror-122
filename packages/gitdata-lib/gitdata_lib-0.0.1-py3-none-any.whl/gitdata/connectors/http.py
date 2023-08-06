""" http connector
"""

# import requests
# from io import StringIO

from .common import BaseConnector

# class Source(object):

#     def __init__(self, kind, data):
#         self.kind = kind
#         self.data = data

#     def __repr__(self):
#         return self.kind #'<Source({self.kind!r}, data)>'.format(self=self)
#         #return '<Source({self.kind!r}, data)>'.format(self=self)



class HttpConnector(BaseConnector):

    name = 'http'
    reads = ['location']
    writes = ['blob', 'status']

#     def _views(self, source):
#         r = requests.get(source.data.url)
#         if r.status_code == 200:
#             print('http success: ', source.data.url)
#             return [
#                 Source('blob', StringIO(r.content))
#             ]

#     def extract(self, source):
#         r = requests.get(source.url)
#         if r.status_code == 200:
#             print('http success: ', source.url)
#             return [Source('blob', StringIO(r.content))]

#     # legacy
#     def collect(self, target):
#         r = requests.get(target.url)
#         if r.status_code == 200:
#             return StringIO(r.content)

