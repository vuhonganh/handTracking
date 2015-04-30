#include <iostream>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;

//global variables
const int slider_max = 10;
int slider;
Mat img;
 
//callback function for trackbar event
void on_trackbar(int , void *)
{
  Mat img_converted;
  // if(pos > 0)
    cvtColor(img, img_converted, CV_RGB2GRAY);
    // else
    //img_converted = img;

  imshow("Trackbar app", img_converted);
}

int main(int argc, char **argv)
{
  Mat img = imread("bg.jpg");
  namedWindow("Trackbar app");
  Mat gray;
  cvtColor(img, gray, CV_RGB2GRAY);
  imshow("Trackbar app", gray);
  //imshow("Trackbar app", img);
  //cout << img.shape[0] << endl;

  slider = 0;

  //createTrackbar("RGB <-> Grayscale", "Trackbar app", &slider, slider_max, on_trackbar);
  //access a pixel value in image
  //  Point toPrint(25,46);
  //cout << "im at (i,j) = " << im.at<Vec3b>(toPrint) << endl;

  //cout << "Press 'q' to quit..." << endl;
  while(1)
    {
      if(char(waitKey(1)) == 'q') break;
    }
  destroyAllWindows();
  return 0;
}
