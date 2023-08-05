import os
import warnings
from typing import Any

import cv2
import numpy as np
import numpy.typing as npt
import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/67.0.3396.99 Safari/537.36"
    )
}


class NeedPurchase(Warning):
    pass


class GetJump:
    def __init__(self) -> None:
        pass

    def get(
        self, url: str, save_path: str = ".", overwrite: bool = True
    ) -> tuple[str, str]:
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            raise ConnectionError(r.status_code)
        j = r.json()["readableProduct"]
        next = j["nextReadableProductUri"]
        next = next + ".json" if type(next) is str else next
        series_title = j["series"]["title"]
        title = j["title"]

        save_dir = os.path.join(save_path, series_title, title)
        if os.path.exists(save_dir) and not overwrite:
            return next, save_dir
        os.makedirs(save_dir, exist_ok=True)

        if not j["isPublic"] and not j["hasPurchased"]:
            warnings.warn(title, NeedPurchase, stacklevel=1)
            return next, save_dir
        else:
            pages = j["pageStructure"]["pages"]

        self.__save_images(pages, save_dir)

        return next, save_dir

    def __save_images(self, pages: list[Any], save_dir: str) -> None:
        imgs = []
        for page in pages:
            if "src" not in page:
                continue
            img = self.__get_image(page)
            imgs.append(img)

        len_page_digit = len(str(len(imgs)))
        for idx, img in enumerate(imgs):
            save_img_path = os.path.join(
                save_dir, f"%0{len_page_digit}d" % idx + ".jpg"
            )
            cv2.imwrite(save_img_path, img)

    def __get_image(self, image_dic: dict[str, Any]) -> npt.ArrayLike:
        src = image_dic["src"]
        img = requests.get(src, stream=True).raw
        img = np.asarray(bytearray(img.read()), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        offset = 4
        height, width = img.shape[:2]
        dice_height = int((height - self.__get_height_gap(height)) / offset)
        dice_width = int((width - self.__get_width_gap(width)) / offset)
        pieces = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for x in range(offset):
            for y in range(offset):
                x_slice = slice(x * dice_height, (x + 1) * dice_height)
                y_slice = slice(y * dice_width, (y + 1) * dice_width)

                piece = img[x_slice, y_slice]
                pieces[y][x] = piece

        img = cv2.vconcat([cv2.hconcat(x) for x in pieces])
        return img

    @staticmethod
    def __get_height_gap(height: int) -> int:
        if height == 1200:
            return 16
        elif height == 1600:
            return 0
        elif height == 1024:
            return 0
        else:
            raise ValueError(
                "Unfamiliar height (please let me know with issue <https://git.io/J2jV3>): %d"
                % height
            )

    @staticmethod
    def __get_width_gap(width: int) -> int:
        if width == 760:
            return 24
        elif width == 764:
            return 25
        elif width == 822:
            return 22
        elif width == 1114:
            return 23
        elif width == 720:
            return 15
        elif width == 704:
            return 0
        elif width == 1125:
            return 2
        else:
            raise ValueError(
                "Unfamiliar width (please let me know with issue <https://git.io/J2jV3>): %d"
                % width
            )


def main() -> None:
    g = GetJump()
    next_uri = "https://shonenjumpplus.com/episode/13932016480028799982.json"
    while next_uri:
        next_uri, prev_title = g.get(next_uri, overwrite=False)
        print("saved:", prev_title)
        print("next:", next_uri)


if __name__ == "__main__":
    main()
