import tensorflow as tf
from tensorflow.math import log


class GAN:
  def __init__ (self, generator, discriminator):
    self.name = 'GAN'
    self.loss_name = 'GAN original loss'
    self.generator = generator
    self.discriminator = discriminator


  def _feed_loss (self, X_gen, X_ref, Y_ref, training):
    Y_gen = self.generator (X_gen, training = training)
    self.XY_gen = tf.concat ([X_gen, Y_gen], axis = 1)
    self.XY_ref = tf.concat ([X_ref, Y_ref], axis = 1)


  def generator_loss (self, X_gen, X_ref, Y_ref, w_gen, w_ref, training):
    self._feed_loss (X_gen, X_ref, Y_ref, training)
    noise_gen = tf.random.normal (tf.shape (self.XY_gen), mean = 0., stddev = 0.1)
    noise_ref = tf.random.normal (tf.shape (self.XY_ref), mean = 0., stddev = 0.1)
    D_gen = self.discriminator (self.XY_gen + noise_gen, training = training)
    D_ref = self.discriminator (self.XY_ref + noise_ref, training = training)

    loss = w_ref * log ( tf.clip_by_value (D_ref, 1e-12, 1.) ) + \
           w_gen * log ( tf.clip_by_value (1 - D_gen, 1e-12, 1.) )
    loss = tf.reduce_mean (loss)
    return loss


  def discriminator_loss (self, X_gen, X_ref, Y_ref, w_gen, w_ref, training):
    loss = - self.generator_loss (X_gen, X_ref, Y_ref, w_gen, w_ref, training)
    return loss