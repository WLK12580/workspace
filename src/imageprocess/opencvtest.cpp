#include<opencv2/opencv.hpp>
#include<iostream>

int main() {
  cv::Mat img = cv::imread("/home/wlk/workspace/autocar/Image/image.png", cv::IMREAD_COLOR);
  cv::imshow("img", img);
  cv::waitKey(0);
  return 0;
}
