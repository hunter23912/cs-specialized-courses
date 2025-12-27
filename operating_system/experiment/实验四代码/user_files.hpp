#pragma once

#include <iostream>
#include <cstring>
#include <unordered_map>
#include <vector>
using namespace std;

struct File
{
    string name;
    string content;
    int size;
    string permission; // 111表示可读可写可执行 rwx
    bool isopen;       // 文件是否被打开
};

class User // 用户文件表
{
public:
    string name;
    unordered_map<string, File> filelist;

    // 创建文件
    void createFile(string &filename, string &filecontent, string &PERMISSION)
    {
        auto it = filelist.find(filename);
        if (it != filelist.end())
        {
            cout << "ERROR: FILE ALREADY EXISTS!" << endl;
            return;
        }
        int filesize = filecontent.size();
        filelist[filename] = File{filename, filecontent, filesize, PERMISSION, false};
        cout << "CREATE SUCCESS!" << endl;
    }

    // 打开文件
    void openFile(string &filename)
    {
        auto it = filelist.find(filename);
        if (it == filelist.end())
        {
            cout << "[ERROR]: FILE NOT FOUND!" << endl;
            return;
        }
        it->second.isopen = true;
        cout << "OPEN SUCCESS!" << endl;
    }

    // 关闭文件
    void closeFile(string &filename)
    {
        auto it = filelist.find(filename);
        if (it == filelist.end())
        {
            cout << "[ERROR]: FILE NOT FOUND!" << endl;
            return;
        }
        it->second.isopen = false;
        cout << "CLOSE SUCCESS!" << endl;
    }

    // 读文件
    void readFile(string &filename)
    {
        auto it = filelist.find(filename);
        if (it == filelist.end())
        {
            cout << "[ERROR]: FILE NOT FOUND!" << endl;
            return;
        }
        it->second.isopen = true;
        if (it->second.permission[0] != '1')
        {
            cout << "[ERROR]: PERMISSION DENIED!" << endl;
            return;
        }
        cout << "FILE CONTENT: " << it->second.content << endl;
    }

    // 写文件
    void writeFile(string &filename, string &filecontent)
    {
        auto it = filelist.find(filename);
        if (it == filelist.end())
        {
            cout << "[ERROR]: FILE NOT FOUND!" << endl;
            return;
        }
        if (it->second.isopen == false)
        {
            cout << "[ERROR]: FILE NOT OPEN!" << endl;
            return;
        }
        if (it->second.permission[1] != '1')
        {
            cout << "[ERROR]: PERMISSION DENIED!" << endl;
            return;
        }
        it->second.content = filecontent;
        cout << "WRITEN SUCCESS!" << endl;
    }

    // 删除文件
    void deleteFile(string &filename)
    {
        auto it = filelist.find(filename);
        if (it == filelist.end())
        {
            cout << "[ERROR]: FILE NOT FOUND!" << endl;
            return;
        }
        if (it->second.isopen == true)
        {
            cout << "[ERROR]: FILE IS OPEN, PLEASE CLOSE IT FIRST!" << endl;
            return;
        }
        filelist.erase(it);
        cout << "DELETE SUCCESS!" << endl;
    }

    // 修改文件权限
    void changePermission(string &filename, string &permission)
    {
        auto it = filelist.find(filename);
        if (it == filelist.end())
        {
            cout << "[ERROR]: FILE NOT FOUND!" << endl;
            return;
        }
        it->second.permission = permission;
        cout << "CHANGE PERMISSION SUCCESS!" << endl;
    }

    // 读取文件列表
    void showFileList()
    {
        if (filelist.empty())
        {
            cout << "[ERROR]: FILE LIST IS EMPTY!" << endl;
            return;
        }
        printf("%-12s%-15s%-5s\n", "FILE NAME", "PERMISSION", "SIZE");
        for (auto &file : filelist)
        {
            printf("%-12s%-15s%-5d\n", file.second.name.c_str(), file.second.permission.c_str(), file.second.size);
        }
        cout << endl;
    }
};
