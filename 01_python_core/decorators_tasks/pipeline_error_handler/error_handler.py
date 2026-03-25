import functools

def ignore_exception(*args2):
  def dec(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
      try:
        return f(*args, **kwargs)
      except Exception as err:
        if type(err) in args2:
          print(f"Исключение {type(err).__name__} обработано")
        else:
          return f(*args, **kwargs)
    return wrapper
  return dec