from os.path import join, isdir, isfile
from os import mkdir


class GCRecourse:

    default_root = r"D:\Projects\DiscordBots\GameCenter\resource"

    def __init__(self, module, root=default_root):
        self.module = module
        self.full_path = join(root, self.module)
        assert isdir(self.full_path)

    def get_submodule(self, module):
        return GCRecourse(module, self.full_path)

    def get_resource(self, source):
        resource_path = join(self.full_path, source)
        assert isfile(resource_path)
        return resource_path

    def create_submodule(self, module):
        full_path = join(self.full_path, module)
        if not isdir(full_path):
            mkdir(full_path)
            return self.get_submodule(module)
        else:
            return None

    def create_resource(self, source):
        resource_path = join(self.full_path, source)
        if not isfile(resource_path):
            with open(resource_path, 'w') as _:
                pass
            return self.get_resource(source)
        else:
            return None
