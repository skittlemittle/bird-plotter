#ifndef QUEUE_H
#define QUEUE_H

#include "Arduino.h"
#include <new>
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
 * Fixed size Queue
 */
template <class T> class Queue {
  public:
    /* qSize: number of points in line*/
    Queue(int qSize)
    {
        q = new T[qSize];
        qlen = qSize;
        size = 0;
        index = 0;
    }

    ~Queue()
    {
        for (int i = 0; i < size; i++)
            delete &q[i];
        delete[] q;
    }

  private:
    T *q = nullptr;
    int qlen;
    int size;
    int index;
    float EMPTY = -1.0f;

  public:
    void enqueue(const T &it);
    T dequeue();
    bool isEmpty() { return size == 0; }
};

template <typename T> void Queue<T>::enqueue(const T &it)
{
    if (size + index >= qlen) {
        Serial.println("WARN: queue full not adding this");
    }
    else {
        q[size + index] = it;
        size++;
    }
}

template <typename T> T Queue<T>::dequeue()
{
    if (size == 0)
        Serial.println("ERR: cannot dequeue an empty queue");

    T ret = q[index];
    delete &q[index];
    index++;
    size--;
    return ret;
}

#endif
