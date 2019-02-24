import functools
import traceback
import json

INDENT = 4*' '
INDENT_GENERAL = 0

#TRACING = True
TRACING = False

def indent(txt):
    global INDENT_GENERAL
    return '\n'.join(" " * INDENT_GENERAL + line for line in  txt.splitlines())


def stacktrace(func):
    @functools.wraps(func)
    def wrapped(*args, **kwds):
        # Get all but last line returned by traceback.format_stack()
        # which is the line below.'
        global INDENT_GENERAL
        INDENT_GENERAL += 4
        callstack = '\n'.join([INDENT+line.strip() for line in traceback.format_stack()][:-1])
        if TRACING:
            print('\n' + indent('-'*len('{}() called:'.format(func.__name__))))
            print(indent('{}() called:'.format(func.__name__)))
            print(indent(callstack))
        return_value = func(*args, **kwds)
        INDENT_GENERAL -= 4
        return return_value

    return wrapped


def trace(message):
    if TRACING:
        print()
        print(indent(message))
        print()
    pass

def format_json(json_array):
    """
    Returns a human-readable JSON array
    """
    return json.dumps(json_array, sort_keys=True, indent=4, separators=(',', ': '))

def pretty_print(json_array):
    """
    Prints a formatted JSON array
    """
    if TRACING:
        print(indent(format_json(json_array)))