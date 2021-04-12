#ifndef RUNSNAKE_H
#define RUNSNAKE_H
#include "implementation.h"

class RunSnake:public QThread
{
    Q_OBJECT
public:
    RunSnake();
    void run();
    void setDirection(int dir);
    GridLocation getFoodPosition();
    deque<GridLocation> getSnakePosition();
private:
    void initSnakeAndFood();        //初始化蛇和食物
    void moveSnake();               //移动蛇
    void feedFood();                //喂食物
    int detectCollision();     //检测是否发生碰撞
    int checkSnakePathValid();
    int followTail();
    int anyPossibleMove();
    void AI();                  //人工智能，电脑自动玩,采用A*算法
    int getLevel();

    SquareGrid makeDiagram(deque<GridLocation> deq);
    SquareGrid makeDiagram1(deque<GridLocation> deq);
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

#endif // RUNSNAKE_H
