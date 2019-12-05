"""
Contains a set of independent free functions for tracing. They can be used privately by the other modules of minicrm
package, but client code can use them directly as well.
"""

__author__ = "Adam Rudolf"
__copyright__ = "Adam Rudolf, 2018"

import functools
import json
import traceback

INDENT = 4 * ' '
INDENT_GENERAL = 0

TRACING = True
"""Global variable to turn tracing on/off."""


TRACING = False


def indent(txt):
    """
    Returns a string with the current log indentation, based on the call stack depth.

    :param txt: the text to be indented and returned. Can be multiline.
    :type txt: str

    :return: txt param, concatendated to a number of spaces, matching to the current log indentation. If txt is
             multiline, all lines will be indented.
    :rtype: str
    """

    global INDENT_GENERAL
    return '\n'.join(" " * INDENT_GENERAL + line for line in txt.splitlines())


def stacktrace(func):
    """
    Decorator, which

    - adds 4 spaces to the current indentation level

    - prints the name of the wrapped

    - prints the current call stack

    - calls the wrapped

    - subtracts 4 spaces from the current indentation

    Usage on the example function "get_today":

    .. code-block:: python

      @stacktrace
      def get_today(self):
          return self._today

    Doesn't print anything if TRACING is set to False.

    :param func: the wrapped function
    :type func: function

    :return: return of func
    """

    @functools.wraps(func)
    def wrapped(*args, **kwds):
        # Get all but last line returned by traceback.format_stack()
        # which is the line below.'
        global INDENT_GENERAL
        INDENT_GENERAL += 4
        callstack = '\n'.join([INDENT + line.strip() for line in traceback.format_stack()][:-1])
        if TRACING:
            print('\n' + indent('-' * len('{}() called:'.format(func.__name__))))
            print(indent('{}() called:'.format(func.__name__)))
            print(indent(callstack))
        return_value = func(*args, **kwds)
        INDENT_GENERAL -= 4
        return return_value

    return wrapped


def trace(message):
    """
    Indents and prints the given string, surrounded by empty lines.

    Doesn't print anything if TRACING is set to False.

    :param message: the message to be logged.
    :type message: str

    :return: None
    """

    if TRACING:
        print("\n" + indent(message) + "\n")


def format_json(json_array):
    """
    Returns a human-readable JSON array.

    It gets the array as a (minified) srting, and inserts separators, newlines and indentation.

    :param json_array: the JSON array as a minified string without whitespaces
    :type json_array: str

    :return: the formatted JSON array
    :rtype: str
    """

    return json.dumps(json_array, sort_keys=True, indent=4, separators=(',', ': '))


def pretty_print(json_array):
    """
    Prints a human-readable JSON array.

    It gets the array as a (minified) srting, and inserts separators, newlines and indentation.

    Doesn't print anything if TRACING is set to False.

    :param json_array: the JSON array as a minified string without whitespaces
    :type json_array: dict

    :return: None
    """
    if TRACING:
        print(indent(format_json(json_array)))
