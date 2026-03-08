def dict_travel(nested_dicts):
  l = []
  def rec(k, v):
    if isinstance(v, dict):
      for a, b in v.items():
        newk = k + "." + a
        rec(newk, b)
    else:
      l.append(k + ": " + str(v))
      
  for k, v in nested_dicts.items():
    rec(k, v)
  
  for i in sorted(l):
    print(i)