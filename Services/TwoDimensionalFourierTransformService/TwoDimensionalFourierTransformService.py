import cmath, numpy
from tqdm import tqdm
from typing import Tuple

class TwoDimensionalFourierTransformService:

    def _make_zero_pad_image(self, pgm_image_numpy_ndarray) -> numpy.ndarray:
        original_image_dimension = numpy.shape(pgm_image_numpy_ndarray)

        padded_image_dimension = (2 * original_image_dimension[0] - 1, 2 * original_image_dimension[1] - 1)

        padded_pgm_image_numpy_ndarray = numpy.zeros(padded_image_dimension)

        padded_pgm_image_numpy_ndarray[:original_image_dimension[0],
                                       :original_image_dimension[1]] = pgm_image_numpy_ndarray

        return padded_pgm_image_numpy_ndarray

    def _make_center_align_from_zero_pad_image(self,
                                               zero_padded_pgm_image_numpy_ndarray: numpy.ndarray) -> numpy.ndarray:

        zero_padded_pgm_image_numpy_ndarray_dimension = numpy.shape(zero_padded_pgm_image_numpy_ndarray)
        center_aligned_zero_padded_pgm_image_numpy_ndarray = numpy.zeros(zero_padded_pgm_image_numpy_ndarray_dimension)

        for x in range(zero_padded_pgm_image_numpy_ndarray_dimension[0]):
            for y in range(zero_padded_pgm_image_numpy_ndarray_dimension[1]):
                center_aligned_zero_padded_pgm_image_numpy_ndarray[x, y] = zero_padded_pgm_image_numpy_ndarray[x, y] * numpy.power(-1, x + y)

        return center_aligned_zero_padded_pgm_image_numpy_ndarray

    def two_dimensional_discrete_fourier_transform(self, pgm_image_numpy_ndarray: numpy.ndarray) -> numpy.ndarray:

        pgm_image_numpy_ndarray_shape = numpy.shape(pgm_image_numpy_ndarray)
        M, N = pgm_image_numpy_ndarray_shape

        forward_transformed_image = numpy.zeros((pgm_image_numpy_ndarray_shape[0], pgm_image_numpy_ndarray_shape[1]), dtype=complex)

        for u in tqdm(range(*self.get_shifted_range(pgm_image_numpy_ndarray_shape[0])), ascii=True, desc="Ongoing forward fourier transform"):
            for v in range(*self.get_shifted_range(pgm_image_numpy_ndarray_shape[1])):
                for x in range(*self.get_shifted_range(pgm_image_numpy_ndarray_shape[0])):
                    for y in range(*self.get_shifted_range(pgm_image_numpy_ndarray_shape[1])):
                        unshifted_u = self.get_unshifted_index(u, pgm_image_numpy_ndarray_shape[0])
                        unshifted_v = self.get_unshifted_index(v, pgm_image_numpy_ndarray_shape[1])
                        unshifted_x = self.get_unshifted_index(x, pgm_image_numpy_ndarray_shape[0])
                        unshifted_y = self.get_unshifted_index(y, pgm_image_numpy_ndarray_shape[1])
                        forward_transformed_image[unshifted_u, unshifted_v] += pgm_image_numpy_ndarray[unshifted_x, unshifted_y] * \
                                                                               cmath.exp(- 2j * numpy.pi * (float(u * x) / M + float(v * y) / N))

        return forward_transformed_image

    def two_dimensional_reverse_discrete_fourier_transform(self, forward_transformed_image: numpy.ndarray) -> numpy.ndarray:

        pgm_image_numpy_ndarray_shape = numpy.shape(forward_transformed_image)
        M, N = pgm_image_numpy_ndarray_shape

        inverse_transform_image = numpy.zeros((pgm_image_numpy_ndarray_shape[0], pgm_image_numpy_ndarray_shape[1]), dtype=complex)

        for x in tqdm(range(*self.get_shifted_range(pgm_image_numpy_ndarray_shape[0])), ascii=True, desc="Ongoing reverse fourier transform"):
            for y in range(*self.get_shifted_range(pgm_image_numpy_ndarray_shape[1])):
                for u in range(*self.get_shifted_range(pgm_image_numpy_ndarray_shape[0])):
                    for v in range(*self.get_shifted_range(pgm_image_numpy_ndarray_shape[1])):
                        unshifted_u = self.get_unshifted_index(u, pgm_image_numpy_ndarray_shape[0])
                        unshifted_v = self.get_unshifted_index(v, pgm_image_numpy_ndarray_shape[1])
                        unshifted_x = self.get_unshifted_index(x, pgm_image_numpy_ndarray_shape[0])
                        unshifted_y = self.get_unshifted_index(y, pgm_image_numpy_ndarray_shape[1])
                        inverse_transform_image[unshifted_x, unshifted_y] += forward_transformed_image[unshifted_u, unshifted_v] * \
                                                                             cmath.exp(2j * numpy.pi * (float(u * x) / M + float(v * y) / N))

        inverse_transform_image = inverse_transform_image/(M*N)

        return inverse_transform_image

    def apply_filter_on_time_domain_image(self,
                                          forward_transformed_image: numpy.ndarray,
                                          filter: numpy.ndarray) -> numpy.ndarray:

        filtered_time_domain_image = numpy.multiply(forward_transformed_image, filter)

        return filtered_time_domain_image

    def generate_low_pass_filter(self,
                                 shape: Tuple[int, int],
                                 radius: float) -> numpy.ndarray:
        low_pass_filter = numpy.zeros(shape)

        center = (shape[0]/2, shape[1]/2)
        for x in range(shape[0]):
            for y in range(shape[1]):
                low_pass_filter[x, y] = 1. if (x-center[0])**2 + (y-center[1])**2 <= radius**2 else 0.

        return low_pass_filter

    def generate_high_pass_filter(self,
                                 shape: Tuple[int, int],
                                 radius: float) -> numpy.ndarray:
        high_pass_filter = numpy.zeros(shape)

        center = (shape[0]/2, shape[1]/2)
        for x in range(shape[0]):
            for y in range(shape[1]):
                high_pass_filter[x, y] = 0. if (x-center[0])**2 + (y-center[1])**2 <= radius**2 else 1.0

        return high_pass_filter

    def get_shifted_range(self, length: int) -> Tuple[int, int]:
        half_length = int( (length-1)/2 )
        return ( -half_length, half_length )

    def get_unshifted_index(self, index: int, length: int) -> Tuple[int, int]:
        half_length = int( (length-1)/2 )
        return index + half_length