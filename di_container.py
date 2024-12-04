
class DIContainer:
    def __init__(self):
        self._registrations = {}

    def register(self, interface, implementation):
        self._registrations[interface] = implementation

    def resolve(self, interface):
        implementation = self._registrations.get(interface)
        if not implementation:
            raise ValueError(f"No registration for {interface}")

        if callable(implementation):
            return implementation()

        constructor = implementation.__init__
        if constructor is object.__init__:
            return implementation()
        params = constructor.__code__.co_varnames[1:constructor.__code__.co_argcount]
        dependencies = [self.resolve(param) for param in params]
        return implementation(*dependencies)

