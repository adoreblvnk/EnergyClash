import re

f = open('blob.txt','r').read()
r = re.findall(r'<div class="label">[\w\W]*</div>[\w\W]*<div class="value">.*</div>\n',f)
print(r[0])