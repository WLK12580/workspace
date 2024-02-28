#pragma once

#include <fastrtps/attributes/PublisherAttributes.h>
#include <fastrtps/publisher/PublisherListener.h>

#include "fastrtps/fastrtps_fwd.h"
#include "helloWorldFastDDS.h"
#include "helloWorldFastDDSPubSubTypes.h"

class helloWorldPublisher {
 public:
  helloWorldPublisher();
  virtual ~helloWorldPublisher();
  bool init();
  bool publish(bool waitForListen = true);
  void run(uint32_t number, uint32_t sleep);

 private:
  helloWorld m_hello;
  eprosima::fastrtps::Participant *m_participant;
  eprosima::fastrtps::Publisher *m_publisher;
  bool stop;
};
