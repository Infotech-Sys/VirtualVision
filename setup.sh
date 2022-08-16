#!/bin/bash

install_dep (){
	sudo pacman --noconfirm -Sy git vim cmake gdb clang llvm wget unzip zip
}
download_opencv (){
	[ ! -d "thirdparty" ] && {mkdir thirdparty}
	cd thirdparty
	[ ! -d "zip" ] && {mkdir zip}
	cd zip
	[ ! -f "opencv.zip" ] && wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip 
	[ ! -f "opencv_contrib.zip" ] && wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.x.zip
	cd ../../
}
build_opencv (){
	cd thirdparty
	cp zip/opencv*.zip .
	[ ! -d "opencv-4.x" ] && unzip opencv.zip
	[ ! -d "opencv_contrib-4.x" ] && unzip opencv_contrib.zip
	rm *.zip
	[ ! -d "build_opencv" ] && mkdir -p build_opencv
	cd build_opencv
	cmake -DCMAKE_BUILD_TYPE=RELEASE -DOPENCV_GENERATE_PKGCONFIG=YES -DOPENCV_EXTRA_MODUstLES_PATH=../opencv_contrib-4.x/modules ../opencv-4.x
	sudo make install -j$(nproc)
	cd ../../
}
install_emsdk (){
	cd thirdparty
	git clone https://github.com/emscripten-core/emsdk.git
	cd emsdk
	./emsdk install latest
	./emsdk activate latest
	source ./emsdk_env.sh
	cd ../../
}
build_opencv_js (){
	source emsdk_env.sh
	cp others/build_js.py thirdparty/opencv-4.x/platforms/js/
	cd thirdparty
	python opencv-4.x/platforms/js/build_js.py build_wasm --build_wasm --emscripten_dir="emsdk/upstream/emscripten"
}
# install_dep
# download_opencv
# build_opencv
# install_emsdk
build_opencv_js
