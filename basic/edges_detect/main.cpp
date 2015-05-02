#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;


Mat edges, edges_thresholded;
string winName = "thresholded scharr edges", trackbarName = "threshold value";
int slider = 50;

void on_slider(int, void *)
{
  if(!edges.empty())
    {
      threshold(edges, edges_thresholded, slider, 255, THRESH_TOZERO);
      imshow(winName, edges_thresholded);
    }
}

int main()
{
  Mat im = imread("lena.jpg");
  Mat im_blurred;

  //blur image to remove noise
  GaussianBlur(im, im_blurred, Size(3,3), 0);
  
  //change to gray scale
  Mat gray;
  cvtColor(im_blurred, gray, CV_RGB2GRAY);
  
  //start calculating gradient
  Mat Gx, Gy;
  Scharr(gray, Gx, CV_32F, 1, 0);//CV_32F for calculating
  Scharr(gray, Gy, CV_32F, 0, 1);

  pow(Gx, 2, Gx);
  pow(Gy, 2, Gy);
  
  Mat G;
  sqrt(Gx+Gy, G);
  //to display, need to reconvert to CV_8U
  G.convertTo(edges, CV_8U);
  
  namedWindow(winName);
  threshold(edges, edges_thresholded, slider, 255, THRESH_TOZERO);
  imshow(winName, edges_thresholded);  
  createTrackbar(trackbarName, winName, &slider, 255, on_slider);//255 the max value a slider could be

  while(char(waitKey(1)) != 'q'){}
 
  return 0;
  
}
