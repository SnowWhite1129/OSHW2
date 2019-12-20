import numpy as np


class Image:
    def __init__(self, img, cvNet):
        self.img = img
        self.cvNet = cvNet

    def detect(self):
        #im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
        #to_draw = im.copy()
        pixel_means = [0.406, 0.456, 0.485]
        pixel_stds = [0.225, 0.224, 0.229]
        pixel_scale = 255.0
        #rows, cols, c = im.shape
        im_tensor = np.zeros((1, 3, self.img.shape[0], self.img.shape[1]))
        im = self.img.astype(np.float32)
        for i in range(3):
            im_tensor[0, i, :, :] = (im[:, :, 2 - i] / pixel_scale - pixel_means[2 - i]) / pixel_stds[2-i]
        self.cvNet.setInput(im_tensor)
        print(im_tensor.shape)
        import time
        cvOut = self.cvNet.forward()
        for _ in range(1):
            t0 = time.time()
            cvOut = self.cvNet.forward()
            print(time.time() - t0)
        for detection in cvOut[0, 0, :, :]:
            score = float(detection[2])
            if score > 0.6:
                return True
                '''
                left =int( detection[3] * cols)
                top =int( detection[4] * rows)
                right = int(detection[5] * cols)
                bottom = int(detection[6] * rows)
                cropped = to_draw[top:bottom, left:right]   
                '''
        return False

