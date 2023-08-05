from typing import Tuple

import numpy as np
from scipy.ndimage import distance_transform_edt as distance

from .._shared.utils import _supported_float_type


def _cv_curvature(phi):
    """Returns the 'curvature' of a level set 'phi'.
    """
    P = np.pad(phi, 1, mode='edge')
    fy = (P[2:, 1:-1] - P[:-2, 1:-1]) / 2.0
    fx = (P[1:-1, 2:] - P[1:-1, :-2]) / 2.0
    fyy = P[2:, 1:-1] + P[:-2, 1:-1] - 2*phi
    fxx = P[1:-1, 2:] + P[1:-1, :-2] - 2*phi
    fxy = .25 * (P[2:, 2:] + P[:-2, :-2] - P[:-2, 2:] - P[2:, :-2])
    grad2 = fx**2 + fy**2
    K = ((fxx*fy**2 - 2*fxy*fx*fy + fyy*fx**2) /
         (grad2*np.sqrt(grad2) + 1e-8))
    return K


def _cv_calculate_variation(
    img: np.array, phi: np.array, mu: float, nu: float, lambda1: float, lambda2: float, dt: float
) -> np.array:
    """Solve the level set values at t+1.

    Parameters
    ----------
    img : np.array
        The image to segment.
    phi : np.array
        The level set.
    mu : float
        Segmentation curve length penalty.
    nu : float
        Segmentation area length penalty.
    lambda1 : float
        Penalty of the inside class intravariance.
    lambda2 : float
        Penalty of the outside class intravariance.
    dt : float
        Time step used for the pde resolution.

    Returns
    -------
    np.array
        The level set values at t+1.
    """
    eta = 1e-16
    padded = np.pad(phi, 1, mode='edge')
    grad_x_p = padded[1:-1, 2:] - padded[1:-1, 1:-1]
    grad_x_n = padded[1:-1, 1:-1] - padded[1:-1, :-2]
    grad_x_0 = (padded[1:-1, 2:] - padded[1:-1, :-2]) / 2.0

    grad_y_p = padded[2:, 1:-1] - padded[1:-1, 1:-1]
    grad_y_n = padded[1:-1, 1:-1] - padded[:-2, 1:-1]
    grad_y_0 = (padded[2:, 1:-1] - padded[:-2, 1:-1]) / 2.0

    div_1 = 1. / np.sqrt(eta + grad_x_p ** 2 + grad_y_0 ** 2)
    div_2 = 1. / np.sqrt(eta + grad_x_n ** 2 + grad_y_0 ** 2)
    div_3 = 1. / np.sqrt(eta + grad_x_0 ** 2 + grad_y_p ** 2)
    div_4 = 1. / np.sqrt(eta + grad_x_0 ** 2 + grad_y_n ** 2)

    mu_term = (padded[1:-1, 2:] * div_1 + padded[1:-1, :-2] * div_2 +
               padded[2:, 1:-1] * div_3 + padded[:-2, 1:-1] * div_4)

    c1, c2 = _cv_calculate_averages(img, phi)

    dist_c1 = img - c1
    dist_c1 *= dist_c1
    dist_c1 = lambda1 * np.sum(dist_c1, axis=len(img.shape) - 1)
    dist_c2 = img - c2
    dist_c2 *= dist_c2
    dist_c2 = lambda2 * np.sum(dist_c2, axis=len(img.shape) - 1)

    delta_phi = dt * _cv_delta(phi)
    new_phi = phi + delta_phi * (mu * mu_term - nu - dist_c1 + dist_c2)

    return new_phi / (1 + mu * delta_phi * (div_1 + div_2 + div_3 + div_4))


def _cv_heavyside(x, eps=1.):
    """Returns the result of a regularised heavyside function of the
    input value(s).
    """
    return 0.5 * (1. + (2./np.pi) * np.arctan(x/eps))


def _cv_delta(x: np.array, eps: float = 1.) -> np.array:
    """Compute a regularized Dirac function of x.

    Parameters
    ----------
    x : np.array
        Input aray.
    eps : float, optional
        Input aray, by default 1.

    Returns
    -------
    np.array
        The application of a regularized dirac function on x.
    """
    return eps / (eps**2 + x**2)


def _cv_calculate_averages(img: np.array, phi: np.array) -> Tuple[np.array, np.array]:
    """Compute average of the two segmentation classes.

    Parameters
    ----------
    img : np.array
        The image.
    phi : np.array
        The level set.
    Returns
    -------
    Tuple[np.array, np.array]
        The first value is the average inside the level set and the second is the one outside.
    """
    avg_c1 = np.zeros((img.shape[-1]), dtype=img.dtype)
    avg_c2 = np.zeros((img.shape[-1]), dtype=img.dtype)
    idx = phi > 0
    count_c1 = np.count_nonzero(idx)
    count_c2 = idx.size - count_c1

    if count_c1 > 0:
            avg_c1 = np.sum(img[idx], axis=0)
            avg_c1 /= count_c1
    if count_c2 > 0:
        avg_c2 = np.sum(img[np.logical_not(idx)], axis=0)
        avg_c2 /= count_c2

    return avg_c1, avg_c2


def _cv_difference_from_average_term(image, Hphi, lambda_pos, lambda_neg):
    """Returns the 'energy' contribution due to the difference from
    the average value within a region at each point.
    """
    (c1, c2) = _cv_calculate_averages(image, Hphi)
    Hinv = 1. - Hphi
    return (lambda_pos * (image-c1)**2 * Hphi +
            lambda_neg * (image-c2)**2 * Hinv)


def _cv_edge_length_term(phi, mu):
    """Returns the 'energy' contribution due to the length of the
    edge between regions at each point, multiplied by a factor 'mu'.
    """
    toret = _cv_curvature(phi)
    return mu * toret


def _cv_energy(image, phi, mu, lambda1, lambda2):
    """Returns the total 'energy' of the current level set function.
    """
    H = _cv_heavyside(phi)
    avgenergy = _cv_difference_from_average_term(image, H, lambda1, lambda2)
    lenenergy = _cv_edge_length_term(phi, mu)
    return np.sum(avgenergy) + np.sum(lenenergy)


def _cv_reset_level_set(phi):
    """This is a placeholder function as resetting the level set is not
    strictly necessary, and has not been done for this implementation.
    """
    return phi


def _cv_checkerboard(image_size, square_size, dtype=np.float64):
    """Generates a checkerboard level set function.

    According to Pascal Getreuer, such a level set function has fast
    convergence.
    """
    yv = np.arange(image_size[0], dtype=dtype).reshape(image_size[0], 1)
    xv = np.arange(image_size[1], dtype=dtype)
    sf = np.pi / square_size
    xv *= sf
    yv *= sf
    return np.sin(yv) * np.sin(xv)


def _cv_large_disk(image_size):
    """Generates a disk level set function.

    The disk covers the whole image along its smallest dimension.
    """
    res = np.ones(image_size)
    centerY = int((image_size[0]-1) / 2)
    centerX = int((image_size[1]-1) / 2)
    res[centerY, centerX] = 0.
    radius = float(min(centerX, centerY))
    return (radius - distance(res)) / radius


def _cv_small_disk(image_size):
    """Generates a disk level set function.

    The disk covers half of the image along its smallest dimension.
    """
    res = np.ones(image_size)
    centerY = int((image_size[0]-1) / 2)
    centerX = int((image_size[1]-1) / 2)
    res[centerY, centerX] = 0.
    radius = float(min(centerX, centerY)) / 2.0
    return (radius - distance(res)) / (radius * 3)


def _cv_init_level_set(init_level_set, image_shape, square_size=5, dtype=np.float64):
    """Generates an initial level set function conditional on input arguments.

    'square_size' is only used if 'init_level_set' is set to 'checkerboard'
    """
    if type(init_level_set) == str:
        if init_level_set == 'checkerboard':
            res = _cv_checkerboard(image_shape, square_size, dtype)
        elif init_level_set == 'disk':
            res = _cv_large_disk(image_shape)
        elif init_level_set == 'small disk':
            res = _cv_small_disk(image_shape)
        else:
            raise ValueError("Incorrect name for starting level set preset.")
    else:
        res = init_level_set
    return res.astype(dtype, copy=False)


def chan_vese(image, mu=0.25, nu=0., lambda1=1.0, lambda2=1.0, tol=1e-3,
              max_num_iter=500, dt=0.5, init_level_set='checkerboard',
              extended_output=False):
    """Chan-Vese segmentation algorithm.

    Active contour model by evolving a level set. Can be used to
    segment objects without clearly defined boundaries.

    Parameters
    ----------
    image : (M, N) or (M, N, K) ndarray
        Image to be segmented.
    mu : float, optional
        'edge length' weight parameter. Higher `mu` values will
        produce a 'round' edge, while values closer to zero will
        detect smaller objects.
    nu: float, optional
        Segmentation area length penalty. A positive value favors
        a small segmentated area while a negative one encourages a big segmented area.
    lambda1 : float, optional
        'difference from average' weight parameter for the output
        region with value 'True'. If it is lower than `lambda2`, this
        region will have a larger range of values than the other.
    lambda2 : float, optional
        'difference from average' weight parameter for the output
        region with value 'False'. If it is lower than `lambda1`, this
        region will have a larger range of values than the other.
    tol : float, positive, optional
        Level set variation tolerance between iterations. If the
        L2 norm difference between the level sets of successive
        iterations normalized by the area of the image is below this
        value, the algorithm will assume that the solution was
        reached.
    max_num_iter : uint, optional
        Maximum number of iterations allowed before the algorithm
        interrupts itself.
    dt : float, optional
        A multiplication factor applied at calculations for each step,
        serves to accelerate the algorithm. While higher values may
        speed up the algorithm, they may also lead to convergence
        problems.
    init_level_set : str or (M, N) ndarray, optional
        Defines the starting level set used by the algorithm.
        If a string is inputted, a level set that matches the image
        size will automatically be generated. Alternatively, it is
        possible to define a custom level set, which should be an
        array of float values, with the same shape as 'image'.
        Accepted string values are as follows.

        'checkerboard'
            the starting level set is defined as
            sin(x/5*pi)*sin(y/5*pi), where x and y are pixel
            coordinates. This level set has fast convergence, but may
            fail to detect implicit edges.
        'disk'
            the starting level set is defined as the opposite
            of the distance from the center of the image minus half of
            the minimum value between image width and image height.
            This is somewhat slower, but is more likely to properly
            detect implicit edges.
        'small disk'
            the starting level set is defined as the
            opposite of the distance from the center of the image
            minus a quarter of the minimum value between image width
            and image height.
    extended_output : bool, optional
        If set to True, the return value will be a tuple containing
        the three return values (see below). If set to False which
        is the default value, only the 'segmentation' array will be
        returned.

    Returns
    -------
    segmentation : (M, N) ndarray, bool
        Segmentation produced by the algorithm.
    phi : (M, N) ndarray of floats
        Final level set computed by the algorithm.
    energies : list of floats
        Shows the evolution of the 'energy' for each step of the
        algorithm. This should allow to check whether the algorithm
        converged.

    Notes
    -----
    The Chan-Vese Algorithm is designed to segment objects without
    clearly defined boundaries. This algorithm is based on level sets
    that are evolved iteratively to minimize an energy, which is
    defined by weighted values corresponding to the sum of differences
    intensity from the average value outside the segmented region, the
    sum of differences from the average value inside the segmented
    region, and a term which is dependent on the length of the
    boundary of the segmented region.

    This algorithm was first proposed by Tony Chan and Luminita Vese,
    in a publication entitled "An Active Contour Model Without Edges"
    [1]_.

    Typical values for `lambda1` and `lambda2` are 1. If the
    'background' is very different from the segmented object in terms
    of distribution (for example, a uniform black image with figures
    of varying intensity), then these values should be different from
    each other.

    Typical values for mu are between 0 and 1, though higher values
    can be used when dealing with shapes with very ill-defined
    contours.

    The 'energy' which this algorithm tries to minimize is defined
    as the sum of the differences from the average within the region
    squared and weighed by the 'lambda' factors to which is added the
    length of the contour multiplied by the 'mu' factor.

    Supports 2D grayscale and vector-valued images.

    References
    ----------
    .. [1] An Active Contour Model without Edges, Tony Chan and
           Luminita Vese, Scale-Space Theories in Computer Vision,
           1999, :DOI:`10.1007/3-540-48236-9_13`
    .. [2] Chan-Vese Segmentation, Pascal Getreuer Image Processing On
           Line, 2 (2012), pp. 214-224,
           :DOI:`10.5201/ipol.2012.g-cv`
    .. [3] The Chan-Vese Algorithm - Project Report, Rami Cohen, 2011
           :arXiv:`1107.2782`
    """
    if len(image.shape) == 2:
        image = image[..., np.newaxis]

    float_dtype = _supported_float_type(image.dtype)
    phi = _cv_init_level_set(init_level_set, image.shape[:-1], dtype=float_dtype)

    if type(phi) != np.ndarray or phi.shape != image.shape[:-1]:
        raise ValueError("The dimensions of initial level set do not "
                         "match the dimensions of image.")

    image = image.astype(float_dtype, copy=False)
    image = image - np.min(image.reshape(image.shape[0] * image.shape[1], image.shape[2]), axis=0)
    max_val = np.max(image.reshape(image.shape[0] * image.shape[1], image.shape[2]), axis=0)
    max_val[max_val == 0] = 1.
    image = image / max_val

    i = 0
    old_energy = _cv_energy(image, phi, mu, lambda1, lambda2)
    energies = []
    phi_var = tol + 1
    segmentation = phi > 0

    while phi_var > tol and i < max_num_iter:
        # Save old level set values
        old_phi = phi

        # Calculate new level set
        phi = _cv_calculate_variation(image, phi, mu, nu, lambda1, lambda2, dt)
        phi = _cv_reset_level_set(phi)
        phi_var = np.linalg.norm(phi - old_phi)

        # Extract energy and compare to previous level set and
        # segmentation to see if continuing is necessary
        segmentation = phi > 0
        new_energy = _cv_energy(image, phi, mu, lambda1, lambda2)

        # Save old energy values
        energies.append(old_energy)
        old_energy = new_energy
        i += 1

    if extended_output:
        return segmentation, phi, energies
    else:
        return segmentation
