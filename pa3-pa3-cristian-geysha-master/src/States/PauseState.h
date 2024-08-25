#pragma once

#include "State.h"
#include "ofMain.h"
#include "ofEvents.h"

class PauseState : public State {

public:
    PauseState();
    ~PauseState();
    void reset();
    void update();
    void draw();
    void keyPressed(int key);
    void mousePressed(int x, int y, int button);

    ofRectangle ContinueButton;

};