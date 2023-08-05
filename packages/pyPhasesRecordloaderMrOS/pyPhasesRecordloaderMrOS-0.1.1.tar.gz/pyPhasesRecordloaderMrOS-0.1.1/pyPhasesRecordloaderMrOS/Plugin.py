from pyPhases import PluginAdapter
from pyPhasesRecordloader import RecordLoader


class Plugin(PluginAdapter):
    def initPlugin(self):
        # self.project.loadConfig(self.project.loadConfig(pathlib.Path(__file__).parent.absolute().joinpath("config.yaml")))
        RecordLoader.registerRecordLoader(
            "RecordLoaderMrOS", "pyPhasesRecordloaderMrOS.recordLoaders"
        )
        RecordLoader.registerRecordLoader(
            "MrOSAnnotationLoader", "pyPhasesRecordloaderMrOS.recordLoaders"
        )
        mrosPath = self.getConfig("mros-path")
        self.project.setConfig(
            "loader.mros.dataset.downloader.basePath",
            mrosPath + "/polysomnography/edfs/visit1/",
        )
        self.project.setConfig(
            "loader.mros.dataset.downloader.basePathExtensionwise",
            [
                mrosPath + "polysomnography/edfs/visit1/",
                mrosPath + "polysomnography/annotations-events-nsrr/visit1/",
                mrosPath + "polysomnography/edfs/visit2/",
                mrosPath + "polysomnography/annotations-events-nsrr/visit2/",
            ],
        )

        # self.project.setConfig("loader.visit2.dataset.downloader.basePath", mrosPath + "/polysomnography/edfs/visit2")
        # self.project.setConfig(
        #     "loader.visit2.dataset.downloader.basePathExtensionwise",
        #     [mrosPath + "polysomnography/edfs/visit2", mrosPath + "polysomnography/annotations-events-nsrr/visit2"],
        # )
