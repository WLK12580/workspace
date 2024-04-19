#include <mqtt/async_client.h>
#include <mqtt/message.h>

#include <iostream>
#include <thread>

class MQTTCallback : public virtual mqtt::callback {
 public:
  void connectLose(const std::string &cause) { std::cout << "connectLose=" << cause << std::endl; }
  void publish(std::string topic, std::string payload);
};

int main() {
  const std::string ADDRESS("mqtt://172.17.59.119:1883");
  const std::string CLIENTID("paho_cpp_async_publish");
  mqtt::async_client client(ADDRESS, CLIENTID);
  MQTTCallback mqttClient;
  client.set_callback(mqttClient);
  mqtt::connect_options connOpts;
  connOpts.set_keep_alive_interval(20);
  connOpts.set_clean_session(true);
  mqtt::token_ptr conntok = client.connect(connOpts);
  conntok->wait();
  std::cout << "connect success" << std::endl;

  const std::string mqttTopic = "mqttTopic";
  const std::string mqttPayload = "hello,mqtt";
  mqtt::message_ptr pubmsg = mqtt::make_message(mqttTopic, mqttPayload);
  pubmsg->set_qos(1);
  while (1) {
    client.publish(pubmsg)->wait();
    std::cout << "publish success" << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(1));
  }
  std::cout << "disconnect success" << std::endl;
  return 0;
}