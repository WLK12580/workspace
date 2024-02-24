
#include <functional>
#include <iostream>
#include <memory>
#include <mutex>
#include <thread>

namespace AUTOCAR {
template <typename T>
class Singleton {
 public:
  static T& Instance() { return *instanceptr_; }

 public:
  Singleton(){};
  virtual ~Singleton(){};
  Singleton(const Singleton&) = delete;
  Singleton& operator=(const Singleton&) = delete;

 private:
  static std::unique_ptr<T> instanceptr_;
};
template <typename T>
std::unique_ptr<T> Singleton<T>::instanceptr_ = std::make_unique<T>();
}  // namespace AUTOCAR
