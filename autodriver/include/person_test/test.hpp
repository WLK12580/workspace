#include "../internal_deps/Singleton/Singleton.hpp"
using namespace AUTOCAR;
class subclass : public Singleton<subclass> {
  friend class Singleton<subclass>;

 public:
  void setName(const std::string &name) { name_ = name; }
  std::string getName() { return name_; }

 private:
  std::string name_ = "";
};

class subclass_ : public Singleton<subclass_> {
  friend class Singleton<subclass_>;

 public:
  void setName(const std::string &name) { name_ = name; }
  std::string getName() { return name_; }

 private:
  std::string name_ = "";
};