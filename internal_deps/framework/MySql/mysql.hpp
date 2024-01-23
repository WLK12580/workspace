#pragma once
#include <mysql/mysql.h>
#include <iostream>
#include <functional>
#include <unordered_map>
typedef enum class EDataType
{
    NUMBER,
    STRING
} dataType;

namespace AUTOCAR::DataBase {
class MySql {
 public:
  MySql();
  ~MySql();
  bool connect(const std::string &host, const std::string &user, const std::string &passwd, const std::string &dataBase,
               unsigned int port);
  bool insertToTable(const std::string &tableName,std::unordered_map<std::string,std::tuple<dataType,std::string>>& insertData);
 private:
  MYSQL *mysql_;
  std::string host_;
  std::string user_;
  std::string passwd_;
  std::string dataBase_;
  unsigned int port_;
  unsigned int timeout_;
  dataType dataType_;
};

}  // namespace AUTOCAR::DataBase