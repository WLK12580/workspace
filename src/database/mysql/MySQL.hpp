#pragma once

#include <mysql/mysql.h>

#include <iostream>

namespace DataBase::MySQL {
class Mysql {
 public:
  bool connect();

 private:
  MYSQL *mysqlHandle;
  std::string database_;
  std::string username_;
  std::string host_;
  std::string passwd_;
  int port_;
};
}  // namespace DataBase::MySQL