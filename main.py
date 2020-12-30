#!/usr/bin/env python3
############################################################
__title__   = 'Local Templating Engine'
__author__  = 'Gray'
__version__ = 1.0
__website__ = 'https://lambda.black/'
############################################################
import re, sys, os, shutil
from glob import glob
del sys.argv[0]

# CLI Standards
class c:
  _ = '\033[0m'
  p = '\033[38;5;204m'
  o = '\033[38;5;208m'
  b = '\033[38;5;295m'
  c = '\033[38;5;299m'
  g = '\033[38;5;47m'
  r = '\033[38;5;1m'
  y = '\033[38;5;226m'


def success(msg):
  """
  Prints out a success message
  Usage: success(msg)
  -------------------------------------------------------------------
  parameters:
    msg - message to print (str)
  """
  print(f'{c.g}[+]{c._} {msg}')

def error(msg, fatal=False):
  """
  Prints out an error message
  Usage: error(msg)
  -------------------------------------------------------------------
  parameters:
    msg - message to print (str)
    fatal - Terminates execution of program if True (bool)
  """
  sys.stderr.write(f'{c.r}[-]{c._} {msg}\n')
  if fatal:
    sys.exit(1)

def warn(msg):
  """
  Prints out a warning message if global variable verbosity is set to True
  Usage: warn(msg)
  -------------------------------------------------------------------
  parameters:
    msg - message to print (str)
  """
  if verbosity:
    sys.stderr.write(f'{c.y}[~]{c._} {msg}\n')

def info(msg):
  """
  Prints out an info message if global variable verbosity is set to True
  Usage: info(msg)
  -------------------------------------------------------------------
  parameters:
    msg - message to print (str)
  """
  if verbosity:
    print(f'{c.c}[*]{c._} {msg}')

def get_filepath(path):
  """
  Takes in a filepath and returns the full filepath terminating with a '/'
  Prints out a success message
  Usage: full_path = get_filepath(path)
  -------------------------------------------------------------------
  parameters:
    path - filepath to process (str)
  returns:
    full_path - Full version of the filepath provided (str)
  """
  # terminate with '/'
  if path[-1:] != '/':
    path += '/'
  # if full path return
  if path[:1] == '/':
    return path
  # complete the rest of the filepath
  path = path.replace('./','')
  return f'{os.getcwd()}/{path}'

def print_help():
  width = int(os.popen('stty size', 'r').read().split()[1])
  if width > 130: width = 130
  print(c.o+'='*width)
  print(f'{__title__} v{__version__}'.center(width))
  print(f'{c.b}Author: {c.g}{__author__}    {c.b}Website: {c.g}{__website__}')
  
  print(f"\n{c.o}Flags:")
  tmp = f'\n{c.c}    Usage: '

  for f in flags:
    print(f"""  {c.y}{' '.join([x+' '+(f['parameter'] if f['parameter'] else '') for x in f['name']])}
    {c.b}{f['description']}{''.join([tmp+x for x in f['usage']])}""")
  print(c.o+"="*width)

def parse_flag(flag):
  for i,x in enumerate(sys.argv):
    if x in flag['name']:
      if flag['parameter']:
        return sys.argv[i+1]
      else:
        return True
  return flag['default']

# run flags
flags = [
  {
    'name':['-i','--input'],
    'parameter':'<folder>',
    'description':'Specifies input folder',
    'usage':['-i website/', '--input /var/www/html'],
    'default':None
  },
  {
    'name':['-o','--output'],
    'parameter':'<folder>',
    'description':'Specifies output folder',
    'usage':['-o website/', '--output /var/www/html'],
    'default':'output'
  },
  {
    'name':['-t','--template-folder'],
    'parameter':None,
    'description':'Specify path to templates folder',
    'usage':['-t templates/', '--templates-folder /var/www/templates'],
    'default':'templates'
  },
  {
    'name':['-v','--verbosity'],
    'parameter':None,
    'description':'Enables more verbose output such as info and warnings.',
    'usage':['-v'],
    'default':False
  },
  {
    'name':['-h','--help','help'],
    'parameter':None,
    'description':'Prints out this help screen.',
    'usage':['-h'],
    'default':False
  },
]

input_folder = parse_flag(flags[0])
output_folder = parse_flag(flags[1])
templates_folder = parse_flag(flags[2])
verbosity = parse_flag(flags[3])
_help = parse_flag(flags[4])

# Check flags to make sure there isn't any bull shit
if _help:
  print_help()
  sys.exit(0)

if not input_folder:
  error('You need to specify an input folder for this program to work.', fatal=True)

# get full paths
input_folder = get_filepath(input_folder)
output_folder = get_filepath(output_folder)








def read_doc(data, variables={}):
  """
  Reads through contents of a document file and then returns the evaluated version of the document.
  Evaluated document resolves all variables declared and invoked within itself and other modules.
  This function also returns variable and module data discovered if required.
  Usage: data, variables, modules = read_doc(data)
  -------------------------------------------------------------------
  parameters:
    data - Contents of a document that you want to process (str)
    variables - Variables to add to the document context (dict)
  returns: 
    data - Processed version of the input document (str) 
    variables - Dictionary of all variables declared within the document and it's modules, keys represent variable names, values represent their respective values (dict) 
    modules - Dictionary of all modules declared within the document and it's modules, keys represent modules paths within modules folder, values represent the processed data from each respective module document (dict) 
  """
  # Find data
  variables.update({k.strip():v.strip() for k,v in [x.split('=') for x in re.findall(r'{{\s*?var:(.*?)\s*?}}', data)]})
  # variables = {k.strip():v.strip() for k,v in [x.split('=') for x in re.findall(r'{{\s*?var:(.*?)\s*?}}', data)]}
  modules = [x for x in re.findall(r'{{\s*?mod:(.*?)\s*?}}', data)]

  # Remove data
  if variables:
    data = re.sub(r'{{\s*?var:(.*?)\s*?}}', '', data)
  if modules:
    data = re.sub(r'{{\s*?mod:(.*?)\s*?}}', '', data)
  data = data.strip()

  # Load new modules
  modules_dict = {}
  for mod in modules:
    with open(f'{input_folder}{templates_folder}/{mod}') as f:
      new = read_doc(f.read(), variables=variables)
      modules_dict[mod] = new[0]
      variables.update(new[1])
  modules = modules_dict
  del modules_dict
  
  # Insert data
  def tmp(txt):
    warn(f'Invalid invocation within file {filename} at "{txt}", skipping.')
    return txt
  data = re.sub(r'{{\s*?(\S*?)\s*?}}', lambda x: variables[x.group(1)] if x.group(1) in variables else tmp(x.group()), data, flags=re.DOTALL)
  data = re.sub(r'{%\s*?(\S*?)\s*?%}', lambda x: modules[x.group(1)] if x.group(1) in modules else tmp(x.group()), data, flags=re.DOTALL)

  return data, variables, modules

# delete output folder if it exists
try:
  shutil.rmtree(output_folder)
except FileNotFoundError:
  pass
# copy input folder to output folder
shutil.copytree(input_folder, output_folder)

# get all files
files = [y for x in os.walk(output_folder) for y in glob(os.path.join(x[0], '*.html'))]

for filename in files:
  success(f'processing file {filename}')
  # get file data
  with open(filename) as f:
    data = f.read()

  # Process individual file
  data, variables, modules = read_doc(data)
  with open(filename, 'w') as f:
    f.write(data)

shutil.rmtree(f"{output_folder}{templates_folder}")