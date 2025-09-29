import numpy as np
import pydicom
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Reading the data 
dicomfile = pydicom.dcmread('Sample.dcm')

pixel_data = dicomfile.pixel_array

print('Image Shape',pixel_data.shape)

# Transforming unsigned 16-bit integer into the proper HU values
HU_data = np.zeros((int(pixel_data.shape[0]), int(pixel_data.shape[1])))
print('HU Data Shape',HU_data.shape)

for i, row in enumerate(pixel_data):
	for j, element in enumerate(row):
		HU_data[i][j] = (element*1) -1024

# Finding the maximum and minimum
HU_data_flat = HU_data.flatten()
max_hu = np.max(HU_data)
min_hu = np.min(HU_data)

print('Max HU', max_hu)
print('Min HU', min_hu)

# Plotting and Saving the histogram

bins = np.arange(min_hu,max_hu+1,1)
plt.hist(HU_data_flat, bins = bins)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of HU Data')
# plt.show()
plt.savefig('Histogram of HU Data')

# Choosing Region of Interest
x_aorta = 125
y_aorta = 209
width_aorta = 50
height_aorta = 50
x_bg = 195
y_bg = 170
width_bg = 50
height_bg = 50

aorta_ROI = [x_aorta, y_aorta, width_aorta, height_aorta]
bg_ROI = [x_bg, y_bg, width_bg, height_bg]

# Showing region of interest in a figure where the ROI for aorta is red rectangle and for background is Yellow rectangle

fig, ax = plt.subplots()

ax.imshow(pixel_data, cmap='gray')

roi_patch_aorta = Rectangle((x_aorta, y_aorta), width_aorta, height_aorta, linewidth=1, edgecolor='r', facecolor='none')
roi_patch_bg = Rectangle((x_bg, y_bg), width_bg, height_bg, linewidth=1, edgecolor='y', facecolor='none')

ax.add_patch(roi_patch_aorta)
ax.add_patch(roi_patch_bg)

plt.title('DICOM Image with ROI')
plt.axis('off')  # Turn off axis labels
# plt.show()
plt.savefig('DICOM Image with ROI')

# calculating the mean HU for target area, background area and noise
aorta_pixels = HU_data[y_aorta:y_aorta+height_aorta, x_aorta:x_aorta+width_aorta]
bg_pixels = HU_data[y_bg:y_bg+height_bg, x_bg:x_bg+width_bg]

mean_HU_aorta = np.mean(aorta_pixels)
mean_HU_bg = np.mean(bg_pixels)
noise = np.std(bg_pixels)

print('Mean HU Target Area', mean_HU_aorta)
print('Mean HU Background', mean_HU_bg)
print('Noise', noise)

# calculating the CNR and effective dose
CNR = (mean_HU_aorta - mean_HU_bg) / noise
CTDIvol = dicomfile.CTDIvol 
k_factor = 0.014
num_slices = 379
slice_thickness = dicomfile.SliceThickness/10 # converting mm to cm
Dose_length_factor = CTDIvol*slice_thickness*num_slices
effective_dose = Dose_length_factor * k_factor

print('CNR', CNR)
print('Effective Dose', effective_dose)
