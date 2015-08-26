# -*- coding: utf-8 -*-
## @package guided_filter.datasets.google_image
#
#  Image datasets via Google Image API.
#  createDatasets function will create datasets
#  with the following direcotry structure.
#
#  * datasets
#    - apple
#      - apple_1.jpg
#    - banana
#      - banana_1.jpg
#
#  @author      tody
#  @date        2015/08/15


import json
import os
import urllib2
import httplib2

import cv2
import matplotlib.pyplot as plt

from guided_filter.io_util.image import loadRGB, saveRGB

_root_dir = os.path.dirname(__file__)


## Data directory for the given data_name.
def dataDir(data_name):
    data_dir = os.path.join(_root_dir, data_name)
    return data_dir


## Data file path list for the given data_name.
def dataFiles(data_name):
    data_dir = dataDir(data_name)
    data_files = []
    for data_name in os.listdir(data_dir):
        data_file = os.path.join(data_dir, data_name)
        if ".png" in data_name or ".jpg" in data_name:
            data_files.append(data_file)
        else:
            os.remove(data_file)
    return data_files


## Data file path for the given data_name and data_id.
def dataFile(data_name, data_id):
    data_files = dataFiles(data_name)

    if data_id >= len(data_files):
        return None

    data_file = data_files[data_id]
    return data_file


def loadData(data_name, data_id):
    data_file = dataFile(data_name, data_id)

    if data_file is None:
        return None

    return loadRGB(data_file)


## Simple image loaders via Google image API.
class GoogleImageLoader:
    ## Constructor
    #  @param keyword     keyword for image search.
    #  @param num_images  target number of images for the search.
    #  @param update      Update existing images if the value is True.
    def __init__(self, keyword="banana", num_images=10, update=False):
        self._keyword = keyword
        self._num_images = num_images
        self._data_dir = dataDir(keyword)
        self._update = update

        self.searchImageURLs()
        self.downloadImages()
        self.postResize()

    def searchImageURLs(self):
        keyword = self._keyword
        num_images = self._num_images

        image_urls = []
        google_api = "http://ajax.googleapis.com/ajax/services/search/images?q={0}&v=1.0&rsz=large&start={1}&imgc=color"

        for i in range((num_images / 8) + 1):
            res = urllib2.urlopen(google_api.format(keyword, i * 8))
            page_data = json.load(res)
            page_urls = [result["url"] for result in page_data["responseData"]["results"]]
            image_urls.extend(page_urls)

        if len(image_urls) >= num_images:
            image_urls = image_urls[:num_images]
        self._image_urls = image_urls
        return image_urls

    def downloadImages(self):
        print "  Download"
        data_name = self._keyword
        image_urls = self._image_urls
        data_dir = self._data_dir
        if os.path.exists(data_dir) == False:
            os.makedirs(data_dir)

        http = httplib2.Http(".cache")

        for i in range(len(set(image_urls))):
            try:
                url_name, ext = os.path.splitext(image_urls[i])

                data_filename = "%s_%s%s" % (data_name, i, ext)
                data_filepath = os.path.join(data_dir, data_filename)

                if not self._update:
                    if os.path.exists(data_filepath):
                        print "  - Skip: %s" % data_filename
                        continue

                response, content = http.request(image_urls[i])

                with open(data_filepath, 'wb') as data_file:
                    data_file.write(content)

                    print "  - Done: %s" % data_filename
            except:
                continue

    def postResize(self):
        print "  Post resize"
        data_name = self._keyword
        data_files = dataFiles(data_name)

        for data_file in data_files:
            data_filename = os.path.basename(data_file)
            C_8U = loadRGB(data_file)

            if C_8U is None:
                os.remove(data_file)
                print "  - Delete: %s" % data_filename
                continue
            h, w = C_8U.shape[0:2]

            opt_scale = 800.0 / float(h)
            opt_scale = max(opt_scale, 800.0 / float(w))
            opt_scale = min(opt_scale, 1.0)

            h_opt = int(opt_scale * h)
            w_opt = int(opt_scale * w)

            C_8U_small = cv2.resize(C_8U, (w_opt, h_opt))
            saveRGB(data_file, C_8U_small)
            print "  - Resized: %s" % data_filename


## Create dataset for the given data_name.
def createDataset(data_name="banana", num_images=10, update=False):
    GoogleImageLoader(data_name, num_images, update)


## Create datasets for the given data_names.
def createDatasets(data_names=["apple", "banana", "sky", "tulip", "flower"],
                   num_images=10,
                   update=False):
    for data_name in data_names:
        print "Create datasets: %s" % data_name
        createDataset(data_name, num_images, update)


if __name__ == '__main__':
    createDatasets()
