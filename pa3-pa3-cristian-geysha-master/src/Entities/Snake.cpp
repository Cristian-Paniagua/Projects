#include "Snake.h"
#include "ofMain.h"

Snake::Snake(int segmentSize, int boardSizeW, int boardSizeH) {
    body.push_back({8, 9});
    body.push_back({9, 9});
    body.push_back({10, 9});
    body.push_back({11, 9});
    this->direction = LEFT;
    this->crashed = false;
    this->segmentSize = segmentSize;
    this->boardSizeWidth = boardSizeW;
    this->boardSizeHeight = boardSizeH;
}

Snake::~Snake() {
    // TODO Auto-generated destructor stub
}

void Snake::update() {
    vector<int> oldHead = this->getHead();   
    switch(this->direction) {
        case LEFT: {
            this->body[0][0] -= 1;
            break;
        }
        case DOWN: {
            this->body[0][1] += 1;
            break;
        }
        case RIGHT: {
            this->body[0][0] += 1;
            break;
        }
        case UP: {
            this->body[0][1] -= 1;      
            break;
        }
        case NONE: {
            // Stop moving
            break;
        }
    }

    if(oldHead[0] == -1 || oldHead[0] == boardSizeWidth || oldHead[1] == -1 || oldHead[1] == boardSizeHeight) {
        if(!godModeActive) {
            crashed = true;
        }       
        return;
    }

    if(this->direction != NONE) {
        
        int prevX = oldHead[0];
        int prevY = oldHead[1];
        for (int i = 1; i < this->body.size(); i++) {
            int currX = this->body[i][0];
            int currY = this->body[i][1];
            this->body[i][0] = prevX;
            this->body[i][1] = prevY;
            prevX = currX;
            prevY = currY;
        }
    }

    checkSelfCrash();
}

void Snake::draw() {
    for (int i = 0; i < body.size(); i++) {
        int curX = this->body[i][0];
        int curY = this->body[i][1];
        int HeadX = this->body[0][0];
        int HeadY = this->body[0][1];
        ofSetColor(ofColor::green);
        ofDrawRectangle(curX * segmentSize, curY * segmentSize, segmentSize, segmentSize);
        ofSetColor(ofColor::lawnGreen);
        ofDrawRectangle(HeadX*segmentSize, HeadY*segmentSize, segmentSize, segmentSize);
    }
}

void Snake::changeDirection(Direction d) {

    if(this->direction == LEFT and d == RIGHT)
        return;
    if(this->direction == RIGHT and d == LEFT) 
        return;
    if(this->direction == UP and d == DOWN) 
        return;
    if(this->direction == DOWN and d == UP)
        return;
    
    this->direction = d;
}

void Snake::checkSelfCrash() {
    std::vector<std::vector<int>> snake = this->body;
    vector<int> head = snake[0];
    for(int i = 1; i < snake.size(); i++) {
        if(head[0] == snake[i][0] and head[1] == snake[i][1]) {
            if(!godModeActive) {  
                crashed = true;
            }
            return;
        }
    }
}

void Snake::grow() {
    vector<int> newSegment = this->getTail();
    this->body.push_back(newSegment);
    score += 10;
}

void Snake::undo() {
    if(body.size() > 2) {
        body.pop_back();
        score -= 10;
    }
}