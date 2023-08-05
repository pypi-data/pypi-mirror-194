# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashEventSource(Component):
    """A DashEventSource component.
An interface to server sent events in Dash

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- close (boolean; optional):
    Close event source.

- error (string; optional):
    Error.

- message (string; optional):
    Received message.

- readyState (number; optional):
    A number representing the state of the connection. Possible values
    are CONNECTING (0), OPEN (1), or CLOSED (2).

- url (string; required):
    A DOMString representing the URL of the source.

- withCredentials (boolean; optional):
    A boolean value indicating whether the EventSource object was
    instantiated with cross-origin (CORS) credentials set (True), or
    not (False, the default)."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, close=Component.UNDEFINED, error=Component.UNDEFINED, message=Component.UNDEFINED, readyState=Component.UNDEFINED, withCredentials=Component.UNDEFINED, url=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'close', 'error', 'message', 'readyState', 'url', 'withCredentials']
        self._type = 'DashEventSource'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'close', 'error', 'message', 'readyState', 'url', 'withCredentials']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['url']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashEventSource, self).__init__(**args)
