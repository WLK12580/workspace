#pragma once
#include <mysql/mysql.h>
#include <iostream>
#include <functional>
#include <unordered_map>
#include <map>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/prettywriter.h>
typedef enum class EDataType
{
    NUMBER,
    STRING
} dataType;

namespace AUTOCAR::DataBase {
class CMySql {
 public:
  CMySql();
  ~CMySql();
  bool connect();
  bool insertToTable(const std::string &tableName,std::unordered_map<std::string,std::tuple<dataType,std::string>>& insertData);
  bool selectFromTable(const std::string &tableName,std::unordered_map<std::string,std::tuple<dataType,std::string>>& selectData,
                       std::unordered_map<std::string,std::tuple<dataType,std::string>>& whereData);
  bool selectFromTable(const std::string &tableName,const std::string& filterFiledName="",const std::string& whereData="");


public:
 void initConfig(const std::string &host, const std::string &user, const std::string &passwd,
                 const std::string &dataBase, unsigned int port);

private:
 void getQueryData(MYSQL *mysql);
 void toJson(const std::map<int,std::unordered_map<std::string,std::tuple<dataType,std::string>>>& queryData,rapidjson::Document& document);

private:
 inline void setHost(const std::string &host) { host_ = host; }
 inline void setUser(const std::string &user) { user_ = user; }
 inline void setPasswd(const std::string &passwd) { passwd_ = passwd; }
 inline void setDB(const std::string &database) { dataBase_ = database; }
 inline void setPort(const int &port) { port_ = port; }
 inline std::string getHost() { return host_; }
 inline std::string getUser() { return user_; }
 inline std::string getPasswd() { return passwd_; }
 inline std::string getDatabase() { return dataBase_; }
 inline int getPort() { return port_; }
 inline void setMysql(MYSQL *mysql) { mysql_ = mysql; }
 inline MYSQL *getMySql() { return mysql_; }

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
