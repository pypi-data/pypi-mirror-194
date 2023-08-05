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
        # check if method exist in self

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

    # def augmentSegmentMap(self, splitName):
    #     return lambda S: self.config(S[0], S[1], splitName)

    def loadFromConfig(self, config, X, Y, splitName):
        config = config.copy()
        name = config["name"]
        del config["name"]

        if "trainingOnly" in config:
            if config["trainingOnly"] and splitName != "training":
                return X, Y
            del config["trainingOnly"]

        return self.step(name, X, Y, **config)

    """
    all data inputs (`array`) is expected to be in following default shape: (-1, Segementlength, Channelcount)
    """

    @staticmethod
    def paddingSegments(array, paddingSize):
        """adds a zero filled segments before and after the array

        Args:
            paddingSize ([int]): padding size in samples
        """
        _, windowSize, numChannels = array.shape
        padding = np.zeros((paddingSize, windowSize, numChannels))

        return np.concatenate((padding, array, padding))

    @staticmethod
    def temporalContext(array, contextSize):
        """Create a temporal context, by adding `contextSize` channels, with the content of
           future segments

        Args:
            contextSize ([int]): channel count to be added

        """
        _, windowSize, numChannels = array.shape
        size = len(array)

        marginSize = contextSize // 2
        paddedX = DataAugmentation.paddingSegments(array, marginSize)

        newX = np.empty((size, contextSize, windowSize, numChannels), dtype=array.dtype)

        for XId in range(marginSize, size + marginSize):
            startAt = XId - marginSize
            endWith = XId + marginSize + 1
            newX[startAt, ::, ::, ::] = paddedX[startAt:endWith, ::, ::]
            # assert all(newX[startAt, ::, 10] == array[startAt, ::, 0])

        return newX

    @staticmethod
    def shuffle(X, Y, seed=None):
        """shuffles all segments (axis=0)

        Args:
            seed ([int]): numpy seed to use

        """
        if not seed:
            seed = 2
        np.random.seed(seed)
        np.random.shuffle(X)
        np.random.seed(seed)
        np.random.shuffle(Y)

        return X, Y

    @staticmethod
    def channelShuffle(X, channelSlice, seed=None):

        rng = default_rng(seed)
        channelSlice = slice(channelSlice[0], channelSlice[1])

        cutChannels = X[:, :, channelSlice].copy()
        rng.shuffle(cutChannels, axis=2)
        X[:, :, channelSlice] = cutChannels

        return X

    @staticmethod
    def channelSelect(X, channelSlice=slice(0, None)):
        """selects all channels fitting the given slice

        Args:
            channelSlice (slice): array slice

        """

        return X[:, :, channelSlice]

    # @staticmethod
    # def znorm(X):
    #     X = (X - X.mean(axis=1, keepdims=True)) / (X.std(axis=1, keepdims=True) + 0.000000001)
    #     return X

    # @staticmethod
    # def MagScale(X, low=0.8, high=1.25, seed=2):
    #     rng = default_rng(seed)
    #     scale = low + rng.random(1, dtype=X.dtype) * (high - low)
    #     X = scale * X

    #     return X

    # @staticmethod
    # def reshapeWithOverlap(X, windowSize, stepSize):
    #     windowSize = int(windowSize)
    #     stepSize = int(stepSize)
    #     segmentLength = int(X.shape[1] / stepSize)
    #     newX = []
    #     for Xi in X:
    #         # padding
    #         paddingSize = int((windowSize / 2) - (stepSize / 2))
    #         padding = np.zeros((paddingSize, Xi.shape[1]))
    #         paddedX = np.concatenate((padding, Xi, padding))
    #         # list comprehension
    #         last_start = paddedX.shape[0] - windowSize + 1
    #         period_starts = range(0, last_start, stepSize)
    #         reshapedX = np.array([paddedX[k : k + windowSize, :] for k in period_starts])
    #         # reshape to numpy: (4,240,1200,2)
    #         newX.append(reshapedX)
    #     # parameters:
    #     # numSegements = 4 = X.shape[0]
    #     # predictionsPerSegment=240
    #     #
    #     return np.array(newX)

    # @staticmethod
    # def majorityVoteAnnotations(Y, windowSize, channel, reduce=False):
    #     windowSize = int(windowSize)
    #     segmentLength = Y.shape[1]
    #     channelCount = Y.shape[2]
    #     Y = Y.reshape(-1, windowSize, channelCount)
    #     for yIndex, _ in enumerate(Y):

    #         values, counts = np.unique(Y[yIndex, ::, channel], return_counts=True)
    #         majorityIndex = np.argmax(counts)

    #         Y[yIndex, ::, channel] = values[majorityIndex]

    #     Y = Y.reshape(-1, segmentLength, channelCount)
    #     if reduce:
    #         Y = Y[:, ::windowSize, :]

    #     return Y

    # @staticmethod
    # def cutForSegmentLength(X, Y, segmentLength):
    #     length = X.shape[1]
    #     if length % segmentLength != 0:
    #         f = length // segmentLength
    #         end = f * segmentLength
    #         X = X[:, :end, :]
    #         Y = Y[:, :end, :]
    #     return X, Y

    # @staticmethod
    # def gaussNoise(X, stddev=0.01):
    #     noise = np.random.normal(0, 0.05, X.shape).astype(X.dtype)
    #     return X + noise

    # def smoothWindow(Y, windowSize, threshHold=0):
    #     filter = np.full(windowSize, 1)
    #     assert Y.shape[0] == 1
    #     classCount = Y.shape[2]
    #     for i in range(classCount):
    #         Y[0, :, i] = np.convolve(Y[0, :, i], filter, "same")
    #     return Y / windowSize

    # def softMax(y):
    #     m = np.max(y, axis=2)
    #     m = m[:, :, np.newaxis]
    #     e_y = np.exp(y - m)
    #     div = np.sum(e_y, axis=2)
    #     div = div[:, :, np.newaxis]
    #     return e_y / div
