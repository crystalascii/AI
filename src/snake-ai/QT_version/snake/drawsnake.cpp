#include "drawsnake.h"




DrawSnake::DrawSnake()
{
    this->setFixedWidth(STANDARD_WIDTH);
    this->setFixedHeight(STANDARD_HEIGHT);

}

void DrawSnake::updateSnakeAndFood(GridLocation point, deque<GridLocation> deque)
{
    food = point;
    deq = deque;
}

//????????????????????????????????????????????????????????????????????????????????
//有一个疑问，为啥主窗体的坐标不是从（0， 0）开始的，而是从（0， 16）开始的，这个留到后面解决。
//??????????????????????????????????????????????????????????????????????????????????

void DrawSnake::drawBackGround(QPainter &painter)
{
    painter.setBrush(QBrush(Qt::black));
    painter.drawRect(0, 0, width(), height());
}

void DrawSnake::drawMargin(QPainter &painter)
{
    painter.setPen(QPen(Qt::magenta, 2));

    painter.drawRect(QRect(STANDARD_MARGIN, STANDARD_MARGIN, width()-2*STANDARD_MARGIN, height()-2*STANDARD_MARGIN));
}

void DrawSnake::drawSnakeBody(QPainter &painter)
{
    for(deque<GridLocation>::iterator it=deq.begin();it!=deq.end();++it)
    {
        //snake head
        if(it == deq.begin())
        {
            painter.setPen(QPen(Qt::magenta, 1));
            painter.setBrush(QBrush(Qt::yellow));
            QRect rect1(STANDARD_MARGIN+it->x*SNAKE_WIDTH,
                        STANDARD_MARGIN+it->y*SNAKE_WIDTH, SNAKE_WIDTH-2, SNAKE_WIDTH-2);
            painter.drawRoundRect(rect1, 50, 50);

            painter.setPen(QPen(Qt::magenta, 5));
            painter.drawPoint(STANDARD_MARGIN+it->x*SNAKE_WIDTH+SNAKE_WIDTH/2, STANDARD_MARGIN+it->y*SNAKE_WIDTH+SNAKE_WIDTH/2);

            painter.setPen(QPen(Qt::magenta, 1));
            painter.setBrush(QBrush(Qt::green));
        }//snake tail
        else if(it == deq.end()-1)
        {
            QRect rect1(STANDARD_MARGIN+it->x*SNAKE_WIDTH,
                        STANDARD_MARGIN+it->y*SNAKE_WIDTH, SNAKE_WIDTH-2, SNAKE_WIDTH-2);
            painter.drawRoundRect(rect1, 50, 50);

        }//other snake body
        else
        {
            QRect rect1(STANDARD_MARGIN+it->x*SNAKE_WIDTH,
                        STANDARD_MARGIN+it->y*SNAKE_WIDTH, SNAKE_WIDTH-2, SNAKE_WIDTH-2);
            painter.drawRoundRect(rect1);
        }
    }
}

void DrawSnake::drawFood(QPainter &painter)
{
    painter.setBrush(QBrush(Qt::darkRed));
    painter.drawEllipse(STANDARD_MARGIN+food.x*SNAKE_WIDTH,
                        STANDARD_MARGIN+food.y*SNAKE_WIDTH, SNAKE_WIDTH, SNAKE_WIDTH);
}

void DrawSnake::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);

    drawBackGround(painter);
    drawMargin(painter);
    drawSnakeBody(painter);
    drawFood(painter);
}
