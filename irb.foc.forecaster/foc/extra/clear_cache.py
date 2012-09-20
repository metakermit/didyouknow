from foc.forecaster.common import conf
from dracula.cacher import Cacher

cacher = Cacher(host=conf.cache_host, port=conf.cache_port)
cacher.clear()
print("Cache cleared.")