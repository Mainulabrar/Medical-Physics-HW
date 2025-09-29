% Read the DICOM file
dicom_info = dicominfo('Sample.dcm');  % Read DICOM metadata
dicom_image = dicomread(dicom_info);  % Read DICOM pixel data

% Display the DICOM image
imshow(dicom_image, []);  % Display with default windowing (automatic scaling)
colormap(gray);  % Set colormap to grayscale
colorbar;  % Display colorbar with pixel intensity values
title('DICOM Image');  % Set title for the image
