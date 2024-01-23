#include "mysql.hpp"

using namespace AUTOCAR::DataBase;

CMySql::CMySql() { if (mysql_ == nullptr) { mysql_ = mysql_init(nullptr); } }

CMySql::~CMySql() { if (mysql_ != nullptr) { mysql_ = nullptr; } }

void CMySql::initConfig(const std::string &host, const std::string &user, const std::string &passwd,
                 const std::string &dataBase, unsigned int port){
   setHost(host);
   setUser(user);
   setPasswd(passwd);
   setDB(dataBase);
   setPort(port);
}
bool CMySql::connect() {
  if (!mysql_real_connect(mysql_, getHost().c_str(), getUser().c_str(), getPasswd().c_str(), getDatabase().c_str(), getPort(), nullptr, 0)) {
    std::cout << "connect database failed\n";
    return false;
  }
  return true;
}
