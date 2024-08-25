#include "PauseState.h"

//--------------------------------------------------------------
PauseState::PauseState() {

}   
//--------------------------------------------------------------
PauseState::~PauseState() {

}
//--------------------------------------------------------------
void PauseState::reset() {
    setFinished(false);
    setNextState("");
    return;
}
//--------------------------------------------------------------
void PauseState::update() {
}
//--------------------------------------------------------------
void PauseState::draw() {
    ofSetColor(ofColor::black);
    ofDrawRectangle(0,0,ofGetWidth(),ofGetHeight());
    ofSetColor(ofColor::white);
    string text = "Pause";
    ofDrawBitmapString(text, ofGetWidth()/2-8*text.length()/2, ofGetHeight()/2-11);
    ofNoFill();
    ContinueButton.set(ofGetWidth()/3, ofGetHeight()/3, ofGetWidth()/3, ofGetHeight()/3);
    ofDrawRectangle(ContinueButton);
    return;
}
//--------------------------------------------------------------
void PauseState::keyPressed(int key) {
    if (key == 'p') {
        setNextState("Continue");
        setFinished(true);
        return;
    }
}

void PauseState::mousePressed(int x, int y, int button) {
    if (ContinueButton.inside(x,y) and button == 0){
        setNextState("Continue");
        setFinished(true);
        return;
    }

}