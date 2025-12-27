#ifndef SYMBOL_TABLE_H
#define SYMBOL_TABLE_H
#include <map>
#include <string>
#include <vector>

// 符号类型枚举
enum class SymbolType { CONST, VARIABLE, PROCEDURE };

// 符号项结构体
struct Symbol {
    std::string name;
    SymbolType type;
    int value;    // 对于常量存储值，对于变量无意义
    int level;    // 嵌套层级（作用域）
    int address;  // 内存地址（仅对变量有意义）

    Symbol()
        : name(""),
          type(SymbolType::VARIABLE),
          value(0),
          level(0),
          address(0) {}

    Symbol(const std::string& name, SymbolType type, int level = 0,
        int value = 0, int address = 0)
        : name(name),
          type(type),
          value(value),
          level(level),
          address(address) {}
};

// 符号表类
class SymbolTable {
private:
    std::vector<std::map<std::string, Symbol>> scopes;  // 嵌套作用域
    int currentLevel;                                   // 当前嵌套层级
    int address;                                        // 下一个可分配地址

public:
    SymbolTable();

    // 进入新作用域
    void enterScope();

    // 离开当前作用域
    void leaveScope();

    // 添加符号
    void addSymbol(const std::string& name, SymbolType type, int value = 0);

    // 查找符号
    Symbol* findSymbol(const std::string& name);

    // 检查当前作用域中是否存在符号
    bool existInCurrentScope(const std::string& name);

    // 获取当前层级
    int getCurrentLevel() const;

    // 获取当前地址
    int getCurrentAddress() const;
};

#endif  // SYMBOL_TABLE_H