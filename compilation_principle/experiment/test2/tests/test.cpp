#include <exception>
#include <string>
#include <vector>

#include "CodeGenerator.h"
#include "Lexer.h"
#include "Parser.h"
#include "SemanticAnalyzer.h"

// 测试中间代码生成
void test_code_generator() {
    std::vector<std::string> test_cases = {"a * (b + c)",
        "x := y + z * 2",
        "a + b * c / d - e",
        "(a + b) * (c - d)",
        "a > b + c",
        "x := (a + b) * (c - d) / e",
        "a * b + c * d",
        "a := b := c + d",
        "-a * b",
        "a * -b"};

    for (size_t i = 0; i < test_cases.size(); i++) {
        std::string input = test_cases[i];
        // std::string output_file =
        // "../../codegen_output_" + std::to_string(i + 1) + ".txt";

        std::cout << "\nTest case " << (i + 1) << ": " << input << std::endl;
        try {
            // 词法分析
            Lexer lexer(input);

            // 收集所有token
            std::vector<Token> tokens;
            Token token;
            do {
                token = lexer.get_next_token();
                if (token.type != "EOF") {
                    tokens.push_back(token);
                }
            } while (token.type != "EOF");

            // 语法分析
            Parser parser(tokens);
            auto ast = parser.parse();

            // 中间代码生成
            CodeGenerator generator;
            generator.generate(ast);

            std::cout << "Generated quadruples:" << std::endl;
            for (const auto &quad : generator.getQuadruples()) {
                std::cout << quad.toString() << std::endl;
            }

            // 保存到文件
            // generator.saveToFile(output_file);
            // std::cout << "Intermediate code saved to " << output_file
            //   << std::endl;

        } catch (const std::exception &e) {
            std::cerr << "Error: " << e.what() << std::endl;
        }
        std::cout << "----------------------------------------" << std::endl;
    }
}

// 测试语义分析器
void test_semantic_analyzer() {
    std::vector<std::pair<std::string, std::shared_ptr<ASTNode>>> test_cases;

    // 测试用例1：变量未声明就使用
    {
        auto program = std::make_shared<ASTNode>("program");
        auto stmt = std::make_shared<ASTNode>("assign");
        auto ident = std::make_shared<ASTNode>("ident", "x");
        auto value = std::make_shared<ASTNode>("number", "10");
        stmt->children.push_back(ident);
        stmt->children.push_back(value);
        program->children.push_back(stmt);

        test_cases.push_back({"Undeclared variable", program});
    }

    // 测试用例2：给常量赋值
    {
        auto program = std::make_shared<ASTNode>("program");
        auto constDecl = std::make_shared<ASTNode>("const_declaration");
        auto constDef = std::make_shared<ASTNode>("const_def");
        constDef->children.push_back(std::make_shared<ASTNode>("ident", "PI"));
        constDef->children.push_back(
            std::make_shared<ASTNode>("number", "314"));
        constDecl->children.push_back(constDef);

        auto stmt = std::make_shared<ASTNode>("assign");
        stmt->children.push_back(std::make_shared<ASTNode>("ident", "PI"));
        stmt->children.push_back(std::make_shared<ASTNode>("number", "3"));

        program->children.push_back(constDecl);
        program->children.push_back(stmt);

        test_cases.push_back({"Assign to constant", program});
    }

    // 测试用例3：正确的变量声明和赋值
    {
        auto program = std::make_shared<ASTNode>("program");
        auto varDecl = std::make_shared<ASTNode>("var_declaration");
        varDecl->children.push_back(std::make_shared<ASTNode>("ident", "x"));

        auto stmt = std::make_shared<ASTNode>("assign");
        stmt->children.push_back(std::make_shared<ASTNode>("ident", "x"));
        stmt->children.push_back(std::make_shared<ASTNode>("number", "10"));

        program->children.push_back(varDecl);
        program->children.push_back(stmt);

        test_cases.push_back(
            {"Valid variable declaration and assignment", program});
    }

    // 运行测试用例
    for (const auto &test_case : test_cases) {
        std::cout << "Testing: " << test_case.first << std::endl;
        try {
            SemanticAnalyzer analyzer(test_case.second);
            analyzer.analyze();
            std::cout << "Semantic analysis passed." << std::endl;
        } catch (const SemanticError &e) {
            std::cout << "Semantic error detected: " << e.what() << std::endl;
        }
        std::cout << "----------------------------------------" << std::endl;
    }
}

// 测试词法，写文件到output.txt
void test_lexer(int argc, char *argv[]) {
    if (argc != 3) {
        std::string defaultArg1 = "../../input.txt";
        std::string defaultArg2 = "../../output.txt";
        argv[1] = new char[defaultArg1.size() + 1];
        strcpy_s(argv[1], defaultArg1.size() + 1, defaultArg1.c_str());

        argv[2] = new char[defaultArg2.size() + 1];
        strcpy_s(argv[2], defaultArg2.size() + 1, defaultArg2.c_str());

        std::cout << "Already set default input file name as " << argv[1]
                  << " and output file name as " << argv[2] << std::endl;
    }

    try {
        perform_lexical_analysis(argv[1], argv[2]);
        std::cout
            << "Lexical analysis completed successfully. Output written to "
            << argv[2] << std::endl;
        std::cout << "已完成" << std::endl;
    } catch (const std::exception &e) {
        std::cerr << " Error" << e.what() << std::endl;
    }
}

// 测试词法
void test_lexer_errors() {
    std::vector<std::string> error_cases = {
        // "a := 3.4.5;",            // 多个小数点
        // "123abc",                 // 数字后面跟字母
        // "a := 'unclosed string",  // 未闭合的字符串
        // "a := :=",                // 重复的赋值符号
        // "a & b",                  // 未支持的运算符
        // "const pi = 3.14; var x, y; procedure square; begin x := y * y; end;
        // "
        "begin call square; end.",
        // "a := b ++ c;",                             // 未支持的 "++"
        // "a := b -- c;",                             // 未支持的 "--"
        // "a := b || c;",                             // 未支持的 "||"
        // "a := b @ c;",                              // 未支持的 "@"
        // "a := b # c;",                              // 未支持的 "#"
        // "a := (b + c;",                             // 未闭合的 "("
        // "a := b + c);",                             // 未闭合的 ")"
        // "a := := b;",                               // 连续的 ":="
        // "a := b; /* This is a comment */ c := d;",  // 正常注释
        // "a := b; /* Unclosed comment",              // 未闭合的注释
        // "a := b; /* Outer comment /* Inner comment */ End of outer */",
        // "a := (b + c) * (d - e) / f;",
        // "if a > b then c := d else e := f;",
        // "while a < b do a := a + 1;",
        // "repeat a := a - 1; until a = 0;",
    };

    for (const auto &test_case : error_cases) {
        std::cout << "\nCase: " << test_case << std::endl;
        try {
            Lexer lexer(test_case);
            Token token;
            do {
                token = lexer.get_next_token();
                std::cout << "Token: (" << token.type << ", " << token.value
                          << ")" << std::endl;

                // 防止无限循环
                if (token.type == "EOF") break;

            } while (true);
        } catch (const std::exception &e) {
            std::cout << "Uncaught exception: " << e.what() << std::endl;
        }
        std::cout << "---------------------------" << std::endl;
    }
}

// 测试语法分析器
void test_parser() {
    // std::string input = "a := 3 + 5 * (2 - 8) / 4;";
    // std::string input = "(a + 15 * b";
    // std::string input = "a + * b";
    std::vector<std::pair<std::string, std::vector<Token>>> test_cases = {
        // 合法的语法结构
        {"Valid: if-then-else statement",
            {{"ifsym", "if"},
                {"ident", "x"},
                {"gtr", ">"},
                {"number", "0"},
                {"thensym", "then"},
                {"ident", "y"},
                {"becomes", ":="},
                {"number", "1"},
                {"elsesym", "else"},
                {"ident", "y"},
                {"becomes", ":="},
                {"minus", "-"},
                {"number", "1"},
                {"semicolon", ";"},
                {"EOF", ""}}},

        // 非法的语法结构
        {"Invalid: Missing semicolon",
            {{"repeatsym", "repeat"},
                {"ident", "a"},
                {"becomes", ":="},
                {"ident", "a"},
                {"minus", "-"},
                {"number", "1"},
                {"untilsym", "until"},
                {"ident", "a"},
                {"eql", "="},
                {"number", "0"},
                {"EOF", ""}}},

        {"Invalid: Unmatched parentheses",
            {{"beginsym", "begin"},
                {"ident", "x"},
                {"becomes", ":="},
                {"lparen", "("},
                {"ident", "y"},
                {"plus", "+"},
                {"ident", "z"},
                {"semicolon", ";"},
                {"endsym", "end"},
                {"EOF", ""}}},
        {"Valid: Call function",
            {{"beginsym", "begin"},
                {"callsym", "call"},
                {"ident", "square"},
                {"lparen", "("},
                {"ident", "x"},
                {"comma", ","},
                {"ident", "y"},
                {"rparen", ")"},
                {"semicolon", ";"},
                {"endsym", "end"},
                {"EOF", ""}}},
    };
    for (auto &test_case : test_cases) {
        std::cout << "Testing case: " << test_case.first << std::endl;

        try {
            Lexer lexer("");
            lexer.setTokens(test_case.second);
            Parser parser(lexer.tokens);
            parser.parse();  // 调用解析器的解析函数
            std::cout << "Parsing completed successfully." << std::endl;
        } catch (const std::exception &e) {
            std::cerr << "Parsing error: " << e.what() << std::endl;
        }
        std::cout << "----------------------------------------" << std::endl;
    }
}

int main(int argc, char *argv[]) {
    // test_lexer_errors();
    // test_parser();
    // test_semantic_analyzer();
    test_code_generator();
    return 0;
}