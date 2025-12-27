#include "SemanticAnalyzer.h"
// 语义分析的主要实现，遍历AST并使用符号表执行语义检查
SemanticAnalyzer::SemanticAnalyzer(const std::shared_ptr<ASTNode>& ast)
    : ast(ast) {}

void SemanticAnalyzer::analyze() {
    if (ast) {
        analyzeNode(ast);
    }
}

void SemanticAnalyzer::analyzeNode(const std::shared_ptr<ASTNode>& node) {
    if (!node) return;

    // 根据节点类型分发到不同的处理函数
    if (node->type == "program") {
        analyzeProgram(node);
    } else if (node->type == "const_declaration") {
        analyzeConstDeclaration(node);
    } else if (node->type == "var_declaration") {
        analyzeVarDeclaration(node);
    } else if (node->type == "procedure_declaration") {
        analyzeProcDeclaration(node);
    } else if (node->type == "assign") {
        analyzeAssignStatement(node);
    } else if (node->type == "call") {
        analyzeCallStatement(node);
    } else if (node->type == "if") {
        analyzeIfStatement(node);
    } else if (node->type == "while") {
        analyzeWhileStatement(node);
    } else if (node->type == "repeat") {
        analyzeRepeatStatement(node);
    } else if (node->type == "seq") {
        // 顺序执行语句序列中的每一个语句
        for (const auto& child : node->children) {
            analyzeNode(child);
        }
    } else if (node->type == "plus" || node->type == "minus" ||
               node->type == "times" || node->type == "slash" ||
               node->type == "eql" || node->type == "neq" ||
               node->type == "lss" || node->type == "leq" ||
               node->type == "gtr" || node->type == "geq") {
        // 处理表达式
        analyzeExpression(node);
    }
}

void SemanticAnalyzer::analyzeProgram(const std::shared_ptr<ASTNode>& node) {
    // 分析程序的各个部分
    for (const auto& child : node->children) {
        analyzeNode(child);
    }
}

void SemanticAnalyzer::analyzeConstDeclaration(
    const std::shared_ptr<ASTNode>& node) {
    // 常量声明语义分析
    for (const auto& constNode : node->children) {
        if (constNode->type == "const_def") {
            std::string name = constNode->children[0]->value;
            int value = std::stoi(constNode->children[1]->value);
            try {
                symbolTable.addSymbol(name, SymbolType::CONST, value);
            } catch (const std::runtime_error& e) {
                throw SemanticError(e.what());
            }
        }
    }
}

void SemanticAnalyzer::analyzeVarDeclaration(
    const std::shared_ptr<ASTNode>& node) {
    // 变量声明语义分析
    for (const auto& identNode : node->children) {
        std::string name = identNode->value;
        try {
            symbolTable.addSymbol(name, SymbolType::VARIABLE);
        } catch (const std::runtime_error& e) {
            throw SemanticError(e.what());
        }
    }
}

void SemanticAnalyzer::analyzeProcDeclaration(
    const std::shared_ptr<ASTNode>& node) {
    // 过程声明语义分析
    std::string procName = node->children[0]->value;
    try {
        symbolTable.addSymbol(procName, SymbolType::PROCEDURE);
    } catch (const std::runtime_error& e) {
        throw SemanticError(e.what());
    }

    // 进入新作用域
    symbolTable.enterScope();

    // 分析过程体
    for (size_t i = 1; i < node->children.size(); i++) {
        analyzeNode(node->children[i]);
    }

    // 离开作用域
    symbolTable.leaveScope();
}

void SemanticAnalyzer::analyzeAssignStatement(
    const std::shared_ptr<ASTNode>& node) {
    // 分析赋值语句
    std::string identName = node->children[0]->value;
    Symbol* symbol = symbolTable.findSymbol(identName);

    if (!symbol) {
        throw SemanticError("Undefined identifier: " + identName);
    }

    if (symbol->type == SymbolType::CONST) {
        throw SemanticError("Cannot assign to constant: " + identName);
    }

    if (symbol->type == SymbolType::PROCEDURE) {
        throw SemanticError("Cannot assign to procedure: " + identName);
    }

    // 分析表达式
    analyzeNode(node->children[1]);
}

void SemanticAnalyzer::analyzeCallStatement(
    const std::shared_ptr<ASTNode>& node) {
    // 分析调用语句
    std::string procName = node->children[0]->value;
    Symbol* symbol = symbolTable.findSymbol(procName);

    if (!symbol) {
        throw SemanticError("Undefined procedure: " + procName);
    }

    if (symbol->type != SymbolType::PROCEDURE) {
        throw SemanticError(procName + " is not a procedure");
    }
}

void SemanticAnalyzer::analyzeIfStatement(
    const std::shared_ptr<ASTNode>& node) {
    // 分析条件
    analyzeNode(node->children[0]);

    // 分析then部分
    analyzeNode(node->children[1]);

    // 分析else部分（如果存在）
    if (node->children.size() > 2) {
        analyzeNode(node->children[2]);
    }
}

void SemanticAnalyzer::analyzeWhileStatement(
    const std::shared_ptr<ASTNode>& node) {
    // 分析条件
    analyzeNode(node->children[0]);

    // 分析循环体
    analyzeNode(node->children[1]);
}

void SemanticAnalyzer::analyzeRepeatStatement(
    const std::shared_ptr<ASTNode>& node) {
    // 分析循环体
    analyzeNode(node->children[0]);

    // 分析条件
    analyzeNode(node->children[1]);
}

void SemanticAnalyzer::analyzeExpression(const std::shared_ptr<ASTNode>& node) {
    // 分析表达式左右两边
    if (node->children.size() >= 1) {
        analyzeNode(node->children[0]);
    }

    if (node->children.size() >= 2) {
        analyzeNode(node->children[1]);
    }

    // 处理标识符
    if (node->type == "ident") {
        Symbol* symbol = symbolTable.findSymbol(node->value);
        if (!symbol) {
            throw SemanticError("Undefined identifier: " + node->value);
        }
    }
}