class PyCharm:
    def execute(self):
        print('Code compiled')
        print('Code running')

class Code:
    def code(self, ide):
        return ide.execute()

code = Code()
ide = PyCharm()
code.code(ide)