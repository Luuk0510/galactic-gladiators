import functools

def log_special_power(func):
    @functools.wraps(func)
    def wrapper_log_special_power(*args, **kwargs):
        unit = args[0] 
        print(f"{unit.__class__.__name__} gebruikt zijn special power: {unit.special_power}")
        
        result = func(*args, **kwargs)
    
        return result
    return wrapper_log_special_power
