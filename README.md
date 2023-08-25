# image-processing

## Introduction

[tooNoisy](https://toonoisy.nw.r.appspot.com/compare) is a web app that allows you to reduce noise in images one of three ways:
- Gaussian Blur
- Median Filter
- Bilateral Blur

Most of the work was done during Summer 2022; I was interested in both image processing and improving my Python skills, and ended up building this. 

I'd encourage anyone seeing this to visit the website (linked above), but here is a quick overview. I go into more detail in the [about section](https://toonoisy.co.uk/about).

## Overview

Let's use barbara as an example image

![noisy barbara](https://storage.googleapis.com/toonoisy_ims/barbara.png)

### Gaussian Blur

Gaussian Blur was implemented first. The general idea behind this filter is to replace each pixel in the image with the weighted sum of its neightbours, where the weights are determined by the Gaussian function:

$$f(x) = \frac{1}{\sigma \sqrt{2 \pi}} \exp\left(\frac{-(x - \mu)^2}{2 \sigma^2}\right)$$

Initial naiive for loop based attempts were succesful but extremely slow. A short attention span and limited free time led me to read up on faster methods, and so instead tooNoisy implements the Gaussian Blur as a convolution with two 1D Gaussian Kernels (separating filter into two passes reduces time complexity by a factor of kernel width).

Here is Barbara with Gaussian Blurs applied:

| $\sigma = 1$ | $\sigma = 2$|
| ------------- | ------------- |
| ![Gaussian Blur applied with sigma 1](https://github.com/fs-bullard/image-processing/assets/42214857/57104152-a608-424e-bcd2-a0887f45e1a6) | ![Gaussian Blur appiied with sigma 2](https://github.com/fs-bullard/image-processing/assets/42214857/a9780ac5-8552-4916-ab74-83fbd334c500) |

Whilst noise is definitely reduced, we also lose a significant amount of detail. Applying Gaussian blur with a higher $\sigma$ yields an even greater loss of detail:



### Median Filter

Next, I implemented the Median filter. The Median filter is slightly more complicated than the Gaussian Blur, and it is non-linear so cannot be separated. It works by replacing each pixel with the median value of the pixels in the surrounding window (of chosen width).

Here is Barbara with Median filters applied:

| width = 3px | width = 5px |
| ------------- | ------------- |
| ![blur-og_9708622barbara](https://github.com/fs-bullard/image-processing/assets/42214857/fb20c8af-d786-433d-994e-adfa64d7d618) | ![blur-og_9708622barbara](https://github.com/fs-bullard/image-processing/assets/42214857/5a121c11-cdec-4a9e-93b6-9cae35a19584) |

Clearly, Barbara is both less noisy than in the original image, and more detailed than with Gaussian blur applied. The Median filter is especially good at preserving edges.

---

*Side note: how we calculate the median pixel value of the window is interesting. The obvious approach would be to sort pixels by value, in* $O(n \log{n})$ *time. We can do better, however, by applying the [median of medians algorithm](https://en.wikipedia.org/wiki/Median_of_medians), which finds an approximate median in* $O(n)$ *time. Consider the window as an array of 8-bit integers, the median of medians algorithm works by:* 
1. *Split the array into many short (5 number long) subarrays*
2. *Sort the subarrays (yes sorting is* $O(n\log{n})$ *, but here* $n=5$ *is small, so this can be treated as a constant time operation.)*
3. *Calculate the median of each subarray, and form an array of medians*
4. *Find the median of this list, if the list is 5 or fewer medians long then find median as above, otherwise apply the median of medians function to find median via recursion.*
5. *This median is the 'pivot'. Build two new arrays, one with elements smaller than pivot, and one with elements larger than pivot.*
6. *Finally, If the left and right arrays are equal in length, the pivot is returned as the median, otherwise the median of medians function is applied to either the smaller or larger array, if there are more elements in the smaller or larger array respectively.*

---

We can still do better, though. The Median filter seems to produce some weird effects in places, and is still losing a lot of detail. 

### Bilateral Blur

The final filter implemented last summer, Bilateral blur can be thought of as a normalised Gaussian blur, but with pixel values weighted both by spatial and range distance from the subject pixel. The Bilateral filter is defined as:

$$ I_f(x) = \frac{1}{W_p} \sum_{x_i \in \Omega}{ I(x_i) f_r(||I(x_i) - I(x)||)g_s(||x_i - x ||) } $$

Where

- $I_f(x)$ is the filtered intensity of the pixel of coordinates $x$
- $I$ is the original intensity
- $\Omega$ is the window centred on $x$
- $f_r$ is the range kernel for smoothing distances in intensities
- $g_s$ is the spatial kernel for smoothing differences in coordinates

Both of the kernels are implemented here as the Gaussian function. The normalisation term $W_p$ is defined as the sum of the product of the two kernels over the window.

We have two parameters here, $\sigma_r$ and $\sigma_d$, which are the standard deviations of their respective Gaussian functions.

Here is Barbara with Bilateral Blur applied:

| $\sigma_r$ = 100, $\sigma_d$ = 100 | $\sigma_r$ = 100, $\sigma_d$ = 150 | $\sigma_r$ = 150, $\sigma_d$ = 100 |
| ------------- | ------------- | ------------- |
|  |  |  |

