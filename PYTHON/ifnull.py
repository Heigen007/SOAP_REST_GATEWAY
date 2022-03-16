def ifnull(var):
    if var is None: return ""
    if isinstance(var, int): return str(var)
    return var