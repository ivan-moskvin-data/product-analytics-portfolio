import functools

def add_attrs(**kwargs2):
  def dec(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
      return f(*args, **kwargs)
    for k, v in kwargs2.items():
      wrapper.__dict__[k] = v
    return wrapper
  return dec