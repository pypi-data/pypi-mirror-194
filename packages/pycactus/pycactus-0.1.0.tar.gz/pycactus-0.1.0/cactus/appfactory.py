"""
WSGI application builder.
"""
from .webapp import WebApp
from .route_info import parse_project


def build_app(path: str):
	return WebApp(parse_project(path))
