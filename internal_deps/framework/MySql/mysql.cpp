#include "mysql.hpp"

using namespace AUTOCAR::DataBase;

CMySql::CMySql() { if (mysql_ == nullptr) { MYSQL* mysql = mysql_init(nullptr); 
  setMysql(mysql);
} }

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
  if (!mysql_real_connect(getMySql(), getHost().c_str(), getUser().c_str(), getPasswd().c_str(), getDatabase().c_str(), getPort(), nullptr, 0)) {
    printf("connect:%s\n", mysql_error(getMySql()));
    return false;
  }
  return true;
}
bool CMySql::insertToTable(const std::string &tableName, std::unordered_map<std::string, std::tuple<dataType,std::string>> &insertData) {
  // insertData容器中key存储的是表的字段，value:是对于字段的值,此处是单次插入：由于insertData不允许有重复的key
  std::string filedKey = "";
  std::string insertDataValue = "";
  for (auto beginIter = insertData.begin(), endIter = insertData.end(); beginIter != endIter; ++beginIter) {
    filedKey += beginIter->first + ",";
    if(std::get<0>(beginIter->second) == dataType::NUMBER){
      insertDataValue += std::get<1>(beginIter->second)+ ",";
    }else{
      insertDataValue += "'" + std::get<1>(beginIter->second) + "'" + ",";
    }
  }
  filedKey.erase(filedKey.size() - 1);
  insertDataValue.erase(insertDataValue.size() - 1);
  std::string insertToTable =
      "INSERT INTO " + tableName + " (" + filedKey + ") " + "VALUES" + " (" + insertDataValue + ")";
  if (mysql_query(getMySql(), insertToTable.c_str())) {
    printf("error:%s\n", mysql_error(getMySql()));
    return false;
  }
  return true;
}
