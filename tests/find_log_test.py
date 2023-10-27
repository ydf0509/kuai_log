
from pathlib import Path
import re

print(len(re.findall('hi',(Path('/pythonlogs')/Path('2023-10-07.0001.f1d.log')).read_text())))