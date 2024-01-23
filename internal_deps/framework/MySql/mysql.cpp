#include "mysql.hpp"

using namespace AUTOCAR::DataBase;

MySql::MySql() { if (mysql_ == nullptr) { mysql_ = mysql_init(nullptr); } }

MySql::~MySql() { if (mysql_ != nullptr) { mysql_ = nullptr; } }

bool MySql::connect(const std::string &host, const std::string &user, const std::string &passwd,
                    const std::string &dataBase, unsigned int port) {
  if (!mysql_real_connect(mysql_, host.c_str(), user.c_str(), passwd.c_str(), dataBase.c_str(), port, nullptr, 0)) {
    std::cout << "connect database failed\n";
    return false;
  }
  return true;
}
