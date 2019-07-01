% cam = webcamlist;
% if isempty(cam) ~= 1
%     cam = webcam(cam{1});
%     pause(5);
%     img = snapshot(cam);
%     imshow(img);
% else
%     display('No Cam');
% end

%% New Thresholding

image = imread('image8.jpg');
mask = createSideMask(image);
imshow(image);
pause(4);
imshow(mask);
