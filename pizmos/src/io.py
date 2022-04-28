import pygame
import os

from sys import exc_info

def load(path: str) -> dict:
        """
        Recursive function that returns a directory
        with all the images in the path arg directory
        """
        def __load(imgs_dict: dict, prev_key: str=None) -> dict:
            if prev_key:
                imgs_dict[prev_key] = {}
            _imgs: list = []
            try:
                img: pygame.Surface = None
                str_parts: list[str] = None
                for file in os.listdir(path):
                    if file[len(file) - 4 :] == ".png":
                        img = pygame.image.load(os.path.join(path, file)).convert_alpha()
                        img.set_colorkey(img.get_at((0,0)))

                        if file[:-4].isdigit():
                            _imgs.append(img)
                        else:
                            # single .pngs with their key in the title
                            str_parts = file[:-4].split("_")
                            imgs_dict[str_parts[0]] = img

                    else:
                        if prev_key:
                            load(
                                os.path.abspath(os.path.join(path, file)),
                                imgs_dict[prev_key],
                                file,
                            )
                        else:
                            load(
                                os.path.abspath(os.path.join(path, file)),
                                imgs_dict,
                                file,
                            )
            except NotADirectoryError as ex:
                print(f"{ex.filename} not an accepted file type.")
                raise ex.with_traceback(exc_info())

            if len(_imgs) > 0:
                imgs_dict[prev_key] = _imgs
            return imgs_dict
        return __load({})
