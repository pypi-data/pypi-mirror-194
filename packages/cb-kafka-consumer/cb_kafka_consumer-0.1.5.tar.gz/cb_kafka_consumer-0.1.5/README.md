Yet another kafka consumer!

## Installation

To use the consumer you can add it as a dependency to your project.

#### PIP

```Bash
python -m pip install --user cb-kafka-consumer
```

#### Pipfile

```
[packages]
cb-kafka-consumer = "~=0.1.5"
```

## An example decoder / handler

Make sure to use the right values to initiate ``CBKafkaConsumer``.
It is necessary to pass the right decoder callback to decode the received raw message.
An example json decoder is provided below.

```Python
from cb_kafka_consumer.src.consumer import CBKafkaConsumer, Message
import json
import logging


class MyConsumer:
    def __init__(self):
        self.__consumer = CBKafkaConsumer('127.0.0.1:9092', 'my-group-id', 'my-topic', self.__handler, self.__decoder)
        self.__consumer.start()

    def __handler(self, msg: Message):
        print(msg.get_offset(), msg.msg)
        self.__consumer.commit(msg)

    def __decoder(self, raw_msg: str):
        try:
            return json.loads(raw_msg)
        except ValueError:
            logging.error(f'Message cannot be parsed\n{raw_msg}')
            return None
```

## Commit policy

There are two different approaches dealing with commit policy.

- #### auto_commit=True

You can use ``auto_commit=True`` when initiating the consumer to instruct it to automatically
commit received messages right after they have been handed over to the handler callback. When
using ``auto_commit``, the handler callback is not expected to explicitly call the ``commit``
method of consumer object.

- #### auto_commit=False (default behavior)

If ``auto_commit`` is not specified or set to ``False`` the consumer will only commit messages
right before the item in the sequence where it's not committed *(handling may have probably failed)*.
To further demonstrate this let's assume we the consumer has received messages with the following
offsets:

1, 2, 3, 4, 5

The consumer now hands over the received messages to the handler callback. Now let's say the callback
processes message #1 and #2 successfully and commits these two messages but fails to process #3. Next,
messages #4 and #5 are successfully processed and committed. The consumer will only commit message #1
and #2 and will not commit succeeded messages until ``commit`` is called with message #3 and will
only then move onward.

## Where to start receiving messages from
To control the start point the ``start_from`` argument of constructor can be utilized. It accepts either
``earliest`` or ``latest`` as valid values. 