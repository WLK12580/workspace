#include "mysql.hpp"
using namespace AUTOCAR::DataBase;
int main(){
    CMySql mysql;
    mysql.initConfig("127.0.0.1","root","@Wlk210575","test_db",3306);
    if(!mysql.connect()){
        std::cout<<"connect error\n";
        return 0;
    }
    std::string tableName="user";
    std::unordered_map<std::string,std::tuple<dataType,std::string>> map;
    std::tuple<dataType,std::string> tupleData;
    tupleData=std::make_tuple(dataType::STRING,"xiaotong");
    map.emplace("username",tupleData);
    tupleData=std::make_tuple(dataType::NUMBER,"31");
    map.emplace("age",tupleData);
    tupleData=std::make_tuple(dataType::STRING,"123456");
    map.emplace("passwd",tupleData);
    tupleData=std::make_tuple(dataType::STRING,"1993-09-19 12:20:06");
    map.emplace("birthdate",tupleData);
    if(mysql.insertToTable(tableName,map)){
        std::cout<<"insertDataSuccessed\n";
    } else{
        std::cout<<"insertDataFailed\n";
    }
    std::string whereData="where age>18";
    std::string filterFiled="username,age";
    mysql.selectFromTable(tableName,"",whereData);

    std::cout<<"\n";

    mysql.selectFromTable(tableName,filterFiled,whereData);
    
    return 0;
}