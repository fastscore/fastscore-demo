class StreamingCalcBundle(object):
    def __init__(self):
        self._calcs = {}
    
    def __add__(self, calc):
        self._calcs[calc.name] = (calc)
    
    def update(self, **kwargs):
        for n, c in self._calcs.items():
            c.update(**kwargs)
    
    def __getitem__(self, key):
        return self._calcs[key].value
    
    @property
    def values(self):
        return { n: c.value for n, c in self._calcs.items()}
    
class StreamingCalc(object):
    def __init__(self, func, name, val=0, n=0):
        self.val = val
        self.n = n
        self.func = func
        self.name = name
    
    @property
    def value(self):
        return self.val
    
    def update(self, **kwargs):
        self.val = self.func(self.val, self.n, **kwargs)
        self.n = self.n + 1

def update_mean(mean, n, x, **kwargs):
    return (x + n*mean)/(n+1) if n > 0 else x

def update_variance(var, n, x, **kwargs):
	return (n*var + (x - mean)**2)/(n+1) if n > 0 else 0

def update_mse(mse, n, x, y, **kwargs):
    return (n*mse + (x - y)**2)/(n + 1) if n > 0 else (x - y)**2

def update_mae(mae, n, x, y, **kwargs):
    return (n*mae + abs(x - y))/(n + 1) if n > 0 else abs(x - y)

def update_min(minimum, n, x, **kwargs):
    return min(x, minimum) if n > 0 else x

def update_max(maximum, n, x, **kwargs):
    return max(x, maximum) if n > 0 else x

# n.b. this can also be updated to include skewness, kurtosis
def update_moments(mean_var, n, x, **kwargs):
    mean, var = mean_var
    mean_x = (n*mean + x)/(n + 1)
    var_x = (n*var + (x - mean)*(x - mean_x))/(n + 1)
    return mean_x, var_x

def update_ewma(ewma,n, x, alpha = 0.05, **kwargs):
	return alpha*x + (1-alpha)*ewma if n > 1 else x

def update_ewmv(ewmv, n, ewma, x, alpha = 0.05, **kwargs):
	if n == 0:
		return 0
	elif n == 1:
		return x
	else: return (1-alpha)*(ewmv + alpha*(x - ewma)**2)

def update_ewm(ewm, n, x, alpha=0.05, **kwargs):
    ewma, ewmv = ewm
    if n == 0:
        ewma = x
        ewmv = 0.0
    elif n == 1:
        ewma = alpha*x + (1-alpha)*ewma
        ewmv = x
    else:
        ewma = alpha*x + (1-alpha)*ewma
        ewmv = (1-alpha)*(ewmv + alpha*(x - ewma)**2)
    return ewma, ewmv

def update_error_moments(mean_var, n, x, y, **kwargs):
    return update_moments(mean_var, n, x - y, **kwargs)

def update_error_min(minimum, n, x, y, **kwargs):
    return update_min(minimum, n, x - y, **kwargs)

def update_error_max(maximum, n, x, y, **kwargs):
    return update_max(maximum, n, x - y, **kwargs)
    
