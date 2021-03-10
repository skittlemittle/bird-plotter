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
 * Queue to hold lines as sets of points
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
    ~LineQueue()
    {
        for (int i = 0; i < size; i++)
            delete &q[i];
        delete[] q;
    }

  private:
    point *q = nullptr;
    int qlen;
    int size;
    int index;
    float EMPTY = -1.0f;

  public:
    void enqueue(const point &it);
    point dequeue();
    bool isEmpty() { return size == 0; }
};

void LineQueue::enqueue(const point &it)
{
    if (size + index >= qlen) {
        Serial.println("WARN: queue full not adding this");
    }
    else {
        q[size + index] = it;
        size++;
    }
}

point LineQueue::dequeue()
{
    if (size == 0)
        Serial.println("ERR: cannot dequeue an empty queue");

    point ret = q[index];
    delete &q[index];
    index++;
    size--;
    return ret;
}

#endif
