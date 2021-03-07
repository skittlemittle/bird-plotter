// reads lines over serial and draws them.
// skittlemittle

#include "queue.h"

void setup()
{
    Serial.begin(9600); // 115200
    LineQueue lineQueue = LineQueue(4);
    point bruh(2.0f, 4.0f);
    lineQueue.enqueue(bruh);
    point o(4.6f, 7.2f);
    lineQueue.enqueue(o);

    lineQueue.dequeue();
    point p = point(lineQueue.dequeue());
    p.show();
}

void serialEvent()
{
    if (Serial.available()) {
    }
}

void loop() {}
