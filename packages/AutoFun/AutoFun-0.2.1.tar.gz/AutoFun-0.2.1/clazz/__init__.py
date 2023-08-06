import pkgutil,os
import inspect
from clazz import demo
classes = []
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)
    # print('module is ')
    # print(module)
    # print('\n')
    for name, value in inspect.getmembers(module):
        # globals()[name] = value
        # print(value)
        # print('\n')
        # if inspect.isclass(value) and issubclass(value, Template) and value is not Template and not getattr(value, 'ignore', False):
        if inspect.isclass(value) and issubclass(value, demo.TableObject) and value is not demo.TableObject:
            classes.append(value)
        # classes.append(value)
__all__ = __ALL__ = classes
print(classes)