import numpy as np
from PIL import Image
import gc
import concurrent.futures

def denoise_pixel(window:np.ndarray, sigd:int, sigr:int):
    # print('Denoising')
    h, w = window.shape
    # Normalisation factor
    factor_els = []
    elements = []
    x = -w // 2
    while x < w // 2 + 1:
        y = -h // 2
        while y < h // 2 + 1:
            small_w = np.exp(-((x**2 + y**2)/ (2 * sigd**2)) - ((int(window[h//2, w//2]) - int(window[y, x]))**2) / (2 * sigr**2))
            factor_els.append(small_w)
            elements.append(window[y, x] * small_w)
            # print(window[y,x])
            y += 1
        x += 1
    wp = sum(factor_els)
    rest = sum(elements)
    # print(wp, rest)
    return int(rest / wp)
        
def bilateral(argument):
    """
    Input: img as bytes
    radius: radius of kernel
    sigd: standard deviation of spacial component
    sigr: standard deviation of intensity component
    """
    img, radius, sigd, sigr = argument
    # Open image and convert to ndarray


    h, w = img.shape
    img_out = np.zeros((h, w), dtype=np.uint8)
    
    border = radius // 2
    x = border 
    while x < w - border:
        y = border
        while y < h - border:
            # print(f'(x, y) : {(x, y)}')
            # Build window
            winx, winy = 0, 0
            window = np.zeros((radius, radius), dtype=np.uint8)
            for i in range(x - border, x + border + 1):
                for j in range(y - border, y + border + 1):
                    window[winy % radius, winx % radius] = img[j, i]
                    winy += 1
                winx += 1
            img_out[y, x] = denoise_pixel(window, sigd, sigr)
            y += 1
        x += 1
    # Return image from array (ensuring array type is uint8)
    output = Image.fromarray(img_out[border:-border,border:-border].astype(np.uint8), 'L')
    return output

def fast_bilateral(data, radius=3, sigd=50, sigr=50):
    """
    Using concurrency
    """
    print('Applying bilateral filter')
    # Load image and convert to numpy array
    img_data = Image.open(data)
    img = np.asarray(img_data)
    print(f'Original: {img.shape}')
    h, w = img.shape
    dw = radius // 2
    # Split image into 4 sections
    # Note each section will slightly overlap
    sections = [
        (img[:,0:w // 4 + dw], radius, sigd, sigr), 
        (img[:,w // 4 - dw:w // 2 + dw], radius, sigd, sigr),
        (img[:,w // 2 - dw:3 * w // 4 + dw], radius, sigd, sigr),
        (img[:,3 * w // 4 - dw:], radius, sigd, sigr)
    ]
    results = []

    # img_out = filter(img, h, w, radius)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for section in executor.map(bilateral, sections):
            print('Appending')
            results.append(section)
    print('Concatenating ')
    img_out = np.concatenate(results, axis=1)


    del img, img_data, data, sections
    gc.collect()

    return Image.fromarray(img_out.astype(np.uint8), 'L')



if __name__ == '__main__':
    fast_bilateral('non-web-files/barbara.png', 5, 300, 300).show()