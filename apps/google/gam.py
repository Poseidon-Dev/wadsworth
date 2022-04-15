import os 

class BaseGam:

    def __init__(self):
        self.command = 'GAM '

    def update(self):
        self.command += 'UPDATE '
        return self

    def info(self):
        self.command += 'INFO '
        return self

    def run(self):
        return os.system(self.command)

class Groups(BaseGam):

    def __init__(self, group, func=''):
        super().__init__()
        self.domain = os.getenv('DOMAIN')
        if func.lower() == 'update':
            self.update()
        else:
            self.info()
        self.command += 'group ' + group + self.domain + ' '
        

        



    
        