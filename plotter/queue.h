#ifndef QUEUE_H
#define QUEUE_H

#include "Arduino.h"
#include <string.h>

#define DIMENSION 2 // length of each point array

struct point {
    float x = 0.0f;
    float y = 0.0f;

    point() {}
    point(float _x, float _y) : x(_x), y(_y) {}

    void show()
    {
        Serial.print(x);
        Serial.print(" ");
        Serial.println(y);
    }
};

/*
 * Queue to hold lines
 */
class LineQueue {
  public:
    /* qSize: number of points in line*/
    LineQueue(int qSize)
    {
        q = new point[qSize];
        qlen = qSize;
        size = 0;
        index = 0;
    }
    ~LineQueue() { delete[] q; }

  private:
    point *q = nullptr;
    int qlen;
    int size;
    int index;

  public:
    void enqueue(const point &it);
    point dequeue();
    bool isEmpty() { return size == 0; }
};

void LineQueue::enqueue(const point &it)
{
    if (size + index >= qlen)
        Serial.println("WARN: queue full not adding this");

    q[size + index] = point(it.x, it.y); // you didnt see anything
    size++;
}

point LineQueue::dequeue()
{
    if (size == 0)
        Serial.println("ERR: cannot dequeue an empty queue");

    point ret = q[index];

    q[index].x = -1.0f;
    q[index].y = -1.0f;
    index++;
    size--;
    return ret;
}

#endif
