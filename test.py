import re

msg = 'efrtgy5tgeeeehs'

if re.match(r'[A-Za-z0-9]{10}', msg) and len(msg) == 10:
    print('yes')
else:
    print('no')
