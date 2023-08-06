import importlib.metadata


try:
	__version__ = importlib.metadata.version('umbraSnscrpe')
except importlib.metadata.PackageNotFoundError:
	__version__ = None
