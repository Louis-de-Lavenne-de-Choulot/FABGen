# Harfang - The Fabulous binding Generator for CPython and Rust
# 	Copyright (C) 2023 Louis de Lavenne, David Cuahontes, Leo Chartier, Max Bernard & Jason Grosse

import gen

def route_lambda(name):
	return lambda args: "%s(%s);" % (name, ", ".join(args))

def clean_name(name):
    return name.replace("::", "_")

def clean_name_with_title(name):
    return name.replace("::", "_").title()

class RustTypeConverterCommon(gen.TypeConverter):
    def __init__(self, type):
        super().__init__(type)

    def get_type_api(self, module_name):
        out = '// type API for %s\n' % self.ctype
        if self.c_storage_class:
            out += 'struct %s;\n' % self.c_storage_class
        if self.c_storage_class:
            out += 'void %s(int idx, void *obj %s &storage '%(self.to_c_func, self.c_storage_class)
        else:
            out += 'void %s(int idx, void *obj '%(self.to_c_func)
        out += 'int (void *obj, OwnershipPolicy);\n' % self.from_c_func
        out += '\n'
        return out

    def to_c_call(self, out_var, expr):
        out = ''
        if self.c_storage_class:
            out += 'storage = %s' % out_var.replace('&', '_')
            

    def from_c_call(self, out_var, expr, ownership):
        return '%s((void *)%s, %s);\n' % (self.from_c_func, expr, ownership)

    def check_call(self, expr):
        return '%s(%s);\n' % (self.check_func, expr)


class DummyTypeConverter(gen.TypeConverter):
    def __init__(self, type, to_c_storage_type=None, bound_name=None, from_c_storage_type=None, needs_c_storage_class=False):
        super().__init__(type, to_c_storage_type, bound_name, from_c_storage_type, needs_c_storage_class)

    def get_type_api(self, module_name):
        return super().get_type_api(module_name)

class RustGenerator(gen.FABGen):
    default_ptr_converter = RustPtrTypeConverter
    default_class_converter = RustClassTypeDefaultConverter
    default_extern_converter = RustExternTypeConverter
    
    def __init__(self):
        super().__init__()
        self.check_self_type_in_ops = True

    def get_language(self):
        return "Rust"

    def output_includes(self):
        pass