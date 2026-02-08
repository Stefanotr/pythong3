from Utils.Logger import Logger


class BuildingModel:

    def __init__(self):
        try:
            Logger.debug("BuildingModel.__init__", "Building model initialized")
        except Exception as e:
            Logger.error("BuildingModel.__init__", e)