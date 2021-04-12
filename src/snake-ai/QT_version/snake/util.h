#ifndef UTIL_H_
#define UTIL_H_

#include "public.h"
struct SquareGrid;

class Util
{
  public:

    //初始化随机数种子
    static void initRandSeed(void);

    //生成随机数
    static int randomize(int max);
    static int getFlyTime(struct timeval lasttime, struct timeval currenttime);
    static int isTimeArrived(struct timeval lasttime, struct timeval currenttime, int settime);

    static int checkDirection(GridLocation current, GridLocation next);
    static GridLocation chooseShortestWay(SquareGrid grid, GridLocation snakeHead,
                            std::unordered_map<GridLocation, double> cost_so_far);
    static GridLocation chooseLongestWay(SquareGrid grid, GridLocation snakeHead,
                           std::unordered_map<GridLocation, double> cost_so_far);

};

#endif // UTIL_H
