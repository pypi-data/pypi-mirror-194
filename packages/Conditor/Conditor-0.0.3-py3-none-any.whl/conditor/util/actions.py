import conditor.action

DEFAULT_ACTION = 'TestAction'

class TestAction (conditor.action.Action) :
    def run(self) :
        print('HEERE')
        return repr(self)
    pass

