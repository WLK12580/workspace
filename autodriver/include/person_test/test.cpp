#include"test.hpp"
int main(){
    AUTOCAR::Singleton<subclass>::Instance().setName("xiaoximg");
    std::cout<<AUTOCAR::Singleton<subclass>::Instance().getName()<<std::endl;;
    AUTOCAR::Singleton<subclass_>::Instance().setName("xiaoxinnihao");
    std::cout<<AUTOCAR::Singleton<subclass_>::Instance().getName()<<std::endl;;
    return 0;
}