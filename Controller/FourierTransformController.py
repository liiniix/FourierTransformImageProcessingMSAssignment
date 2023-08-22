import numpy
import matplotlib.pyplot as plt
from Services.ImageReadWriteService.PBMImageReadWriteService import PBMImageReadWriteService
from Services.TwoDimensionalFourierTransformService.TwoDimensionalFourierTransformService import \
    TwoDimensionalFourierTransformService

if __name__ == "__main__":
    pbm_image_read_write_service = PBMImageReadWriteService()
    two_dimensional_fourier_transform_service = TwoDimensionalFourierTransformService()

    square_image_side_length = 51
    white_square_side_length = int(square_image_side_length*20/100)
    filter_radius = white_square_side_length

    pbm_image_read_write_service.generate_pgm_image_with_square_white_block_in_the_middle(square_image_side_length,
                                                                                          square_image_side_length,
                                                                                          white_square_side_length,
                                                                                          f'{square_image_side_length}_white_sqaure_in_the_middle.pgm')

    pbm_image_numpy_ndarray = pbm_image_read_write_service.get_pgm_data_as_numpy_array(
        f'{square_image_side_length}_white_sqaure_in_the_middle.pgm')

    original_image_shape = numpy.shape(pbm_image_numpy_ndarray)

    high_pass_filter = two_dimensional_fourier_transform_service. \
        generate_high_pass_filter(
        original_image_shape, filter_radius)

    low_pass_filter = two_dimensional_fourier_transform_service. \
        generate_low_pass_filter(
        original_image_shape, filter_radius)

    two_dimension_fourier_transform = two_dimensional_fourier_transform_service. \
        two_dimensional_discrete_fourier_transform(
        pbm_image_numpy_ndarray)

    high_passed_filtered_image_on_time_domain = two_dimensional_fourier_transform_service. \
        apply_filter_on_time_domain_image(
        two_dimension_fourier_transform, high_pass_filter)

    low_passed_filtered_image_on_time_domain = two_dimensional_fourier_transform_service. \
        apply_filter_on_time_domain_image(
        two_dimension_fourier_transform, low_pass_filter)

    two_dimension_inverse_transform_high_passed = two_dimensional_fourier_transform_service. \
        two_dimensional_reverse_discrete_fourier_transform(
        high_passed_filtered_image_on_time_domain)

    two_dimension_inverse_transform_low_passed = two_dimensional_fourier_transform_service. \
        two_dimensional_reverse_discrete_fourier_transform(
        low_passed_filtered_image_on_time_domain)

    two_dimensional_inverse_transform_unfiltered = two_dimensional_fourier_transform_service. \
        two_dimensional_reverse_discrete_fourier_transform(
        two_dimension_fourier_transform)

    pbm_image_read_write_service.write_pgm_image_from_numpy_array(f'Controller/pbm/{square_image_side_length}_unfiltered_reversed_image.pbm', two_dimensional_inverse_transform_unfiltered.real)
    pbm_image_read_write_service.write_pgm_image_from_numpy_array(f'Controller/pbm/{square_image_side_length}_low_passed_reversed_image.pbm', two_dimension_inverse_transform_low_passed.real)
    pbm_image_read_write_service.write_pgm_image_from_numpy_array(f'Controller/pbm/{square_image_side_length}_high_passed_reversed_image.pbm', two_dimension_inverse_transform_high_passed.real)

    plt.imshow(pbm_image_numpy_ndarray, cmap='gray')
    plt.savefig('Controller/png/original_img.png')
    plt.clf()

    plt.imshow(two_dimension_inverse_transform_high_passed.real, cmap='gray')
    plt.savefig(f'Controller/png/{square_image_side_length}_high_passed_reversed_image.png')
    plt.clf()

    plt.imshow(two_dimension_inverse_transform_low_passed.real, cmap='gray')
    plt.savefig(f'Controller/png/{square_image_side_length}_low_passed_reversed_image.png')
    plt.clf()

    plt.imshow(two_dimensional_inverse_transform_unfiltered.real, cmap='gray')
    plt.savefig(f'Controller/png/{square_image_side_length}_unfiltered_reversed_image.png')
    plt.clf()



