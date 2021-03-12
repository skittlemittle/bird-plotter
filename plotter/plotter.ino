// reads lines over serial and draws them.
// skittlemittle 2021

#include "queue.hpp"

struct point {
    float x = 0.0f;
    float y = 0.0f;

    point() {}
    point(float _x, float _y) : x(_x), y(_y) {}
    point(const point &p) : x(p.x), y(p.y) {}

    void show()
    {
        Serial.print(x);
        Serial.print(" ");
        Serial.println(y);
    }
};

const int LBUFFERLEN = 20;
FixedQueue<point> lines[LBUFFERLEN];

void setup()
{

    Serial.begin(115200);
    FixedQueue<point> l2 = FixedQueue<point>(4);
    l2.enqueue(point(3.0f, 89.993f));
    l2.enqueue(point(0.4405f, 12.00004f));

    l2.dequeue().show();
    l2.dequeue().show();

    Serial.println("LL");
    DynamicQueue<point> linked;
    linked.enqueue(point(9.0f, 9.0f));
    linked.enqueue(point(4.2f, 6.0f));
    linked.enqueue(point(88.0f, 0.93f));

    linked.dequeue().show();
    linked.dequeue().show();
    linked.dequeue().show();
    linked.dequeue().show();
    linked.dequeue().show();
}

void serialEvent()
{
    if (Serial.available()) {
    }
}

void loop() {}
