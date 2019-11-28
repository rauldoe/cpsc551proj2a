
from common import Common

ts = Common.getTsFromConfig('naming', 'adapter')
Common.updateServerList(ts, 'bob')
res = ts._inp(['server_list', None])
print(res)
