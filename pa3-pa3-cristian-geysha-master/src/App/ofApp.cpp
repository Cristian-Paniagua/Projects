#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){

    ofSetWindowTitle("Snake");

    gameState = new GameState();
    menuState = new MenuState();
    loseState = new LoseState();
    pauseState = new PauseState();
    currentState = menuState;

    sound.setVolume(0.5);
    sound.load("music.mp3");
	sound.setLoop(true);
	sound.play();

}

//--------------------------------------------------------------
void ofApp::update(){
    if(currentState->hasFinished()) {
        if(currentState->getNextState() == "GameState") {
            gameState->reset();
            currentState = gameState;
        } 
        else if(currentState->getNextState() == "Continue"){
            gameState->setFinished(false);
            gameState->setNextState("");
            currentState = gameState;
        }
        else if(currentState->getNextState() == "PauseState"){
            pauseState->reset();
            currentState = pauseState;
        }
        else if(currentState->getNextState() == "MenuState") {
            menuState->reset();
            currentState = menuState;
        }
        else if(currentState->getNextState() == "LoseState"){
            loseState->finalScore = gameState->getScore();
            loseState->reset();
            currentState = loseState;
        }
    }
    currentState->update();
}

//--------------------------------------------------------------
void ofApp::draw(){
    currentState->draw();
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
    currentState->keyPressed(key);
}
//--------------------------------------------------------------