mkdir -p source && cd ./source && \
curl -L http://ceres-solver.org/ceres-solver-1.14.0.tar.gz | tar xz && \
cd ./ceres-solver-1.14.0 && \
mkdir -p build && cd ./build && \
cmake .. -DCMAKE_C_FLAGS=-fPIC -DCMAKE_CXX_FLAGS=-fPIC -DBUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF -DCMAKE_INSTALL_PREFIX:PATH=/media/data-huy && \
make -j4 install && \
cd / && rm -rf ./source/ceres-solver-1.14.0
