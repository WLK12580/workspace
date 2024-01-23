#include "mysql.hpp"
using namespace AUTOCAR::DataBase;
int main(){
    MySql mysql;
    std::cout<<"connect_database_result="<<mysql.connect("127.0.0.1","root","@Wlk210575","test_db",3306)<<std::endl;;

    return 0;
}