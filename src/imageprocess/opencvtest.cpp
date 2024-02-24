#include<opencv2/opencv.hpp>
#include<iostream>

int main() {
  cv::Mat img = cv::imread("./Image/test.jpg", cv::IMREAD_COLOR); //路径是基于编译时的cmake路径的，而不是相对于当前原文将的路径
  if(img.empty()){
    std::cout<<"image read failed\n";
  }
  cv::namedWindow("img",cv::WINDOW_AUTOSIZE);
  cv::imshow("img", img);
  cv::waitKey(0);
  return 0;
}
