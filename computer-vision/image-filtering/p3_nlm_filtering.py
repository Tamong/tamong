"""
CS 4391 Homework 2 Programming: Part 4 - non-local means filter
Implement the nlm_filtering() function in this python script
"""
 
import cv2
import numpy as np
import math

def nlm_filtering(
    img: np.uint8,
    intensity_variance: float,
    patch_size: int,
    window_size: int,
) -> np.uint8:
    """
    Homework 2 Part 4
    Compute the filtered image given an input image, kernel size of image patch, spatial variance, and intensity range variance
    """

    img = img / 255
    img = img.astype("float32")
    img_filtered = np.zeros(img.shape) # Placeholder of the filtered image
    
    # Todo: For each pixel position [i, j], you need to compute the filtered output: img_filtered[i, j] using a non-local means filter
    # step 1: compute window_sizexwindow_size filter weights of the non-local means filter in terms of intensity_variance. 
    # step 2: compute the filtered pixel img_filtered[i, j] using the obtained kernel weights and the pixel values in the search window
    # Please see slides 30 and 31 of lecture 6. Clarification: the patch_size refers to the size of small image patches (image content in yellow, 
    # red, and blue boxes in the slide 30); intensity_variance denotes sigma^2 in slide 30; the window_size is the size of the search window as illustrated in slide 31.
    # Tip: use zero-padding to address the black border issue. 

    # ********************************
    # Your code is here.
    # ********************************    
            
    # PHILIP WALLIS
    # PTW190000
    # CS4391.001 - Homework 2
    # 9/22/2023
    # took about 220 seconds to run.......

    pad_size = window_size // 2
    padded_img = np.pad(img, ((pad_size, pad_size), (pad_size, pad_size)), 'constant')

    # loop through the entire image
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            i_ = i + pad_size
            j_ = j + pad_size

            # Initialize weights
            weights = np.zeros((window_size, window_size))

            # Calculate central patch
            x_start_c = i_ - patch_size // 2
            x_end_c = i_ + patch_size // 2 + 1
            y_start_c = j_ - patch_size // 2
            y_end_c = j_ + patch_size // 2 + 1
            central_patch = padded_img[x_start_c:x_end_c, y_start_c:y_end_c]

            # loop through the patch
            for m in range(-pad_size, pad_size + 1):
                for n in range(-pad_size, pad_size + 1):
                    
                    # calculate the patch
                    x_start = i_ + m - patch_size // 2
                    x_end = i_ + m + patch_size // 2 + 1
                    y_start = j_ + n - patch_size // 2
                    y_end = j_ + n + patch_size // 2 + 1
                    patch = padded_img[x_start:x_end, y_start:y_end]

                    # Only calculate the weight if the patch sizes match
                    if patch.shape == central_patch.shape:
                        diff = (patch - central_patch) ** 2
                        weight = np.exp(-np.sum(diff) / intensity_variance)
                        weights[m + pad_size, n + pad_size] = weight

            # Normalize weights and calculate filtered pixel value
            weights /= np.sum(weights)

            # get the window
            window = padded_img[i_ - pad_size:i_ + pad_size + 1, j_ - pad_size:j_ + pad_size + 1]

            # apply the filter and save the new value
            img_filtered[i, j] = np.sum(window * weights)

    img_filtered = img_filtered * 255
    img_filtered = np.uint8(img_filtered)
    return img_filtered


if __name__ == "__main__":
    img = cv2.imread("data/img/butterfly.jpeg", 0) # read gray image
    img = cv2.resize(img, (256, 256), interpolation = cv2.INTER_AREA) # reduce image size for saving your computation time
    cv2.imwrite('results/im_original.png', img) # save image 
    
    # Generate Gaussian noise
    noise = np.random.normal(0,0.6,img.size)
    noise = noise.reshape(img.shape[0],img.shape[1]).astype('uint8')
   
    # Add the generated Gaussian noise to the image
    img_noise = cv2.add(img, noise)
    cv2.imwrite('results/im_noisy.png', img_noise)
    
    # Bilateral filtering
    intensity_variance = 1
    patch_size = 5 # small image patch size
    window_size = 15 # serach window size
    img_bi = nlm_filtering(img_noise, intensity_variance, patch_size, window_size)
    cv2.imwrite('results/im_nlm.png', img_bi)