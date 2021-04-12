
#include "util.h"
#include "implementation.h"

//初始化随机数种子
void Util::initRandSeed(void)
{
    srand(static_cast<unsigned int>(time(nullptr)));
    rand();
    rand();
}

//生成随机数
int Util::randomize(int max)
{
    int number = rand() % max;

    return number;
}

int Util::getFlyTime(struct timeval lasttime, struct timeval currenttime)
{
    int flytime = currenttime.tv_sec*1000+currenttime.tv_usec/1000
            - (lasttime.tv_sec*1000+lasttime.tv_usec/1000);

    return flytime;
}

int Util::isTimeArrived(struct timeval lasttime, struct timeval currenttime, int settime)
{
    if(getFlyTime(lasttime, currenttime) > settime)
    {
        return true;
    }
    else
    {
        return false;
    }
}


int Util::checkDirection(GridLocation current, GridLocation next)
{
    if(next.x - current.x > 0)
        return RIGHT;
    else if(next.x - current.x < 0)
        return LEFT;
    else if(next.y - current.y > 0)
        return  DOWN;
    else if(next.y - current.y < 0)
        return UP;

    return ERROR;
}

GridLocation Util::chooseShortestWay(SquareGrid grid, GridLocation snakeHead,
                        std::unordered_map<GridLocation, double> cost_so_far)
{

    int min = INT_MAX;
    GridLocation nextMove{-1, -1};
    for(GridLocation next: grid.neighbors(snakeHead))
    {
        if(cost_so_far.find(next) != cost_so_far.end() && min > cost_so_far[next])
        {
            min = static_cast<int>(cost_so_far[next]);
            nextMove = next;
        }
    }

    return nextMove;
}

GridLocation Util::chooseLongestWay(SquareGrid grid, GridLocation snakeHead,
                       std::unordered_map<GridLocation, double> cost_so_far)
{
    int max = -INT_MAX;
    GridLocation nextMove{-1, -1};
    for(GridLocation next: grid.neighbors(snakeHead))
    {
        if(cost_so_far.find(next) != cost_so_far.end() && max < cost_so_far[next])
        {
            max = static_cast<int>(cost_so_far[next]);
            nextMove = next;
        }
    }

    return nextMove;
}
