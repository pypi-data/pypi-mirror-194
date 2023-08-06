import sys
from typing import Callable
from .settings import load_project
from .functions import Function, Project
from . import logger


ROUTE_INFO = tuple[str, list[str], Callable, str]


def parse_project(path: str) -> list[ROUTE_INFO]:
	r = load_project(path)
	sys.path.insert(1, path)
	p = Project(r["project"])
	params = []
	for f in r["functions"]:
		try:
			t = Function(*f)
			url = "{}/{}".format(p.route_prefix, t.trigger.route)
			logger.info("[{}] {} {}".format(t.func_name, ", ".join(t.trigger.methods).upper(), url))
			params.append((
				url,
				t.trigger.methods,
				t.load_main(),
				t.trigger.name
			))
		except ValueError as e:
			logger.warning("[{}] Unable to mount Function: {}".format(f[0], e))
	return params
