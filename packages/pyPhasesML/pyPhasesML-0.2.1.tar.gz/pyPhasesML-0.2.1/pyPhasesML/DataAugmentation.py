import numpy as np
from numpy.random import default_rng
from pyPhases import classLogger


@classLogger
class DataAugmentation:
    def __init__(self, config, splitName) -> None:
        self.segmentAugmentation = config["segmentAugmentation"]
        self.config = config
        self.splitName = splitName

    def step(self, stepname, X, Y, **options):
        # check if augmentation step exist

        if hasattr(self, stepname):
            # call method
            return getattr(self, stepname)(X, Y, **options)
        else:
            raise Exception(f"DataAugmentation {stepname} not found")

    def __call__(self, Segment):
        X, Y = Segment
        return self.augmentSegment(X, Y)

    def augmentSegment(self, X, Y):
        X = np.expand_dims(X, axis=0)
        Y = np.expand_dims(Y, axis=0)

        for c in self.segmentAugmentation:
            X, Y = self.loadFromConfig(c, X, Y, self.splitName)

        return X[0], Y[0]

    def loadFromConfig(self, config, X, Y, splitName):
        config = config.copy()
        name = config["name"]
        del config["name"]

        if "trainingOnly" in config:
            if config["trainingOnly"] and splitName != "training":
                return X, Y
            del config["trainingOnly"]

        return self.step(name, X, Y, **config)