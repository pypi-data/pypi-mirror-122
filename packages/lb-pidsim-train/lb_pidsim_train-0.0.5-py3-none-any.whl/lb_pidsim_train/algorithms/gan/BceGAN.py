from __future__ import annotations

import os
import numpy as np
import tensorflow as tf
import matplotlib as mpl
import matplotlib.pyplot as plt

from lb_pidsim_train.algorithms.gan import GAN


d_loss_tracker = tf.keras.metrics.Mean ( name = "d_loss" )
"""Metric instance to track the discriminator loss score."""

g_loss_tracker = tf.keras.metrics.Mean ( name = "g_loss" )
"""Metric instance to track the generator loss score."""


class BceGAN (GAN):
  """Keras model class to build and train BceGAN system.
  
  Parameters
  ----------
  discriminator : `tf.keras.Sequential`
    ...

  generator : `tf.keras.Sequential`
    ...

  latent_dim : `int`, optional
    ... (`64`, by default).

  Attributes
  ----------
  discriminator : `tf.keras.Sequential`
    ...

  generator : `tf.keras.Sequential`
    ...

  latent_dim : `int`
    ...

  Notes
  -----
  ...

  References
  ----------
  ...

  See Also
  --------
  ...

  Methods
  -------
  ...
  """