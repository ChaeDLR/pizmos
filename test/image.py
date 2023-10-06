import os
import pygame


def load_all(func: callable):
    """Test the load_all function by generating 3 nested directorys
    and adding 3 bitmap files in each. Directories get deleted once
    they're finished being used by the load_all function. Asserts that
    every file loaded is a pygame.Surface and every key is a string.

    Args:
        func (callable): src.image.load_all
    """

    # creates pygame surfaces that will be saved as bitmaps to each test directory
    test_images = [pygame.Surface((32, 32)) for _ in range(9)]
    dir_names = ["testdir_0", "testdir_1", "testdir_2"]
    os.makedirs(os.path.join(os.getcwd(), "testdir_0/testdir_1/testdir_2"))

    head_dir = current_path = os.getcwd()

    # region populate test dirs

    inum = 0  # image number

    for _test_dir in dir_names:
        current_path = os.path.join(current_path, _test_dir)

        os.chdir(current_path)

        for _ in range(3):
            pygame.image.save(
                test_images.pop(), os.path.join(current_path, f"test_image_{inum}.bmp")
            )
            inum += 1

    # endregion

    # run the load_all function
    _images = func(os.path.join(head_dir, dir_names[0]))

    # region delete the test dirs

    while current_path != head_dir:
        for _file in os.listdir(current_path):
            if os.path.isfile(_file):
                os.remove(_file)
            else:
                os.rmdir(f"./{_file}")

        os.chdir("..")
        current_path = os.getcwd()

    os.rmdir(dir_names[0])

    # endregion

    # assert keys are strings and values are pygame surfaces
    for k in _images:
        assert isinstance(k, str)
        assert isinstance(_images[k], pygame.Surface)
