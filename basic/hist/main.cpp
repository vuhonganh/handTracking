#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;

Mat im, im_eq;  //original image and image equalized
int choice = 0; //choose to show original image or equalized image
string winName = "image";
string trackbarName = "origin/equalized";
void on_trackbar(int, void*)
{
  if(choice == 0)
    imshow(winName, im);
  else
    imshow(winName, im_eq);
}

int main()
{
  im = imread("bg.jpg");
  namedWindow(winName);
  imshow(winName, im);
  vector<Mat> channels, channels_eq;

  //divide a multi-channels array into several single-channel arrays
  split(im, channels);

  for(size_t i = 0; i < channels.size(); i++)
    {
      Mat eqElem;
  
      //equalize histograms
      equalizeHist(channels[i], eqElem);
      channels_eq.push_back(eqElem);
    }
  
  //Creates one multichannel array out of several single-channel ones
  merge(channels_eq, im_eq);

  createTrackbar(trackbarName, winName, &choice, 1, on_trackbar);
  
  while(char(waitKey(1) != 'q') ) {}
  
  destroyAllWindows();
  
  return 0;
  
}
