#ifndef RUNSNAKE_H
#define RUNSNAKE_H
#include "implementation.h"

class RunSnake:public QThread
{
    Q_OBJECT
public:
    RunSnake();
    void run();
    void initSnakeAndFood();        //初始化蛇和食物
    void moveSnake();               //移动蛇
    void feedFood();                //喂食物
    void catchKeyboardOperation();  //获取键盘输入，改变移动方向
    void catchMenuOperation();  //根据菜单项选择，设置游戏参数，包括游戏速度，游戏的声音，游戏人工还是AI，
                                //食物是否吃完再喂还是隔一段时间喂一次，重新开始，退出
    int findPointInSnakeBody(GridLocation p, deque<GridLocation> deq);
    void getPointsNotInSnakeBodyAndFood(deque<GridLocation> &deq1);
    int detectCollision();     //检测是否发生碰撞
    int checkSnakePathValid();
    int followTail();
    int anyPossibleMove();
    void AI();                  //人工智能，电脑自动玩,采用A*算法
    void checkWinner();         //检测是否是赢家，必须将整个屏幕填满才算赢
    int getLevel();
    void setDirection(int dir);
    GridLocation getFoodPosition();
    deque<GridLocation> getSnakePosition();
    SquareGrid make_diagram(deque<GridLocation> deq);
    SquareGrid make_diagram1(deque<GridLocation> deq);
    SquareGrid make_diagram2(deque<GridLocation> deq);
protected:

signals:
    void update();

private:
    void moveRight();
    void moveLeft();
    void moveUp();
    void moveDown();

    deque<GridLocation> deq;
    GridLocation food;
    int direction; //right: 0, up:1, left:2, down:3
    int level;  //game level
    int x_max;  //the max x position of the snake
    int y_max;  //the max y position of the snake
};

//初始化随机数种子
void initRandSeed(void);

//生成随机数
int randomize(int min, int max);

#endif // RUNSNAKE_H
