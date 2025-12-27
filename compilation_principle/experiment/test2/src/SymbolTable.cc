#include "SymbolTable.h"

#include <stdexcept>

// 符号表，跟踪和管理程序中的标识符

SymbolTable::SymbolTable() : currentLevel(0), address(0) {
    // 初始化全局作用域
    scopes.push_back(std::map<std::string, Symbol>());
}

void SymbolTable::enterScope() {
    currentLevel++;
    scopes.push_back(std::map<std::string, Symbol>());
}

void SymbolTable::leaveScope() {
    if (currentLevel > 0) {
        scopes.pop_back();
        currentLevel--;
    }
}

void SymbolTable::addSymbol(
    const std::string& name, SymbolType type, int value) {
    // 检查当前作用域是否已存在同名符号
    if (existInCurrentScope(name)) {
        throw std::runtime_error(
            "Symbol '" + name + "' already defined in the current scope");
    }

    int addr = address;
    if (type == SymbolType::VARIABLE) {
        address++;  // 为变量分配地址
    }

    // 添加到当前作用域
    scopes[currentLevel][name] = Symbol(name, type, currentLevel, value, addr);
}

Symbol* SymbolTable::findSymbol(const std::string& name) {
    // 从内层作用域向外层查找
    for (int i = currentLevel; i >= 0; i--) {
        auto it = scopes[i].find(name);
        if (it != scopes[i].end()) {
            return &(it->second);
        }
    }
    return nullptr;  // 未找到符号
}

bool SymbolTable::existInCurrentScope(const std::string& name) {
    return scopes[currentLevel].find(name) != scopes[currentLevel].end();
}

int SymbolTable::getCurrentLevel() const {
    return currentLevel;
}

int SymbolTable::getCurrentAddress() const {
    return address;
}