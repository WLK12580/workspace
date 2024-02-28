#include "mysql.hpp"
using namespace AUTOCAR::DataBase;
int main(){
    CMySql mysql;
    mysql.initConfig("127.0.0.1","root","@Wlk210575","test_db",3306);
    std::cout<<"connect_database_result="<<mysql.connect()<<std::endl;
    std::string tableName="user";
    std::unordered_map<std::string,std::string> map;
    map.emplace("username","xiaosun");
    map.emplace("passwd","986532");
    map.emplace("birthdate","1993-08-21");
    std::cout<<"insertSuccessed="<<mysql.insertToTable(tableName,map)<<"\n";

    return 0;
}