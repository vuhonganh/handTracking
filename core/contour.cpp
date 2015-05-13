#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

#define SZ_KERNEL 5
#define SZ_STRUCT 5

int threshVal = 100;

Mat img_orig;
Mat img_bin;
Mat img_gray;

string win_orig = "origin";
string win_bin  = "binary";

void simple_preposcessing(int, void *)
{

    Mat img_buffer;
    Mat img_blurred;
  
    GaussianBlur(img_orig, img_blurred, Size(SZ_KERNEL, SZ_KERNEL), 0, 0);
    cvtColor(img_blurred, img_gray, CV_RGB2GRAY);
  
    Mat st_elem = getStructuringElement(MORPH_RECT, Size(SZ_STRUCT, SZ_STRUCT));

    erode(img_gray, img_buffer, st_elem);
    dilate(img_buffer, img_buffer, st_elem);

    threshold(img_buffer, img_bin, threshVal, 255, THRESH_BINARY);// + THRESH_OTSU);
    imshow(win_bin, img_bin);
    //return res;
}

int main()
{
    namedWindow(win_orig);
    namedWindow(win_bin);

    img_orig = imread("bg.jpg");
    imshow(win_orig, img_orig);

    createTrackbar("binThresh", win_bin, &threshVal, 255, simple_preposcessing);

    //init
    simple_preposcessing(0, 0);


    while(char(waitKey(1)) != 'q' ) {}

    return 0;
}


