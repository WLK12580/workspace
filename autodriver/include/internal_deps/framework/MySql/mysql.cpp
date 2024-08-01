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

bool CMySql::selectFromTable(const std::string &tableName, const std::string &filterFiledName,
                             const std::string &whereData) {
  std::string filterFiled = "";
  std::string whereDataValue = "";
  if (tableName.empty()) {
    std::cout << "tableName is empty\n";
    return false;
  }
  if (filterFiledName.empty()) {
    filterFiled = "*";
  } else {
    filterFiled = filterFiledName;
  }

  if (whereData.empty()) {
    whereDataValue = "";
  } else {
    whereDataValue = whereData;
  }
  std::string queryStr = "select " + filterFiled + " from " + tableName + " " + whereDataValue;
  std::cout << "queryStr=" << queryStr << "\n";
  if (mysql_query(getMySql(), queryStr.c_str())) {
    std::cout << "查询失败" << std::endl;
    return false;
  }
  getQueryData(getMySql());
  return true;
}

bool CMySql::selectFromTable(const std::string &tableName,
                             std::unordered_map<std::string, std::tuple<dataType, std::string>> &selectData,
                             std::unordered_map<std::string, std::tuple<dataType, std::string>> &whereData) {
  // tableName:表名 selectData:查询的字段 whereData:条件

  return true;
}

void CMySql::getQueryData(MYSQL *mysql) {
  MYSQL_RES *res = mysql_store_result(mysql);
  MYSQL_FIELD *field = mysql_fetch_field(res);  // 获取字段名
  int field_count = mysql_num_fields(res);      // 获取字段个数
  for (int i = 0; i < field_count; i++) {
    std::cout << field[i].name << "   \t";
  }
  std::cout << std::endl;
  MYSQL_ROW row;
  while (row = mysql_fetch_row(res)) {
    for (int i = 0; i < field_count; i++) {
      std::cout << row[i] << "  \t";
    }
    std::cout << std::endl;
  }
  std::cout << std::endl;
}

// void CMySql::toJson(const std::map<int,std::unordered_map<std::string,std::tuple<dataType,std::string>>>& queryData,rapidjson::Document& document){
//   //int:行号 unordered_map<string:字段名,tuple<dataType:数据类型,string:数据值>>
//   if(queryData.empty()){
//     std::cout<<"queryData is empty\n";
//     return ;
//   }
//   rapidjson::Document doc;
//   doc.SetObject();
//   rapidjson::Document::AllocatorType& allocator = doc.GetAllocator();
//   //创建数组
//   rapidjson::Value array(rapidjson::kArrayType);
//   std::string id;
//   rapidjson::Value object(rapidjson::kObjectType);
//   for(auto beginIter=queryData.begin(),endIter=queryData.end();beginIter!=endIter;++beginIter){
//     auto filedBegin=beginIter->second.begin();
//     auto filedEnd=beginIter->second.end();
//     id=std::to_string(beginIter->first);
//     object.AddMember("id",id.c_str(),allocator);
//     while(filedBegin!=filedEnd){
//       std::string filedKey=filedBegin->first;
//       std::string filedValue=std::get<1>(filedBegin->second);
//       object.AddMember(filedKey.c_str(),filedValue.c_str(),allocator);
//       filedBegin++;
//     }
//     array.PushBack(object,allocator);
//     object.Clear();
//   }
//   doc.AddMember(id,array,allocator);
//   document.Swap(doc);
// }