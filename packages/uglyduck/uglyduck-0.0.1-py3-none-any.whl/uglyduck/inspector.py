import importlib
import inspect
import sys
import types
import typing

from uglyduck import parse


class TypeInspector:
    def __init__(self, module_path):
        self.module_path = module_path
        self.imports = ['typing']
        self.functions = {}
        self.classes: dict = {}
        self.class_map = {}
        self.current_module = None

    def is_interface_method_name(self, name):
        return len(name) > 1 and name.startswith('I') and name[1].isupper()

    def add_import(self, from_path, to_import=None):
        if from_path == 'inspect' and to_import == '_empty':
            return
        if to_import is None:
            self.imports.append(from_path)
        else:
            self.imports.append((from_path, to_import))

    def get_type_module(self, _type):
        return hasattr(_type, '__module__') and _type.__module__ or None

    def get_mro_names(self, cls):
        return [f'{t.__module__}.{t.__name__}' for t in cls.mro()]

    def get_type_name(self, t):
        _type = type(t)

        if self.get_type_module(_type) == 'types' and isinstance(t, types.GenericAlias):
            str_type = str(t)
            if str_type.startswith('list['):
                t = list(t.__args__)
                _type = type(t)

        if isinstance(t, type):
            if t.__module__ not in ['builtins', self.current_module.__name__]:
                self.add_import(t.__module__, t.__name__)

            if t.__module__ == self.current_module.__name__:
                type_name = 'I' + t.__name__
            else:
                if self.is_interface_method_name(t.__name__):
                    type_name = f"'{t.__name__}'"
                else:
                    type_name = t.__name__
        elif isinstance(t, types.FunctionType):
            type_name = self.get_type_name(t.__annotations__.get('return', typing.Any))
        elif isinstance(t, tuple):
            items = ', '.join([self.get_type_name(item) for item in t])
            type_name = f'typing.Tuple[{items}]'
        elif _type in [
            list,
            typing.List,
        ]:
            if len(t) == 0:
                type_name = 'typing.List[typing.Any]'
            else:
                list_type = self.get_type_name(t[0])
                type_name = f'typing.List[{list_type}]'
        elif isinstance(t, dict):
            items = ', '.join([self.get_type_name(item) for item in t])
            type_name = f'typing.Dict[{items}]'
        elif isinstance(t, (int, float, bool, str)):
            if isinstance(t, str) and str(t) in self.current_module.__dict__ or str(t) in self.classes:
                type_name = f"'I{t}'"
            else:
                type_name = type(t).__name__
        else:
            if self.get_type_module(t) in ['typing', 'types']:
                if _type in [
                    types.GenericAlias,
                    typing._UnionGenericAlias,
                    typing._GenericAlias,
                ]:
                    type_cls_name = str(t).split('[')[0]
                    type_name = f'{type_cls_name}[{self.get_type_name(t.__args__[0])}]'
                elif _type == typing.ForwardRef:
                    forward_ref = t.__forward_arg__
                    if forward_ref in self.current_module.__dict__:
                        type_name = f"'I{forward_ref}'"
                    else:
                        type_name = t.__forward_arg__
                else:
                    type_name = str(t)
            else:
                cls = t.__class__
                if cls.__module__ != 'builtins':
                    self.add_import(cls.__module__, cls.__name__)
                type_name = str(cls.__name__)

        if type_name in [
            'NoneType',
            '_empty',
        ]:
            type_name = 'typing.Any'
        return type_name

    def make_protocol_method(self, method, ident=4):
        arguments = []
        annotations = method.__annotations__
        method_signature = inspect.signature(method)
        for name in method_signature.parameters.keys():
            default = method_signature.parameters[name].default
            if str(default) == "<class 'inspect._empty'>":
                default = ''
            else:
                default = f' = {str(default)}'

            if name in annotations:
                param = annotations[name]
                arguments.append(f'{name}: {self.get_type_name(param)}{default}')
            elif default:
                param = method_signature.parameters[name].default
                arguments.append(f'{name}: {self.get_type_name(param)}{default}')
            else:
                arguments.append(f'{name}{default}')

        if 'return' in annotations:
            return_type = annotations['return']
            return_display = self.get_type_name(return_type)
            return_annotation = f' -> {return_display}'
        else:
            return_annotation = ''

        return {
            method.__name__: f"""
{' ' * ident}def {method.__name__}({', '.join(arguments)}){return_annotation}:
{' ' * ident}    ...
"""}

    def make_class_protocol(self, cls):
        protocol_name = 'I' + cls.__name__
        if cls.__name__ in self.class_map:
            print(f"Non-unique class name {cls.__name__} discovered.")
            return
        self.class_map[cls.__name__] = protocol_name

        try:
            annotations = cls.__annotations__
        except AttributeError:
            annotations = {}

        typing_protocol = 'typing.Protocol'
        parents = [typing_protocol]

        for parent_cls in cls.mro():
            if parent_cls == cls:
                continue

            if parent_cls.__name__ in self.class_map:
                if typing_protocol in parents:
                    parents.remove(typing_protocol)
                parents.insert(0, self.class_map[parent_cls.__name__])

        if '__iter__' in cls.__dict__:
            iter_annotations = cls.__dict__['__iter__'].__annotations__
            if 'return' in iter_annotations:
                iter_type = 'typing.Any'
                if isinstance(iter_annotations['return'], typing._GenericAlias):
                    iter_type = iter_annotations['return'].__args__[0]
                    if isinstance(iter_type, typing.ForwardRef):
                        iter_type = self.get_type_name(iter_type.__forward_arg__)
                    else:
                        iter_type = self.get_type_name(iter_type)

                parents.append(f"typing.Iterable[{iter_type}]")

        parent_classes = ', '.join(reversed(parents))
        code = f"""\n
class {protocol_name}({parent_classes}):
"""
        attributes = {}
        methods = {}
        class_methods = {}
        static_methods = {}
        init_attributes = {}

        for name, method in cls.__dict__.items():
            if name.startswith('_') and name != '__init__':
                continue

            if isinstance(method, type):
                pass
            elif isinstance(method, types.FunctionType):
                methods.update(self.make_protocol_method(method, ident=4))
            elif isinstance(method, classmethod):
                class_methods.update(self.make_protocol_method(method.__func__, ident=4))
            elif isinstance(method, staticmethod):
                static_methods.update(self.make_protocol_method(method.__func__, ident=4))
            elif isinstance(method, property):
                method_signature = inspect.signature(method.fget)
                return_type = method_signature.return_annotation
                return_name = self.get_type_name(return_type)
                attributes[name] = f'    {name}: {return_name}\n'
            else:
                if name in annotations:
                    return_type = annotations[name]
                    return_name = self.get_type_name(return_type)
                else:
                    return_name = self.get_type_name(method)
                attributes[name] = f'    {name}: {return_name}\n'

        if '__init__' in cls.__dict__:
            init_attributes = parse.get_func_obj_self_vars(cls)

        for attribute in attributes.values():
            code += attribute

        if init_attributes:
            code += '    # __init__ attributes\n'
            for name, _type in init_attributes.items():
                if name in attributes:
                    continue

                return_name = self.get_type_name(_type)
                code += f'    {name}: {return_name}\n'

        for method in methods.values():
            code += method

        for method in class_methods.values():
            code += f'\n    @classmethod{method}'

        for method in static_methods.values():
            code += f'\n    @staticmethod{method}'

        if len(attributes) == 0 and len(methods) == 0 and len(class_methods) == 0 and len(init_attributes) == 0:
            code += '    pass\n'

        self.classes[protocol_name] = code

    def make_item(self, func):
        if isinstance(func, type):
            self.make_class_protocol(func)
        elif isinstance(func, types.FunctionType):
            self.functions.update(self.make_protocol_method(func, ident=0))

    @classmethod
    def get_path_to_module(cls, module_name):
        if isinstance(module_name, str):
            mod = sys.modules[module_name]
        else:
            mod = module_name

        return mod.__file__

    def make_imports(self):
        module_import = {}
        to_import = []
        for imp in self.imports:
            if isinstance(imp, str):
                to_import.append(f"import {imp}\n")
            else:
                module, name = imp
                if module == self.module_path:
                    continue

                if module not in module_import:
                    module_import[module] = []
                module_import[module].append(name)

        for module, names in module_import.items():
            names = sorted(list(set(names)))
            to_import.append(f"from {module} import {', '.join(names)}\n")

        to_import = list(set(to_import))
        to_import = sorted(to_import, reverse=True)
        return ''.join(to_import)

    @classmethod
    def make_package_types_file(cls, package, modules=None, ignore=None):
        if ignore is None:
            ignore = []

        path = cls.get_path_to_module(package)
        path = '/'.join(path.split('/')[:-1])
        export_to = f'{path}/types.py'
        module_path = f'{package}.types'

        inspector = cls(module_path)
        if modules is not None:
            modules_to_type = []
            for module_name in modules:
                if module_name not in sys.modules:
                    importlib.import_module(module_name)
            for sys_module_name in sys.modules:
                for module_name in modules:
                    if sys_module_name.startswith(module_name):
                        modules_to_type.append(sys_module_name)
                        break
        else:
            modules_to_type = [module for module in sys.modules if module.startswith(package)]

        for module_name in modules_to_type:
            if module_name.endswith('.types') or module_name in ignore:
                continue

            try:
                mod = sys.modules[module_name]
            except KeyError:
                mod = importlib.import_module(module_name)

            module = mod.__dict__
            items = module.keys()
            inspector.current_module = mod
            for item in items:
                if item.startswith('_'):
                    continue

                if not callable(module[item]) or not inspect.isclass(module[item]):
                    continue

                if module[item].__module__ != module_name:
                    continue

                inspector.make_item(module[item])

        import_str = inspector.make_imports()
        code_str = ''.join(inspector.classes.values())
        with open(export_to, 'w') as f:
            f.write(f"{import_str}\n# Generated with uglyduck\n\n{code_str}")
