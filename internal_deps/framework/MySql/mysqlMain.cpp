#include "mysql.hpp"
using namespace AUTOCAR::DataBase;
int main(){
    CMySql mysql;
    mysql.initConfig("127.0.0.1","root","@Wlk210575","test_db",3306);
    std::cout<<"connect_database_result="<<mysql.connect()<<std::endl;;

    return 0;
}