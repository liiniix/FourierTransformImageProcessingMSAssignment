import netpbmfile
import numpy


class PBMImageReadWriteService:
    # region Ctor
    def __init__(self):
        pass

    # endregion

    # region Methods
    def get_pgm_data_as_numpy_array(self,
                                    file_location_and_name: str) -> numpy.ndarray:
        pgm_image_numpy_array: numpy.ndarray = netpbmfile.imread(file_location_and_name)

        return pgm_image_numpy_array



    def write_pgm_image_from_numpy_array(self,
                                         file_location_and_name:str,
                                         pgm_image_numpy_array:numpy.ndarray):

        preprocessed_pgm_image_numpy_array = self.make_numpy_from_certain_range_write_as_pbm(pgm_image_numpy_array, 255)
        netpbmfile.imwrite(file_location_and_name, preprocessed_pgm_image_numpy_array)

    def generate_pgm_image_with_square_white_block_in_the_middle(self,
                                                                 height_pixel_count: int,
                                                                 width_pixel_count: int,
                                                                 square_block_side_length: int,
                                                                 file_location_and_name) -> None:
        BLACKPIXEL: int = 0
        WHITEPIXEL: int = 255
        pgm_image_numpy_ndarray_with_square_white_block_in_the_middle = numpy.zeros((height_pixel_count, width_pixel_count), dtype=int)

        for height_sweeper in range(height_pixel_count):
             for width_sweeper in range(width_pixel_count):
                 is_height_sweeper_in_white_sqare_block: bool = (height_pixel_count / 2 - square_block_side_length) <= height_sweeper and \
                                                                height_sweeper <= (height_pixel_count / 2 + square_block_side_length)

                 is_width_sweeper_in_white_sqare_block: bool = (width_pixel_count / 2 - square_block_side_length) <= width_sweeper and \
                                                               width_sweeper <= (width_pixel_count / 2 + square_block_side_length)

                 pgm_image_numpy_ndarray_with_square_white_block_in_the_middle[height_sweeper][width_sweeper] =\
                     WHITEPIXEL if is_height_sweeper_in_white_sqare_block and is_width_sweeper_in_white_sqare_block \
                                else\
                     BLACKPIXEL

        netpbmfile.imwrite(file_location_and_name, pgm_image_numpy_ndarray_with_square_white_block_in_the_middle)

    def make_numpy_from_certain_range_write_as_pbm(self,
                                                   pgm_image_numpy_array: numpy.ndarray,
                                                   upper_limit: int) -> numpy.ndarray:
        max_value = numpy.max(pgm_image_numpy_array)
        min_value = numpy.min(pgm_image_numpy_array)

        val = ((pgm_image_numpy_array - min_value) * upper_limit / (max_value - min_value)).astype(int)

        return val

    # endregion
