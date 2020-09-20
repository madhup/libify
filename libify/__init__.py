import json
import tempfile
from cryptography.fernet import Fernet
from importlib.util import module_from_spec, spec_from_loader

# Error Messages
error_help = ('For help on using libify please visit '
              'https://github.com/vagrantism/libify')
export_error = ('libify.exporter incorrectly imported or used. Ensure the '
                'notebook has atleast 1 cell present before importing and '
                'using libify.exporter(). ') + error_help
imp_error = ('Parameter "config" is incorrect. Ensure that it is copied '
             'correctly from the importee notebook without the "Notebook'
             ' exited: " string. ') + error_help
param_error = 'Either "nbaddr" or "config" has to be specified. ' + error_help


patch_func = ('patch_globals = lambda x: globals().update'
              '({k: v for k, v in x.items() if k not in globals()})')
enc = 'utf-8'
prefix = 'libified_'
keys = ['file', 'key']


def exporter(global_vars):
  assert len(global_vars.get('In', [])) > 1, export_error
  key = Fernet.generate_key()
  suite = Fernet(key)
  with tempfile.NamedTemporaryFile(delete=False) as f:
    f.write(suite.encrypt(bytes('\n\n'.join(global_vars['In'][:-1]), enc)))
  global_vars['dbutils'].notebook.exit(json.dumps({'key': key.decode(enc),
                                                   'file': f.name}))


def importer(global_vars, nbaddr='', timeout=0, config=None):
  
  if nbaddr:
    config = json.loads(global_vars['dbutils'].notebook.run(nbaddr, timeout))
  else:
    assert isinstance(config, dict), param_error
    assert all([isinstance(config.get(k, None), str) for k in keys]), imp_error

  with open(config['file'], 'rb') as f:
    defs = Fernet(config['key'].encode(enc)).decrypt(f.read()).decode(enc)

  module = module_from_spec(spec_from_loader(prefix, loader=None))
  exec(patch_func, module.__dict__)
  module.patch_globals(global_vars)
  exec(defs, module.__dict__)
  return module
