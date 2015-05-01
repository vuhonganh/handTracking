#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include "printSt.h"

using namespace std;
using namespace cv;

Mat im, im_processed;

int choice_slider = 0; //0: erode, 1: dilate
int size_slider   = 5;

void process()
{
  size_slider = max(1, size_slider);

  Mat st_elem = getStructuringElement(MORPH_RECT, Size(size_slider, size_slider));
  
  if(choice_slider == 0)
    erode(im, im_processed, st_elem);
  else
    dilate(im, im_processed, st_elem);
  imshow("processed image", im_processed);
}

void on_choice_slider(int, void *)
{
  process();
}

void on_size_slider(int, void *)
{
  int size = max(2, size_slider);
  size = (size % 2 == 0)? size + 1 : size;
  setTrackbarPos("kernel size", "processed image", size);
  process();
}

int main()
{
  im = imread("j.png");

  namedWindow("original image");
  namedWindow("processed image");

  imshow("original image", im);
  Mat st_elem = getStructuringElement(MORPH_RECT, Size(size_slider, size_slider));
  
  erode(im, im_processed, st_elem);
  imshow("processed image", im_processed);

  createTrackbar("Erode/Dilate", "processed image", &choice_slider, 1, on_choice_slider);
  createTrackbar("kernel size", "processed image", &size_slider, 21, on_size_slider);

  printSt(5);

  while(char(waitKey(1) != 'q')){}
  
  return 0;
}
