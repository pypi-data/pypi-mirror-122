import importlib
import sys
def dynamic_load(string : str) :
  def load_module(target : str, remained : list = list()) :
    try:
      module = importlib.import_module(target)
      return (module, remained)
    except ModuleNotFoundError:
      return load_module(target=".".join(target.split(".")[:-1]), remained=[target.split(".")[-1]] + remained)
    except ValueError:
      sys.exit("Cannot resolve any module from {}".format(string))
  module, last = load_module(string)
  for each in last:
    module = getattr(module, each)
  return module
