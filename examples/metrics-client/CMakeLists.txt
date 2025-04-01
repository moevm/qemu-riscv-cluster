cmake_minimum_required(VERSION 3.12 FATAL_ERROR)

project(daemon)

find_package(prometheus-cpp CONFIG REQUIRED)

add_executable(daemon src/main.cpp)
target_link_libraries(daemon PRIVATE prometheus-cpp::push)
