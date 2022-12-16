import re

my_string = "This is my\n <string>string\n please <fix> fix me <br />"

print(re.sub(r'\<[^>]*\>', "", my_string))
