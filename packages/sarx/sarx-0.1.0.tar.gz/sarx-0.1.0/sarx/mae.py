from jax.numpy import mean, abs, where, zeros_like, ones_like
from jax import custom_jvp


@custom_jvp
def mae(e):
    return mean(abs(e))

@mae.defjvp
def maejvp(primals, tangents):
    x, = primals
    dy, = tangents
    zero = zeros_like(x)
    one = ones_like(x)
    return mae(x), where(x > 0, one, where(x < 0, -one, zero)) * dy
