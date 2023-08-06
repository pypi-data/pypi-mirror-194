
import random
import math
import numpy as np

from scipy.ndimage import affine_transform
from scipy.ndimage.filters import gaussian_filter, median_filter

class GaussianNoise:
    def __init__(self, mu=0.0, sigma=0.0, probability=1.0):

        self.mu = mu
        self.sigma = sigma
        self.probability = probability

        if not hasattr(self.mu, "__iter__"):
            self.mu = (self.mu,) * 2

        if not hasattr(self.sigma, "__iter__"):
            self.sigma = (self.sigma,) * 2

    def apply(self, img, masks=[]):

        if random.random() > self.probability:
            # Don't augment this time
            return img, masks

        mean = random.uniform(self.mu[0], self.mu[1])
        sigma = random.uniform(self.sigma[0], self.sigma[1])

        gaussian = np.random.normal(mean, sigma, img.shape)
        return img + gaussian, masks


class GaussianBlur:
    def __init__(self, sigma=0.0, probability=1.0):

        self.sigma = sigma
        self.probability = probability

        if not hasattr(self.sigma, "__iter__"):
            self.sigma = (self.sigma,) * 2

    def apply(self, img, masks=[]):

        if random.random() > self.probability:
            # Don't augment this time
            return img, masks

        sigma = random.uniform(self.sigma[0], self.sigma[1])

        return gaussian_filter(img, sigma=sigma), masks


class MedianBlur:
    def __init__(self, size=1.0, probability=1.0):

        self.size = size
        self.probability = probability

        if not hasattr(self.size, "__iter__"):
            self.size = (self.size,) * 2

    def apply(self, img, masks=[]):

        if random.random() > self.probability:
            # Don't augment this time
            return img, masks

        size = random.randint(self.size[0], self.size[1])

        return median_filter(img, size=size), masks


DIMS = ["ax", "cor", "sag"]


class Affine:
    def __init__(
        self,
        scale={"ax": 1.0, "cor": 1.0, "sag": 1.0},
        translate_percent={"ax": 0.0, "cor": 0.0, "sag": 0.0},
        rotate={"ax": 0.0, "cor": 0.0, "sag": 0.0},
        shear={"ax": 0.0, "cor": 0.0, "sag": 0.0},
        mode="constant",
        cval=-1,
        probability=1.0,
    ):

        self.scale = scale
        self.translate_percent = translate_percent
        self.rotate = rotate
        self.shear = shear
        self.probability = probability

        for d in self.rotate:
            if not hasattr(self.rotate[d], "__iter__"):
                self.rotate[d] = (self.rotate[d],) * 2

        for d in self.scale:
            if not hasattr(self.scale[d], "__iter__"):
                self.scale[d] = (self.scale[d],) * 2

        for d in self.translate_percent:
            if not hasattr(self.translate_percent[d], "__iter__"):
                self.translate_percent[d] = (self.translate_percent[d],) * 2

        for d in self.shear:
            if not hasattr(self.shear[d], "__iter__"):
                self.shear[d] = (self.shear[d],) * 2

        for d in self.scale:
            if not hasattr(self.scale[d], "__iter__"):
                self.scale[d] = (self.scale[d],) * 2

    def get_rot(self, theta, d):
        if d == "ax":
            return np.matrix(
                [
                    [1, 0, 0, 0],
                    [0, math.cos(theta), -math.sin(theta), 0],
                    [0, math.sin(theta), math.cos(theta), 0],
                    [0, 0, 0, 1],
                ]
            )

        if d == "cor":
            return np.matrix(
                [
                    [math.cos(theta), 0, math.sin(theta), 0],
                    [0, 1, 0, 0],
                    [-math.sin(theta), 0, math.cos(theta), 0],
                    [0, 0, 0, 1],
                ]
            )

        if d == "sag":
            return np.matrix(
                [
                    [math.cos(theta), -math.sin(theta), 0, 0],
                    [math.sin(theta), math.cos(theta), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ]
            )

    def get_shear(self, shear):

        mat = np.identity(4)
        mat[0, 1] = shear[1]
        mat[0, 2] = shear[2]
        mat[1, 0] = shear[0]
        mat[1, 2] = shear[2]
        mat[2, 0] = shear[0]
        mat[2, 1] = shear[1]

        return mat

    def apply(self, img, masks=[]):

        if random.random() > self.probability:
            # Don't augment this time
            return img, masks

        deg_to_rad = math.pi / 180

        t_prerot = np.identity(4)
        t_postrot = np.identity(4)
        for i, d in enumerate(DIMS):
            t_prerot[i, -1] = -img.shape[i] / 2
            t_postrot[i, -1] = img.shape[i] / 2

        t = t_postrot

        for i, d in enumerate(DIMS):
            t = t * self.get_rot(
                random.uniform(self.rotate[d][0], self.rotate[d][1]) * deg_to_rad, d
            )

        for i, d in enumerate(DIMS):
            scale = np.identity(4)
            scale[i, i] = 1 / random.uniform(self.scale[d][0], self.scale[d][1])
            t = t * scale

        shear = []
        for i, d in enumerate(DIMS):
            shear.append(random.uniform(self.shear[d][0], self.shear[d][1]))

        t = t * self.get_shear(shear)

        t = t * t_prerot

        for i, d in enumerate(DIMS):
            trans = [p * img.shape[i] for p in self.translate_percent[d]]
            translation = np.identity(4)
            translation[i, -1] = random.uniform(trans[0], trans[1])
            t = t * translation

        augmented_image = affine_transform(img, t, mode="mirror")
        augmented_masks = []
        for mask in masks:
            augmented_masks.append(affine_transform(mask, t, mode="nearest"))

        return augmented_image, augmented_masks
