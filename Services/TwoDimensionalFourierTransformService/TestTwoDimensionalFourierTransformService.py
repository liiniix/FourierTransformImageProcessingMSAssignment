from Services.ImageReadWriteService.PBMImageReadWriteService import PBMImageReadWriteService
import matplotlib.pyplot as plt
import numpy

from Services.TwoDimensionalFourierTransformService.TwoDimensionalFourierTransformService import \
    TwoDimensionalFourierTransformService

if __name__ == "__main__":
    pbm_image_read_write_service = PBMImageReadWriteService()
    pbm_image_numpy_ndarray = pbm_image_read_write_service.get_pgm_data_as_numpy_array(
        '../ImageReadWriteService/51_image_with_middle_white_square_block.pgm')


    def test_accurate_input_image_read():
        plt.imshow(pbm_image_numpy_ndarray, cmap='gray', vmin=0, vmax=255)
        plt.show()


    # test_accurate_input_image_read()

    two_dimensional_fourier_transform_service = TwoDimensionalFourierTransformService()


    def test_make_zero_pad_image():
        zero_padded_pbm_image_numpy_ndarray = two_dimensional_fourier_transform_service._make_zero_pad_image(
            pbm_image_numpy_ndarray)

        plt.imshow(zero_padded_pbm_image_numpy_ndarray, cmap='gray', vmin=0, vmax=255)
        plt.show()


    # test_make_zero_pad_image()

    def test_make_center_align_from_zero_pad_image():
        zero_padded_pbm_image_numpy_ndarray = two_dimensional_fourier_transform_service \
            ._make_zero_pad_image(pbm_image_numpy_ndarray)

        center_aligned_zero_padded_pgm_image_numpy_ndarray = two_dimensional_fourier_transform_service._make_center_align_from_zero_pad_image(
            zero_padded_pbm_image_numpy_ndarray)

        plt.imshow(center_aligned_zero_padded_pgm_image_numpy_ndarray, cmap='gray', vmin=0, vmax=255)
        plt.show()


    # test_make_center_align_from_zero_pad_image()

    def test_two_dimensional_discrete_fourier_transform():
        two_dimension_fourier_transform = two_dimensional_fourier_transform_service.two_dimensional_discrete_fourier_transform(
            pbm_image_numpy_ndarray)

        plt.imshow(two_dimension_fourier_transform.real, cmap='gray', vmin=0, vmax=255)
        plt.show()


    # test_two_dimensional_discrete_fourier_transform()

    def test_two_dimensional_reverse_discrete_fourier_transform():
        two_dimension_fourier_transform = two_dimensional_fourier_transform_service.two_dimensional_discrete_fourier_transform(
            pbm_image_numpy_ndarray)
        two_dimension_inverse_transform = two_dimensional_fourier_transform_service.two_dimensional_reverse_discrete_fourier_transform(
            two_dimension_fourier_transform)

        plt.imshow(two_dimension_inverse_transform.real, cmap='gray', vmin=0, vmax=255)
        plt.show()


    # test_two_dimensional_reverse_discrete_fourier_transform()

    def test_generate_low_pass_filter():
        low_pass_filter = two_dimensional_fourier_transform_service.generate_low_pass_filter((128, 128), 25)
        plt.imshow(low_pass_filter, cmap='gray')
        plt.show()


    # test_generate_low_pass_filter()

    def test_apply_filter_on_time_domain_image():
        original_image_shape = pbm_image_numpy_ndarray.shape

        high_pass_filter = two_dimensional_fourier_transform_service. \
            generate_high_pass_filter(
            original_image_shape, 17)

        low_pass_filter = two_dimensional_fourier_transform_service. \
            generate_low_pass_filter(
            original_image_shape, 17)

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

        f, axarr = plt.subplots(2)
        axarr[0].imshow(two_dimension_inverse_transform_high_passed.real, cmap='gray')
        axarr[1].imshow(two_dimension_inverse_transform_low_passed.real, cmap='gray')
        print(numpy.min(two_dimension_inverse_transform_high_passed.real),
              numpy.max(two_dimension_inverse_transform_high_passed.real),
              numpy.min(two_dimension_inverse_transform_low_passed.real),
              numpy.max(two_dimension_inverse_transform_low_passed.real)
              )
        plt.show()


        pbm_image_read_write_service.write_pgm_image_from_numpy_array('bogor_high.pgm', two_dimension_inverse_transform_high_passed.real)
        pbm_image_read_write_service.write_pgm_image_from_numpy_array('bogor_low.pgm', two_dimension_inverse_transform_low_passed.real)

    test_apply_filter_on_time_domain_image()
