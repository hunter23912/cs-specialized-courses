#include <iostream>

// C++23: std::mdspan（多维数组视图）
#if __has_include(<mdspan>)
#endif

// C++23: std::print（格式化输出）
#if __has_include(<print>)
#endif

int main()
{
    std::cout << "C++版本: " << __cplusplus << "\n";

    // C++23: if consteval（编译时 if）
    // if consteval
    // {
    //     std::cout << "这是在编译时执行的\n";
    // }
    // else
    // {
    //     std::cout << "这是在运行时执行的\n";
    // }
    // 检查是否为 GCC 或 Clang
#ifdef __GNUC__
    std::cout << "编译器: GCC\n";
    std::cout << "GCC 版本: " << __GNUC__ << "." << __GNUC_MINOR__ << "." << __GNUC_PATCHLEVEL__ << "\n";
#endif

// 检查是否为 Clang
#ifdef __clang__
    std::cout << "编译器: Clang\n";
    std::cout << "Clang 版本: " << __clang_major__ << "." << __clang_minor__ << "." << __clang_patchlevel__ << "\n";
#endif

// 检查是否为 MSVC（Microsoft Visual C++）
#ifdef _MSC_VER
    std::cout << "编译器: MSVC\n";
    std::cout << "MSVC 版本: " << _MSC_VER << "\n";
#endif

    // 检查 C++ 标准版本
    std::cout << "C++ 标准版本: " << __cplusplus << "\n";
    return 0;
}