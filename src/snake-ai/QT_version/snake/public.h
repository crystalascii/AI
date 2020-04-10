#ifndef PUBLIC_H
#define PUBLIC_H

#include <QWidget>
#include <QPainter>
#include <QDebug>
#include <QKeyEvent>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>
#include <QThread>
#include <deque>
#include <unordered_map>

#include <iostream>
#include <iomanip>
#include <unordered_map>
#include <unordered_set>
#include <array>
#include <vector>
#include <utility>
#include <queue>
#include <tuple>
#include <algorithm>
#include <cstdlib>


using namespace  std;


typedef struct
{
    int x;
    int y;
}   Point;

struct GridLocation {
  int x, y;
};

typedef  enum
{
    RIGHT = 0X01,
    LEFT  = 0X02,
    UP    = 0X03,
    DOWN  = 0X04,
    ERROR = 0xFF
} DIRECTION;



#define EASY 500
#define MEDIUM 250
#define DIFFICULT 100
#define VERY_DIFFICULT 15

#define STANDARD_WIDTH 600
#define STANDARD_HEIGHT 600
#define STANDARD_MARGIN 30
#define SNAKE_WIDTH 30



#endif // PUBLIC_H
