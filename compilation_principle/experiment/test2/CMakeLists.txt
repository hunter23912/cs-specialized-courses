# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

cmake_minimum_required(VERSION 3.10)
project(PL0CompilerTest)

# 包含头文件目录
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include")

# 添加源文件,再添加一个parser.cpp文件
set(SOURCES
    src/Lexer.cpp
    src/Parser.cpp
    src/SymbolTable.cc
    src/SemanticAnalyzer.cc
    src/CodeGenerator.cc
    tests/test.cpp
)

# 生成可执行文件,默认生成在 build 目录下
add_executable(test_program ${SOURCES})