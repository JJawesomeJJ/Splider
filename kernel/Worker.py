#Description It is a work process try to start Grab the data of network
#At first you should write the rules of grabing!!!
#Example of this
# total_rules = [
#     {
#         "name": "ul_container",
#         "reg": '<ul class="listBox_card">([\s\S]*?)</ul>',
#         "length": 1,
#         'children': [{
#             'name': 'item',
#             'reg': '<a ([\s\S]*?)listBox_card_p1',
#             'children': [
#                 {
#                     "name": 'href',
#                     'reg': 'href="/goods/(.*?).html"',
#                     'length': 1
#                 },
#                 {
#                     "name": 'img',
#                     'reg': 'src="(.*?)"',
#                     'length': 1
#                 }
#             ],
#             "is_store": False
#         }],
#         'is_store': False
#     }
# ]
from Spider.kernel import Spiders
from Spider.kernel import Filter
class Woker():
    url=None
    reg=None
    diver="requests"
    spliers=None
    content=""
    def __init__(self,url,reg=None):
        self.url=url
        self.reg=reg
        self.spliers=Spiders.Spiders(self.url)
    def start(self,method="GET",params={},header={}):
        Content=self.spliers.set_diver(self.diver).get_page_content(method,params,header)
        self.content=Content
        data=Filter.Filter().filter(self.reg,Content)
        return data
    def set_diver(self,dirver="requests"):
        self.diver=dirver
        return self
    def page_content(self):
        return self.content
