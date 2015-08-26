from guided_filter.datasets.google_image import dataFile

# -*- coding: utf-8 -*-
## @package guided_filter.results.performance
#
#  Simple performance test.
#  @author      tody
#  @date        2015/08/26

def performanceTest(image_file):
    image_name = os.path.basename(image_file)
    image_name = os.path.splitext(image_name)[0]

    C_8U = loadRGB(image_file)
    C_32F = to32F(C_8U)

    aspect = C_32F.shape[0] / float(C_32F.shape[1])

    fig_width = 10
    fig_height = int(fig_width * aspect / 3) + 1
    fig = plt.figure(figsize=(fig_width, fig_height))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.02, hspace=0.05)

    plt.subplot(131)
    plt.title("%s" % (image_name))
    plt.imshow(C_32F)
    plt.axis('off')

    h, w, cs = C_32F.shape

    C_noise = np.float32(C_32F + 0.3 * np.random.rand(h, w, cs))
    C_noise = np.clip(C_noise, 0.0, 1.0)

    plt.subplot(132)
    plt.title("Noise Image")
    plt.imshow(C_noise)
    plt.axis('off')

    guided_filter = FastGuidedFilter(C_32F, sigma_space=10, sigma_range=0.05, scale=4)
    C_smooth = guided_filter.filter(C_noise)
    C_smooth = np.clip(C_smooth, 0.0, 1.0)

    plt.subplot(133)
    plt.title("Filtered Image")
    plt.imshow(C_smooth)
    plt.axis('off')

    result_file = resultFile(image_name)
    plt.savefig(result_file)


def performanceTests(data_names, data_ids):
    for data_name in data_names:
        print "Performance tests: %s" % data_name
        for data_id in data_ids:
            print "Data ID: %s" % data_id
            image_file = dataFile(data_name, data_id)
            performanceTest(image_file)

if __name__ == '__main__':
    data_names = ["apple", "flower", "tulip"]
    data_ids = [0, 1, 2]

    performanceTests(data_names, data_ids)