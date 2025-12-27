#include "user_files.hpp"
using namespace std;

void showMenu()
{
    cout << "==========COMMAND MENU==========" << endl;
    cout << "          [1] CREATE" << endl;
    cout << "          [2] OPEN" << endl;
    cout << "          [3] READ" << endl;
    cout << "          [4] WRITE" << endl;
    cout << "          [5] CLOSE" << endl;
    cout << "          [6] DELETE" << endl;
    cout << "          [7] SHOW FILE LIST" << endl;
    cout << "          [8] CHANGE PERMISSION" << endl;
    cout << "          [q] QUIT" << endl;
}

void test()
{
    unordered_map<string, User> userlist;
    while (true)
    {
        cout << "¡¤ INPUT USER NAME: [";
        for (auto it : userlist)
            cout << it.first << " ";
        cout << "]" << endl;
        cout << "¡¤ ENTER 'q' TO QUIT" << endl;
        cout << "YOUR NAME: ";
        string name;
        cin >> name;
        if (name == "q" || name == "Q")
            break;
        if (userlist.find(name) == userlist.end())
            userlist[name] = User{name};
        else
            cout << "WELCOME BACK!" << endl;
        while (true)
        {
            showMenu();
            string choice;
            cin >> choice;
            if ((choice[0] == 'c' || choice[0] == 'C') && (choice[1] == 'r' || choice[1] == 'R') || choice == "1")
            {
                cout << "FILE NAME: ";
                string filename;
                cin >> filename;
                cout << "FILE CONTENT: ";
                string filecontent;
                getline(cin, filecontent);
                getline(cin, filecontent);
                cout << "FILE PERMISSION (rwx = \"111\"): ";
                string permission;
                cin >> permission;
                userlist[name].createFile(filename, filecontent, permission);
            }
            else if (choice[0] == 'o' || choice[0] == 'O' || choice == "2")
            {
                cout << "FILE NAME: ";
                string filename;
                cin >> filename;
                userlist[name].openFile(filename);
            }
            else if (choice[0] == 'r' || choice[0] == 'R' || choice == "3")
            {
                cout << "FILE NAME: ";
                string filename;
                cin >> filename;
                userlist[name].readFile(filename);
            }
            else if (choice[0] == 'w' || choice[0] == 'W' || choice == "4")
            {
                cout << "FILE NAME: ";
                string filename;
                cin >> filename;
                cout << "FILE CONTENT: ";
                string filecontent;
                getline(cin, filecontent); // ¶ÁÈ¡»»ÐÐ·û
                getline(cin, filecontent);
                userlist[name].writeFile(filename, filecontent);
            }
            else if ((choice[0] == 'c' || choice[0] == 'C') && (choice[1] == 'l' || choice[1] == 'L') || choice == "5")
            {
                cout << "FILE NAME: ";
                string filename;
                cin >> filename;
                userlist[name].closeFile(filename);
            }
            else if (choice[0] == 'd' || choice[0] == 'D' || choice == "6")
            {
                cout << "FILE NAME: ";
                string filename;
                cin >> filename;
                userlist[name].deleteFile(filename);
            }
            else if (choice[0] == 's' || choice[0] == 'S' || choice == "7")
            {
                userlist[name].showFileList();
            }
            else if ((choice[0] == 'c' || choice[0] == 'C') && (choice[1] == 'h' || choice[1] == 'H') || choice == "8")
            {
                cout << "FILE NAME: ";
                string filename;
                cin >> filename;
                cout << "NEW PERMISSION: ";
                string permission;
                cin >> permission;
                userlist[name].changePermission(filename, permission);
            }
            else if (choice[0] == 'q' || choice[0] == 'Q' || choice == "quit" || choice == "QUIT")
            {
                break;
            }
            else
            {
                cout << "INVALID COMMAND!" << endl;
            }
        }
    }
}