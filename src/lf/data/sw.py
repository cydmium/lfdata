import numpy as np
import torch
import torch.utils.data
import copy
import pickle
import pdb

# ## train/test split & shuffling, data preprocessing
import torch.utils.data as data


class swDataset(data.Dataset):
    """Solar wind Dataset"""

    def __init__(
        self,
        dataFile,
        split="train",
        valType="rand",
        trainPortion=0.7,
        normalize=True,
        portion=1,
        nVal=10,
    ):

        with open(dataFile, "rb") as f:
            x, y, feats = pickle.load(f)
        x, y = x[: int(portion * len(x))], y[: int(portion * len(y))]
        nsamples = np.shape(x)[0]
        nfeats = np.shape(x)[-1]

        valPortion = 0.15  # valPortion is 15% of the training data
        self.split = split

        if (
            valType == "rand"
        ):  # Decide whether to leave the data as sequential or randomly shuffled
            randidx = torch.randperm(nsamples)
            trainData = x[randidx[: int(trainPortion * len(randidx))]]
            trainLabels = y[randidx[: int(trainPortion * len(randidx))]]
            self.testData = x[randidx[int(trainPortion * len(randidx)) :]]
            self.testLabels = y[randidx[int(trainPortion * len(randidx)) :]]
            self.trainData = trainData[: np.int((1 - valPortion) * len(trainLabels))]
            self.trainLabels = trainLabels[
                : np.int((1 - valPortion) * len(trainLabels))
            ]
            self.valData = trainData[np.int((1 - valPortion) * len(trainLabels)) :]
            self.valLabels = trainLabels[np.int((1 - valPortion) * len(trainLabels)) :]

        if valType == "szn":
            trainData = x[: int(trainPortion * nsamples)]
            trainLabels = y[: int(trainPortion * nsamples)]
            self.testData = x[int(trainPortion * nsamples) :]
            self.testLabels = y[int(trainPortion * nsamples) :]

            self.trainData = trainData[: int(nsamples * (1 / nVal) * (1 - valPortion))]
            self.trainLabels = trainLabels[
                : int(nsamples * (1 / nVal) * (1 - valPortion))
            ]
            self.valData = trainData[
                int(nsamples * (1 / nVal) * (1 - valPortion)) : int(
                    nsamples * (1 / nVal)
                )
            ]
            self.valLabels = trainLabels[
                int(nsamples * (1 / nVal) * (1 - valPortion)) : int(
                    nsamples * (1 / nVal)
                )
            ]
            valDiff = int(nsamples * (1 / nVal)) - int(
                nsamples * (1 / nVal) * (1 - valPortion)
            )
            for i in range(1, nVal):
                start = np.int(i * nsamples * (1 / nVal))
                end = np.int((i + 1) * nsamples * (1 / nVal))
                self.trainData = torch.cat(
                    [self.trainData, trainData[start : end - valDiff]]
                )
                self.trainLabels = torch.cat(
                    [self.trainLabels, trainLabels[start : end - valDiff]]
                )
                self.valData = torch.cat([self.valData, trainData[end - valDiff : end]])
                self.valLabels = torch.cat(
                    [self.valLabels, trainLabels[end - valDiff : end]]
                )

        else:
            trainData = x[: int(trainPortion * nsamples)]
            trainLabels = y[: int(trainPortion * nsamples)]
            self.testData = x[int(trainPortion * nsamples) :]
            self.testLabels = y[int(trainPortion * nsamples) :]
            self.trainData = trainData[: np.int((1 - valPortion) * len(trainLabels))]
            self.trainLabels = trainLabels[
                : np.int((1 - valPortion) * len(trainLabels))
            ]
            self.valData = trainData[np.int((1 - valPortion) * len(trainLabels)) :]
            self.valLabels = trainLabels[np.int((1 - valPortion) * len(trainLabels)) :]

        for i in range(nfeats):
            mean = torch.tensor([torch.mean(trainData[:, :, i])])
            std = torch.tensor([torch.std(trainData[:, :, i])])

            self.trainData[:, :, i] -= mean
            self.testData[:, :, i] -= mean
            self.valData[:, :, i] -= mean

            if not (std == 0):
                self.trainData[:, :, i] /= std
                self.testData[:, :, i] /= std
                self.valData[:, :, i] /= std

        varStyles = np.array([1, -1, 1, 0, 0])
        if normalize:
            self.factors = torch.zeros(trainLabels.shape[-1])
            self.shifts = torch.zeros(trainLabels.shape[-1])
            for i in range(trainLabels.shape[-1]):
                if varStyles[i] == -1:
                    self.shifts[i] = 0
                    self.factors[i] = (
                        torch.min(self.trainLabels[:, :, i]) - self.shifts[i]
                    )
                elif varStyles[i] == 0:
                    self.shifts[i] = torch.mean(self.trainLabels[:, :, i])
                    self.factors[i] = torch.max(torch.abs(trainLabels[:, :, i]))
                else:
                    self.shifts[i] = 0
                    self.factors[i] = (
                        torch.max(self.trainLabels[:, :, i]) - self.shifts[i]
                    )

            self.testLabels -= self.shifts
            self.trainLabels -= self.shifts
            self.valLabels -= self.shifts

            self.testLabels /= self.factors
            self.trainLabels /= self.factors
            self.valLabels /= self.factors

    def __getitem__(self, index):
        if self.split == "train":
            data, labels = self.trainData[index], self.trainLabels[index]
        elif self.split == "val":
            data, labels = self.valData[index], self.valLabels[index]
        elif self.split == "test":
            data, labels = self.testData[index], self.testLabels[index]
        return data, labels

    def __len__(self):
        if self.split == "train":
            return len(self.trainData)
        elif self.split == "val":
            return len(self.valData)
        elif self.split == "test":
            return len(self.testData)

    def reconstruct(self, predictions):
        return predictions * self.factors + self.shifts
