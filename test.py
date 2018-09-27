# -*- coding:utf-8 -*-

import re
import random
import operator

url = 'http://www.xzxw.com/xw/kjww/'
basic_url = re.search(r'(http://www.xzxw.com/.*?/)', url)
print(basic_url[0])

