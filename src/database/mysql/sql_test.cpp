#include <mysql/mysql.h>
#include "Singleton.hpp"

#include <iostream>
int main() {
  MYSQL mysql;
  mysql_init(&mysql);
  mysql_options(&mysql, MYSQL_SET_CHARSET_NAME, "utf8");
  if (!mysql_real_connect(&mysql, "192.168.1.16", "root", "erjk", "henan", 3306, NULL, 0)) {
    std::cout <<"sql_errno="<<mysql_errno(&mysql)<<std::endl;
    return -1;
  }
  std::cout << "sql connect successed!" << std::endl;

  std::string query_str="select * from zhoukou";

  std::string insert_str="insert into zhoukou (Date,District_County,Town,Community,Amount,Price) values('2021-12-25','郸城','南区','蔡庄',200,3);";

  if(mysql_query(&mysql,insert_str.c_str())){
    printf("error:%s\n", mysql_error(&mysql));
    perror("insert error");
  }



  if(mysql_query(&mysql,query_str.c_str())){
    std::cout<<"查询失败"<<std::endl;
    return -1;
  }
  std::cout<<"查询成功"<<std::endl;
  MYSQL_ROW row;
  MYSQL_RES* res=mysql_store_result(&mysql);
  MYSQL_FIELD *field=mysql_fetch_field(res);
  int field_count=mysql_num_fields(res);
  for(int i=0;i<field_count;i++){
    std::cout<<field[i].name<<"\t";
  }
  std::cout<<std::endl;
  while(row=mysql_fetch_row(res)){
    for(int i=0;i<field_count;i++){
        std::cout<<row[i]<<"\t";
    }
    std::cout<<std::endl;
  }

  return 0;
}
