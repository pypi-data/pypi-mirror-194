import cv2
import numpy as np

from hito.func.engine.hitoFunc import HitoFunc


def eccalign(im1, im2):
    # feature_retention = 0.20
    number_of_iterations = 5000
    termination_eps = 1e-6
    # Find size of image1
    sz = im1.shape
    # 将文件分辨率缩到一半
    dim = (int(sz[1] / 2), int(sz[0] / 2))
    # Convert images to grayscale
    im1_gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im1_gray = cv2.resize(im1_gray, dim)
    im2_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.resize(im2_gray, dim)
    im1_gray = get_gradient(im2_gray)
    im2_gray = get_gradient(im2_gray)
    # Define the motion model
    # warp_mode = cv2.MOTION_AFFINE #刚性变换
    warp_mode = cv2.MOTION_EUCLIDEAN  # 只做平移旋转
    # warp_mode = cv2.MOTION_TRANSLATION  # 只做平移变换
    # warp_mode = cv2.MOTION_HOMOGRAPHY # 单应性变换

    # # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else:
        warp_matrix = np.eye(2, 3, dtype=np.float32)

    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                number_of_iterations, termination_eps)

    # Run the ECC algorithm. The results are stored in warp_matrix.
    (cc, warp_matrix) = cv2.findTransformECC(im1_gray, im2_gray, warp_matrix, warp_mode, criteria)
    # 将偏移矩阵转换回大图上
    warp_matrix[0][2] = warp_matrix[0][2] * 2
    warp_matrix[1][2] = warp_matrix[1][2] * 2
    # warp_matrix = warp_matrix*2

    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        # Use warpPerspective for Homography
        im2_aligned = cv2.warpPerspective(im2, warp_matrix, (sz[1], sz[0]),
                                          flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    else:
        # Use warpAffine for Translation, Euclidean and Affine
        im2_aligned = cv2.warpAffine(im2, warp_matrix, (sz[1], sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    return im2_aligned, warp_matrix

def get_gradient(im):
    # Calculate the x and y gradients using Sobel operator
    grad_x = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(im, cv2.CV_32F, 0, 1, ksize=3)
    # Combine the two gradients
    grad = cv2.addWeighted(np.absolute(grad_x), 0.5, np.absolute(grad_y), 0.5, 0)
    return grad

class EccAlignFunc(HitoFunc):
    def process(self, im1, im2):
        return eccalign(im1, im2)