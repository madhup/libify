import json
import types
import tempfile
import importlib
from cryptography.fernet import Fernet

patch = 'globals().update({k: v for k, v in x.items() if k not in globals()})'
enc = 'utf-8'
prefix = 'libified_'
export_error = ('libify.exporter incorrectly imported or used. Ensure the '
                'notebook has atleast 1 cell present before importing and '
                'using libify.exporter(). For help on using libify please '
                'visit https://pypi.org/project/libify/')

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
    assert config is not None, 'Either "nbaddr" or "config" has to be specified'

  with open(config['file'], 'rb') as f:
    defs = Fernet(config['key'].encode(enc)).decrypt(f.read()).decode(enc)

  with tempfile.NamedTemporaryFile('w') as tf:
    tf.write('patch_globals = lambda x: ' + patch + '\n' + defs)
    tf.seek(0)
    loader = importlib.machinery.SourceFileLoader(prefix + nbaddr, tf.name)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)

  module.patch_globals(global_vars)
  return module
