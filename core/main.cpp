#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

#define SZ_KERNEL 5
#define SZ_STRUCT 5

int threshVal = 100;

int hsv_slider = 0;
int low_slider = 1;
int high_slider = 100;

int low_H  = 1;
int high_H = 25;

int low_S  = 38;
int high_S = 250;

int low_V  = 51;
int high_V = 242;

Mat img_orig;
Mat img_blurred;
Mat img_bin;
Mat img_bin_hsv;

// ??????? co nen ton tai duoi dang static? ton bo nho
Mat img_gray;
Mat img_hsv;
Mat st_elem = getStructuringElement(MORPH_RECT, Size(SZ_STRUCT, SZ_STRUCT)); //structure element

//ve sau co the nhet dong o duoi nay vao init
string win_orig = "origin";
string win_bin  = "binary";
string win_bin_hsv = "hsv_binary";

string loTh = "Low Threshold ";
string hiTh = "High Threshold";
string biTh = "Bin Threshold";

//img -> gaussian blur -> gray -> threshold + morphology -> binary
void simple_preproscessing(int, void *)
{      
    /*
    erode(img_gray, img_buffer, st_elem);
    dilate(img_buffer, img_buffer, st_elem);
    */

    threshold(img_gray, img_bin, threshVal, 255, THRESH_BINARY);// + THRESH_OTSU);

    //open and close to remove noise in binary image
    //API: morphologyEx(src, dst, operationType, kernel)
    morphologyEx(img_bin, img_bin, MORPH_OPEN, st_elem);
    morphologyEx(img_bin, img_bin, MORPH_CLOSE, st_elem);

    imshow(win_bin, img_bin);
    //return res;
}

//In OpenCV: in HSV color space: H : [0, 180], S: [0, 255], V: [0, 255]
void hsv_preprocessing(int, void*)
{

    cvtColor(img_blurred, img_hsv, CV_BGR2HSV);

    //get binary hsv from hsv
    //thresh values [low, high]
    int low_rangeH  = (int) (((double) low_H)/255.0 * 180);
    int high_rangeH = (int) (((double) high_H)/255.0 * 180);

    //API openCV: inRange(src, low, upp, dst)
    inRange(img_hsv, Scalar(low_rangeH, low_S, low_V), Scalar(high_rangeH, high_S, high_V), img_bin_hsv);

    //remove noise in binary image
    //API: morphologyEx(src, dst, operationType, kernel)
    morphologyEx(img_bin_hsv, img_bin_hsv, MORPH_OPEN, st_elem);
    morphologyEx(img_bin_hsv, img_bin_hsv, MORPH_CLOSE, st_elem);
//    erode(img_gray, img_buffer, st_elem);
//    dilate(img_buffer, img_buffer, st_elem);

    imshow(win_bin_hsv, img_bin_hsv);
}

void on_hsv_trackbar(int, void *)
{
    switch(hsv_slider)
    {
    case 0:
        setTrackbarPos(loTh, win_bin_hsv, low_H);
        setTrackbarPos(hiTh, win_bin_hsv, high_H);
        break;
    case 1:
        setTrackbarPos(loTh, win_bin_hsv, low_S);
        setTrackbarPos(hiTh, win_bin_hsv, high_S);
        break;
    case 2:
        setTrackbarPos(loTh, win_bin_hsv, low_V);
        setTrackbarPos(hiTh, win_bin_hsv, high_V);
        break;
    }
}

void on_low_thresh_trackbar(int, void *)
{
    switch(hsv_slider)
    {
    case 0:
        low_H = min(high_slider - 1, low_slider);
        setTrackbarPos(loTh, win_bin_hsv, low_H);
        break;
    case 1:
        low_S = min(high_slider - 1, low_slider);
        setTrackbarPos(loTh, win_bin_hsv, low_S);
        break;
    case 2:
        low_V = min(high_slider - 1, low_slider);
        setTrackbarPos(loTh, win_bin_hsv, low_V);
        break;
    }
}

void on_high_thresh_trackbar(int, void *)
{
    switch(hsv_slider)
    {
    case 0:
        high_H = max(low_slider + 1, high_slider);
        setTrackbarPos(hiTh, win_bin_hsv, high_H);
        break;
    case 1:
        high_S = max(low_slider + 1, high_slider);
        setTrackbarPos(hiTh, win_bin_hsv, high_S);
        break;
    case 2:
        high_V = max(low_slider + 1, high_slider);
        setTrackbarPos(hiTh, win_bin_hsv, high_V);
        break;
    }
}

/*
def find_contour_hull(binary_image):
    #find the contour
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #search the maximum contour in the hierachy tree of contours
    max_area = 0
    ci = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if(area > max_area):
            max_area = area
            ci = i

    cnt = contours[ci]
    hull = cv2.convexHull(cnt)
    hull_idx = cv2.convexHull(cnt, returnPoints = False)

    return cnt, hull, hull_idx
*/



/*
def draws_contour_hull(img, cnt, hull):
    #draws the image with only the contour and its convex hull
    drawing = np.zeros(img.shape, np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 3)
    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
    return drawing
*/


int main()
{

    namedWindow(win_orig);
    namedWindow(win_bin);
    namedWindow(win_bin_hsv);

    VideoCapture cap(0);
    if(!cap.isOpened())
    {
        cerr << "capture camera has problem\n";
        return -1;
    }

    createTrackbar("0-H, 1-S, 2-V", win_bin_hsv, &hsv_slider, 2, on_hsv_trackbar);
    createTrackbar(loTh, win_bin_hsv, &low_slider, 255, on_low_thresh_trackbar);
    createTrackbar(hiTh, win_bin_hsv, &high_slider, 255, on_high_thresh_trackbar);
    createTrackbar(biTh, win_bin, &threshVal, 255, simple_preproscessing);
    
    //img_orig = imread("bg.jpg");
    while(char(waitKey(1)) != 'q' )
    {
        cap >> img_orig;

        //get blurred and gray
        GaussianBlur(img_orig, img_blurred, Size(SZ_KERNEL, SZ_KERNEL), 0, 0);
        cvtColor(img_blurred, img_gray, CV_BGR2GRAY);

        //imshow(win_orig, img_orig);
        imshow(win_orig, img_blurred);//show blurred of original

        //init
        simple_preproscessing(0, 0);
        hsv_preprocessing(0, 0);
    }

    return 0;
}


