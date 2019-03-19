# fastscore.schema.0: double
# fastscore.schema.1: double
# fastscore.schema.3: mapdouble

def begin():
    global calcbundle
    calcbundle = StreamingCalcBundle()
    calcbundle + StreamingCalc(update_moments, name="Moments", val=(0,0))
    calcbundle + StreamingCalc(update_max, name="Maximum")
    calcbundle + StreamingCalc(update_min, name="Minimum")

def action(x):
    global calcbundle
    yield (1, x)

    values = calcbundle.values
    mean, std = values["Moments"]
    maxi = values["Maximum"]
    mini = values["Minimum"]

    yield (3, {"Mean": mean, "StdDev": std, "Max": maxi, "Min": mini})


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

def update_min(minimum, n, x, **kwargs):
    return min(x, minimum) if n > 0 else x

def update_max(maximum, n, x, **kwargs):
    return max(x, maximum) if n > 0 else x

# n.b. this can also be updated to include skewness, kurtosis
def update_moments(mean_var, n, x, **kwargs):
    mean, var = mean_var
    mean_x = mean + (x - mean)/(n + 1)
    var_x = (n*var + (x - mean)*(x - mean_x))/(n + 1)
    return mean_x, var_x
