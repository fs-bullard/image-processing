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

Here is Barbara with a Gaussian Blur applied:

| $\sigma = 1$ | $\sigma = 2$|
| ------------- | ------------- |
| ![Gaussian Blur applied with sigma 1](https://github.com/fs-bullard/image-processing/assets/42214857/57104152-a608-424e-bcd2-a0887f45e1a6) | ![Gaussian Blur appiied with sigma 2](https://github.com/fs-bullard/image-processing/assets/42214857/a9780ac5-8552-4916-ab74-83fbd334c500) |

Whilst noise is definitely reduced, we also lose a significant amount of detail. Applying Gaussian blur with a higher $\sigma$ yields an even greater loss of detail:



### Median Filter

Next, I implemented the Median filter. The Median filter is slightly more complicated than the Gaussian Blur, and it is non-linear so cannot be separated. It works by replaci




