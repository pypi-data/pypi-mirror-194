from pyPhases import PluginAdapter
# from pyPhasesPreprocessing.DataAugmentation import DataAugmentation

from .Preprocessing import Preprocessing


class Plugin(PluginAdapter):
    def __init__(self, project, options=...):
        super().__init__(project, options)

        def update(value):
            if value is None or value == "preprocessing":
                self.setupPreprocessing()

        self.project.on("configChanged", update)

    def setupPreprocessing(self):
        Preprocessing.setup(self.project.config)
        # DataAugmentation.setup(self.project.config)

    def initPlugin(self):
        self.setupPreprocessing()
