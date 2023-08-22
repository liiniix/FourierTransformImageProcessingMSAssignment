from Services.ImageReadWriteService.PBMImageReadWriteService import PBMImageReadWriteService

if __name__ == "__main__":
    pbm_image_read_write_service = PBMImageReadWriteService()

    pbm_image_read_write_service.\
        generate_pgm_image_with_square_white_block_in_the_middle(128, 128, 10, "128_image_with_middle_white_square_block.pgm")
    pbm_image_read_write_service.\
        generate_pgm_image_with_square_white_block_in_the_middle(86, 86, 7, "86_image_with_middle_white_square_block.pgm")
    pbm_image_read_write_service.\
        generate_pgm_image_with_square_white_block_in_the_middle(51, 51, 4, "51_image_with_middle_white_square_block.pgm")