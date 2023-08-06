
import inspect
def getFuncArgumens(func):
    result = []
    # print(func,inspect.signature(func))
    # print(func, inspect.signature(func).parameters.values())
    for item in inspect.signature(func).parameters.values():
        result.append(convertParameter(item))
    return result


def convertParameter(item: inspect.Parameter):
    # result={}
    kind = item.kind
    formatted = item._name

    if item._annotation is not inspect._empty:
        formatted = '{}: {}'.format(formatted,
                                    inspect.formatannotation(item._annotation))

    # Add annotation and default value
    if item._default is not inspect._empty:
        if item._annotation is not inspect._empty:
            formatted = '{} = {}'.format(formatted, repr(item._default))
        else:
            formatted = '{}={}'.format(formatted, repr(item._default))

    if kind == inspect._VAR_POSITIONAL:
        formatted = '*' + formatted
    elif kind == inspect._VAR_KEYWORD:
        formatted = '**' + formatted

    return formatted