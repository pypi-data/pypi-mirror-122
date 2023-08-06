import tensorflow as tf
from tensorflow.math import log

from .GAN import GAN


class Critic:
    def __init__ (self, h):
        self.h = h

    def __call__ (self, x_1, x_2):
        critic_func = tf.norm (self.h(x_1) - self.h(x_2), axis = 1) - \
                      tf.norm (self.h(x_1), axis = 1)
        return critic_func


class CramerGAN (GAN):
  def __init__ (self, generator, discriminator, grad_penalty = 1.):
    super().__init__ (generator, discriminator)
    self.name = 'CramerGAN'
    self.loss_name = 'Energy distance'
    self.gp = grad_penalty


  def _feed_loss (self, X_gen, X_ref, Y_ref, training):
    super()._feed_loss (X_gen, X_ref, Y_ref, training)
    self.critic = Critic (lambda x : self.discriminator (x, training = training))


  def generator_loss (self, X_gen, X_ref, Y_ref, w_gen, w_ref, training):
    self._feed_loss (X_gen, X_ref, Y_ref, training)
    self.XY_gen1, self.XY_gen2 = tf.split (self.XY_gen, 2)
    self.XY_ref1, self.XY_ref2 = tf.split (self.XY_ref, 2)
    self.w_gen1 , self.w_gen2  = tf.split (w_gen, 2)
    self.w_ref1 , self.w_ref2  = tf.split (w_ref, 2)

    # <--- YANDEX --->
    loss = self.w_ref1 * self.w_gen2 * self.critic (self.XY_ref1, self.XY_gen2) - \
           self.w_gen1 * self.w_gen2 * self.critic (self.XY_gen1, self.XY_gen2) 
    loss = tf.reduce_mean (loss)
    #loss = tf.reduce_sum ( self.w_ref1 * self.w_gen1 * self.w_gen2 * \
    #                       (self.critic (self.XY_ref1, self.XY_gen2) - \
    #                        self.critic (self.XY_gen1, self.XY_gen2)) ) / \
    #       tf.reduce_sum ( self.w_ref1 * self.w_gen1 * self.w_gen2 )
    # < --- >
    return loss

 
  @tf.function   # for tf.gradients
  def discriminator_loss (self, X_gen, X_ref, Y_ref, w_gen, w_ref, training):
    loss = - self.generator_loss (X_gen, X_ref, Y_ref, w_gen, w_ref, training)

    rnd = tf.random.uniform (
                              shape  = [tf.shape (self.XY_ref1) [0], 1] , 
                              minval = 0. , 
                              maxval = 1.
                            )
    self.XY_hat = rnd * self.XY_ref1 + (1 - rnd) * self.XY_gen1   # interpolation
    
    crit_hat = self.critic (self.XY_hat, self.XY_gen2)
    grad_hat = tf.gradients (crit_hat, self.XY_hat)
    # <--- YANDEX --->
    #grad_hat = tf.norm (grad_hat, axis = 1)
    grad_hat = tf.concat  (grad_hat, axis = 1)
    grad_hat = tf.reshape (grad_hat, shape = [tf.shape (grad_hat) [0], -1])

    slopes  = tf.norm (grad_hat, axis = 1)
    gp_term = tf.square ( tf.maximum ( tf.abs (slopes) - 1., 0. ) )
    gp_term = self.gp * tf.reduce_mean (gp_term)
    #gp_term = self.gp * tf.square (grad_hat - 1.)   # gradient penalty term
    #gp_term = tf.reduce_sum (self.w_ref1 * self.w_gen1 * self.w_gen2 * gp_term) / \
    #          tf.reduce_sum (self.w_ref1 * self.w_gen1 * self.w_gen2)
    # < --- >
    loss += gp_term
    return loss