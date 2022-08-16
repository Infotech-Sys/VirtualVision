#include<iostream>
#include<string>
#include "opencv4/opencv2/highgui.hpp"
#include "opencv4/opencv2/core.hpp"
#include "opencv4/opencv2/imgproc.hpp"

class AutoEdgeDetector {
    public:
    cv::Mat orginal_image,grayscale_image,threshold_image,border_image;
    double perfect_threshold_value;
    
    
    void find_threshold_value(){
        cv::cvtColor(orginal_image,grayscale_image,cv::COLOR_BGR2GRAY);
        perfect_threshold_value = cv::threshold(grayscale_image,threshold_image,0,255,cv::THRESH_BINARY + cv::THRESH_OTSU);
    }
    

    void edge_detection(){
        cv::Mat blurImage;
        cv::GaussianBlur(threshold_image,blurImage,cv::Size2d(3,3),1);
        cv::Canny(blurImage,border_image,perfect_threshold_value-10,perfect_threshold_value+10,3);
        

    }

    void invert_border(){

    }

    void contour_edge(){

    }

    void add_color(){

    }
};

int main(){
    std::cout<<"Hello World\n";    
    return 0;
}