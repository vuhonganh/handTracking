#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

bool writeVideoFromCap(VideoCapture &cap, VideoWriter &put)
{
  Size S = Size( (int) cap.get(CV_CAP_PROP_FRAME_WIDTH), (int) cap.get(CV_CAP_PROP_FRAME_HEIGHT) );

  //make a video writer object and initialize at 30 frame per second
  put = VideoWriter("output.mpg", CV_FOURCC('M', 'P', 'E', 'G'), 30, S);
  if(!put.isOpened())
    {
      cout << "out put file could not be created for writing video" << endl;
      return false;
    }
  return true;
}

int main()
{
  //0 is the ID of the built-in laptop camera, change if you want to use other
  VideoCapture cap(0);

  //check if camera was opened properly
  if(!cap.isOpened())
    {
      cout << "capture camera has problem" << endl;
      return -1;
    }

  //create a window 
  namedWindow("Video");
   
  VideoWriter put;
  bool writeVideo = writeVideoFromCap(cap, put);

  //play the video in a loop until it ends
  while(char(waitKey(1)) != 'q' && cap.isOpened())
    {
      Mat frame;
      cap >> frame;

      //check if the video is over
      if(frame.empty())
	{
	  cout << "Video over" << endl;
	  break;
	}
      imshow("Video", frame);
      if(writeVideo)
	put << frame;
    }
  return 0;
}
