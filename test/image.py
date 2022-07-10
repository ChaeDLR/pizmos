import os
import pygame


def load(func: callable):

    test_images = [pygame.Surface((32, 32)) for _ in range(9)]

    os.makedirs(os.path.join(os.getcwd(), "testdir_0/testdir_1/testdir_2"))

    head_dir = current_path = os.getcwd()

    for _test_dir in ["testdir_0", "testdir_1", "testdir_2"]:

        current_path = os.path.join(
            current_path, _test_dir
        )

        os.chdir(current_path)

        for i in range(3):
            pygame.image.save(
                test_images.pop(),
                os.path.join(current_path, f"test_image_{i}.bmp")
            )

        # test 1image saving and write delete

    _images = func(head_dir)
