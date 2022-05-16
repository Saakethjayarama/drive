import re

pattern = r'<span>.?<\/span>'
string = '<span>+</span>11<span>%</span>'
x = re.split(pattern, string)
print(x)