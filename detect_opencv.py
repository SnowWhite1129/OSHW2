import numpy as np


class Image:
    def __init__(self, img, cvNet):
        self.img = img
        self.cvNet = cvNet

    def detect(self):
        pixel_means = [0.406, 0.456, 0.485]
        pixel_stds = [0.225, 0.224, 0.229]
        pixel_scale = 255.0
        im_tensor = np.zeros((1, 3, self.img.shape[0], self.img.shape[1]))
        im = self.img.astype(np.float32)
        for i in range(3):
            im_tensor[0, i, :, :] = (im[:, :, 2 - i] / pixel_scale - pixel_means[2 - i]) / pixel_stds[2-i]
        self.cvNet.setInput(im_tensor)
        cvOut = self.cvNet.forward()
        for _ in range(1):
            cvOut = self.cvNet.forward()
        for detection in cvOut[0, 0, :, :]:
            score = float(detection[2])
            if score > 0.8:
                return False
        return True
