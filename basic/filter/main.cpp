#include <iostream>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

uchar computeMatMul(float kernel[][3], float im_part[][3])
{
  float sum = 0;
  for(int row = 0; row < 3; row++)
    {
      for(int time = 0; time < 3; time++)//one row will have do 3 times multip
	{
	  float elem = 0;
	   for(int col = 0; col < 3; col++)
	     elem += kernel[row][col]*im_part[col][time];
	   sum += elem;
	}
    }
  float coef = 0.0;
  for(int row = 0; row < 3; row++)
    for(int col = 0; col < 3; col++)
      //coef += (kernel[row][col] < 0)? -kernel[row][col] : kernel[row][col];
      coef += kernel[row][col];
  
  if(coef == 0)
    coef = 1;
  sum /= coef;
  
  if(sum < 0) 
    return 0;
  else
    return ( (int) sum) % 256;
}

void  my_own_filter(float kernel[][3], Mat &im_origin, Mat &im_filtered)
{
  Size im_size = im_origin.size();
  int h = im_size.height;
  int w = im_size.width;

  for(int i = 1; i < h-1; i++)
    {
      for(int j = 1; j < w-1; j++)
	{
	  float im_part[3][3];
	  for(int row = 0; row < 3; row++)
	    for(int col = 0; col < 3; col++)
	      im_part[row][col] = (float) im_origin.at<uchar>(i+row-1, j+col-1);
	  im_filtered.at<uchar>(i,j) = computeMatMul(kernel, im_part);
	  //im_filtered.at<uchar>(i,j) = computeMatMul(im_part, kernel);

	} 
    }
}

void apply_filter2D(float kernel[][3], Mat &im_origin, Mat &im_filtered)
{
  Mat filter_kernel(3, 3, CV_32FC1, kernel);
  //apply filter
  filter2D(im_origin, im_filtered, -1, filter_kernel);//-1 is a default value (see doc)
}

int main()
{
  Mat im_origin = imread("image.jpg", CV_LOAD_IMAGE_GRAYSCALE);
  
  Size im_size = im_origin.size();
  
  Mat im_filtered(im_size.height, im_size.width, CV_8UC1);

  //filter kernel to remove vertical edge:
  float rm_vert_edges_fil[3][3] = {{0, 0, 0}, {-1, 2, -1}, {0, 0, 0}};
  //float rm_horz_edges_fil[3][3] = {{0, -1, 0}, {0, 2, 0}, {0, -1, 0}};
 
  //cout << filter_kernel << endl;
  //  cout << im << endl;

  bool useOpenCV_filter = false;
  if(useOpenCV_filter)
    apply_filter2D(rm_vert_edges_fil, im_origin, im_filtered);
  else
    my_own_filter(rm_vert_edges_fil, im_origin, im_filtered);

  namedWindow("origin");
  namedWindow("filtered");
  imshow("origin", im_origin);
  imshow("filtered", im_filtered);

  while(char(waitKey(1)) != 'q') {}

  return 0;

}
