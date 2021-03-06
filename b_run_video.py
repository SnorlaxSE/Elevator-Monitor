import cv2
import os
import torch 
from model import LSCCNN
from matplotlib import pyplot as plt
import numpy as np 

checkpoint_path = './weights/part_b_scale_4_epoch_24_weights.pth'
checkpoint_path = './weights/qnrf_scale_4_epoch_46_weights.pth'
checkpoint_path = './weights/part_a_scale_4_epoch_13_weights.pth'
# checkpoint_path = './weights/part_a/scale_4_epoch_13.pth'

network = LSCCNN(checkpoint_path=checkpoint_path)
if torch.cuda.is_available():
    network.cuda()
network.eval()

weights_tag = 'part_a'
nms_thresh = 0.1
image_dir = 'outputs/head-detection-frames'
output_dir = "outputs/" + os.path.basename(image_dir) + '-{}-{}-outputs'.format(weights_tag, nms_thresh)
print(output_dir)
if os.path.exists(image_dir) and not os.path.exists(output_dir):
    os.makedirs(output_dir)

for image_file in os.listdir(image_dir):
    if image_file.endswith('jpg'):
        print(image_file)

        image_filepath = os.path.join(image_dir, image_file)
        image = cv2.imread(image_filepath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        pred_dot_map, pred_box_map, img_out = network.predict_single_image(image, nms_thresh)
        head_idx = np.where(pred_dot_map > 0)
        Y, X = head_idx[-2] , head_idx[-1]
        predict_head_num = len(X)
        print(predict_head_num)

        # # add text
        # text = f"detection num: {predict_head_num}"
        # # cv2.putText(img_out, text, (50, 290), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        # cv2.putText(img_out, text, (50, 285), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255), 1)

        plt.figure()
        plt.imshow(img_out)
        output_filepath = os.path.join(output_dir, image_file)
        plt.imsave(output_filepath, img_out)
        # plt.show()