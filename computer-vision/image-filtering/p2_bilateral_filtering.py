"""
CS 4391 Homework 2 Programming: Part 3 - bilateral filter
Implement the bilateral_filtering() function in this python script
"""
 
import cv2
import numpy as np
import math

def bilateral_filtering(
    img: np.uint8,
    spatial_variance: float,
    intensity_variance: float,
    kernel_size: int,
) -> np.uint8:
    """
    Homework 2 Part 3
    Compute the bilaterally filtered image given an input image, kernel size, spatial variance, and intensity range variance
    """

    img = img / 255
    img = img.astype("float32")
    img_filtered = np.zeros(img.shape) # Placeholder of the filtered image
    
    # Todo: For each pixel position [i, j], you need to compute the filtered output: img_filtered[i, j]
    # step 1: compute kernel_sizexkernel_size spatial and intensity range weights of the bilateral filter in terms of spatial_variance and intensity_variance. 
    # step 2: compute the filtered pixel img_filtered[i, j] using the obtained kernel weights and the neighboring pixels of img[i, j] in the kernel_sizexkernel_size local window
    # The bilateral filtering formula can be found in slide 15 of lecture 6
    # Tip: use zero-padding to address the black border issue.

    # ********************************
    # Your code is here.
    # ********************************
    
    # PHILIP WALLIS
    # PTW190000
    # CS4391.001 - Homework 2
    # 9/22/2023

    half_kernel = kernel_size // 2

    # get the x and y coordinates of the kernel
    x, y = np.meshgrid(
        np.linspace(-half_kernel, half_kernel, kernel_size),
        np.linspace(-half_kernel, half_kernel, kernel_size),
    )

    # for each pixel, compute the spatial and intensity weights
    spatial_filter = np.exp(-(x ** 2 + y ** 2) / (2 * spatial_variance))

    # pad the edge of the image
    padded_img = np.pad(img, ((half_kernel, half_kernel), (half_kernel, half_kernel)), 'constant')

    # for height
    for i in range(img.shape[0]):
        # for width
        for j in range(img.shape[1]):
            
            region = padded_img[i:i + kernel_size, j:j + kernel_size]
            
            # Compute the intensity Gaussian filter
            intensity_filter = np.exp(-((region - img[i, j]) ** 2) / (2 * intensity_variance))
            
            # Compute the bilateral filter
            bilateral_filter = spatial_filter * intensity_filter
            
            # apply the filter 
            weighted_sum = np.sum(region * bilateral_filter)
            normalization_factor = np.sum(bilateral_filter)
        
            # save the new value
            img_filtered[i, j] = weighted_sum / normalization_factor

    
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
    spatial_variance = 30 # signma_s^2
    intensity_variance = 0.5 # sigma_r^2
    kernel_size = 7
    img_bi = bilateral_filtering(img_noise, spatial_variance, intensity_variance, kernel_size)
    cv2.imwrite('results/im_bilateral.png', img_bi)