import collections.abc

def exec_format_map(format_string, format_map) :
    """Format string as format literal.

    Attrs:
        format_string:
            String to fromat.

    TODO:
        Documentation.
    """
    return eval(f'f"""{format_string}"""', globals(), format_map)

def exec_format(format_string, context) :
    return exec_format_map(format_string, context)


#class Composer (collections.abc.Mapping) :
#    def __init__(self, context) :
#        self.context = context
#        return
#    def __getitem__(self, name) :
#        return self.attributes[name]
#    def __iter__(self) :
#        return iter(self.attributes)
#    def __len__(self) :
#        return len(self.attributes)
#    def add_attribute(self, name, value) :
#        self._attributes[name] = value
#        return
#    def spawn(self) :
#        return Context(self)
#    @property
#    def attributes(self) :
#        if self.parent is None :
#            return self._attributes
#        return {**self.parent.attributes, **self._attributes}
#    def format_str(self, format_str) :
#        return exec_format(format_str, self.attributes)
#    pass



