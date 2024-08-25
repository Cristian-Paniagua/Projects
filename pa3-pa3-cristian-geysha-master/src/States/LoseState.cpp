#include "LoseState.h"
//--------------------------------------------------------------
LoseState::LoseState() {
}  
//--------------------------------------------------------------
LoseState::~LoseState() {
}
//--------------------------------------------------------------
void LoseState::reset() {
    setFinished(false);
    setNextState("");
    return;
}
//--------------------------------------------------------------
void LoseState::update() {
}
//--------------------------------------------------------------
void LoseState::draw() {
    ofSetColor(ofColor::black);
    ofDrawRectangle(0,0,ofGetWidth(),ofGetHeight());
    ofSetColor(ofColor::white);
    string text = "You Lost!";
    string text2 = "Press any arrow key to play again or press ESC to exit.";
    string text3 = "Score = " + ofToString(finalScore);
    ofDrawBitmapString(text, ofGetWidth()/2-8*text.length()/2, ofGetHeight()/2-11);
    ofDrawBitmapString(text2, ofGetWidth()/2-8*text2.length()/2, ofGetHeight()/2+2);
    ofDrawBitmapString(text3 , ofGetWidth()/2-8*text2.length()/2, ofGetHeight()/3);
    return;
}
//--------------------------------------------------------------
void LoseState::keyPressed(int key) {
    if(key == OF_KEY_LEFT || key == OF_KEY_RIGHT || key == OF_KEY_UP || key == OF_KEY_DOWN) {
        setFinished(true);
        setNextState("GameState");
        return;
    }
    if(key == OF_KEY_ESC) {
        ofExit();
    }
}
//---------------------------------------------------------------
void LoseState::mousePressed(int x, int y, int button){
    
}