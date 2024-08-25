#pragma once
#include "State.h"
#include "ofMain.h"
class LoseState : public State {
public:
    LoseState();
    ~LoseState();
    void reset();
    void update();
    void draw();
    void keyPressed(int key);
    void mousePressed(int x, int y, int button);

    int finalScore;

};
