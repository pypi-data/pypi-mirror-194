import sys, importlib
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


def parse_project_v2(path: str) -> list[ROUTE_INFO]:
	sys.path.insert(1, path)
	m = importlib.import_module("function_app")
	return from_app(m.app)


def from_app(app: "azure.functions.FunctionApp") -> list[ROUTE_INFO]:
	output = []
	for f in app.get_functions():
		if f.is_http_function():
			fname = f.get_function_name()
			trigger = f.get_trigger()
			handler = f.get_user_function()
			handler.__name__ = fname
			if trigger.methods is None:
				methods = ["GET"]
			else:
				methods = [str(x) for x in trigger.methods]
			logger.info("[{}] {} {}".format(fname, ",".join(methods), trigger.route))
			output.append((trigger.route, methods, handler, fname))
	return output
