import flask, inspect, re
import azure.functions as func
from typing import Callable, Union
from .route_info import parse_project, parse_project_v2, from_app, ROUTE_INFO
from . import logger


FIND_PARAMS_NAMES_REGEX = re.compile(r"\{(.*?)\}")
FIND_REGEX_CONSTRAINT = re.compile(r"regex\(([^}]*)\)")


def adjust_route_for_flask(route: str) -> str:
	"""
	Converts the route definition of Azure Function to the Flask format.
	The only constraint supported is "regex:()".
	"""
	for param in FIND_PARAMS_NAMES_REGEX.findall(route):
		if ":" in param:
			name, constraint = param.split(":", 1)
			try:
				constraint = FIND_REGEX_CONSTRAINT.findall(constraint)[0]
				route = route.replace("{"+param+"}",
					"<regex(\"{}\"):{}>".format(constraint, name))
			except:
				logger.warning("Constraint not supported: {}. Fall back to route".format(tup[0]))
				route = route.replace("{"+param+"}", "<string:{}>".format(param))
		else:
			route = route.replace("{"+param+"}", "<string:{}>".format(param))
	return "{}{}".format(
		"" if route.startswith("/") else "/",
		route
	)


def flask_request_to_azure(req: flask.Request) -> func.HttpRequest:
	return func.HttpRequest(
		req.method,
		req.path,
		headers={**req.headers},
		route_params=req.view_args,
		params={**req.args},
		body=req.stream.read()
	)


def azure_response_to_flask(res: func.HttpResponse) -> flask.Response:
	return flask.Response(
		res.get_body(),
		status=res.status_code,
		headers={**res.headers}
	)


def wrap_handler(handler: Callable):
	def wrapper(*args, **kwargs):
		from flask import request
		return azure_response_to_flask(handler(flask_request_to_azure(request)))
	wrapper.__name__ = "{}_{}".format(
		handler.__module__.replace(".", "_"),
		handler.__name__
	)
	return wrapper


def build_blueprint(name: str, route_infos: list[ROUTE_INFO]) -> flask.Blueprint:
	blueprint = flask.Blueprint(name, __name__)
	for path, methods, handler, input_name in route_infos:
		logger.debug("[{}] {}".format(",".join(methods), path))
		blueprint.route(
			adjust_route_for_flask(path),
			methods=methods,
			strict_slashes=False
		)(wrap_handler(handler))
	return blueprint


def build_app(path: str) -> flask.app.Flask:
	return _build_app(parse_project(path), name=path)


def build_app_v2(app: Union[str, "azure.functions.FunctionApp"]) -> flask.app.Flask:
	if isinstance(app, str):
		return _build_app(parse_project_v2(app))
	else:
		return _build_app(from_app(app))


def _build_app(route_infos: list[ROUTE_INFO], name: str = "<app>") -> flask.app.Flask:
	app = flask.Flask(__name__)
	app.register_blueprint(
		build_blueprint(
			f"FunctionApp <{name}>",
			route_infos
		)
	)
	return app
