def takes_positive(func):
  def f(*args, **kwargs):
    l = [*args, *kwargs.values()]
    if any(map(lambda x: isinstance(x, (str, float)), l)):
      raise TypeError()
    elif any(map(lambda x: x <= 0 and isinstance(x, int), l)):
      raise ValueError()
    else:
      return func(*args, **kwargs)
  return f