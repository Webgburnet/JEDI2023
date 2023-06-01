from .naivedict import NaiveDict
from .simpledict import SimpleDict

get = {
    "naive": NaiveDict,
    "simple": SimpleDict,
}

choices = list(get.keys())

default = "naive"
