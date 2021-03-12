#ifndef QUEUE_H
#define QUEUE_H

#include <string.h>

/*
 * Fixed size Queue
 * NOTE: making a queue of queues will go badly
 */
template <class T> class FixedQueue {
  public:
    /* qSize: number of things in queue */
    FixedQueue(int qSize)
    {
        q = new T[qSize];
        qlen = qSize;
        size = 0;
        index = 0;
    }

    FixedQueue() {} // hmmmm danger

    ~FixedQueue()
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

  public:
    void enqueue(const T &it);
    T dequeue();
    bool isEmpty() { return size == 0; }
};

template <typename T> void FixedQueue<T>::enqueue(const T &it)
{
    if (size + index >= qlen) {
        Serial.println("WARN: queue full not adding this");
    }
    else {
        q[size + index] = it;
        size++;
    }
}

template <typename T> T FixedQueue<T>::dequeue()
{
    if (size == 0)
        Serial.println("ERR: cannot dequeue an empty queue");

    T ret = q[index];
    delete &q[index];
    index++;
    size--;
    return ret;
}

/*
 * Linked list based dynamic size queue.
 */

template <typename T> class DynamicQueue {
  public:
    DynamicQueue() : first(NULL), last(NULL) {}

  private:
    struct Node {
        T val;
        struct Node *next;
    };
    Node *first;
    Node *last;

  public:
    void enqueue(const T &it);
    T dequeue();
    bool isEmpty() { return first == NULL; }
};

template <typename T> void DynamicQueue<T>::enqueue(const T &it)
{
    Node *oldLast = last;
    last = new Node;
    last->val = it;
    last->next = nullptr;

    if (isEmpty())
        first = last;
    else
        oldLast->next = last;
}

template <typename T> T DynamicQueue<T>::dequeue()
{
    if (isEmpty()) {
        Serial.println("ERR: queue empty");
    }
    else {
        T ret = first->val;
        first = first->next;
        if (isEmpty())
            last = NULL;
        return ret;
    }
}
#endif
