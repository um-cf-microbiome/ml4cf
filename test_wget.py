import shutil
from shutil import which
output = open("output.test","w")
output.write(str("testing "+shutil.which('wget')))
output.close()