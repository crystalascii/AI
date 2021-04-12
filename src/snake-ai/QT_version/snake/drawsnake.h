#ifndef DRAWSNAKE_H
#define DRAWSNAKE_H
#include "implementation.h"


class DrawSnake:public QWidget
{
    Q_OBJECT
public:
    DrawSnake();
    void updateSnakeAndFood(GridLocation point, deque<GridLocation> deque);

protected:
    void paintEvent(QPaintEvent *event);
private:
    void drawBackGround(QPainter &painter);
    void drawMargin(QPainter &painter);
    void drawSnakeBody(QPainter &painter);
    void drawFood(QPainter &painter);
private:
    GridLocation food;
    deque<GridLocation> deq;
};

#endif // DRAWSNAKE_H
