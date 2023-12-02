#include "WinState.h"

WinState::WinState(){
	string text = "Next Day";
	restartButton = new Button(ofGetWidth()/2 - text.length()*8, ofGetHeight()/2 - text.length()*11, 64, 50, "Next Day");
}
void WinState::tick() {
	restartButton->tick();
	if(restartButton->wasPressed()){
		setNextState("Game");
		setFinished(true);

	}
}
void WinState::render() {
	ofSetBackgroundColor(230, 230, 250);
	restartButton->render();
}

void WinState::keyPressed(int key){
	
}

void WinState::mousePressed(int x, int y, int button){
	restartButton->mousePressed(x, y);
}

void WinState::reset(){
	setFinished(false);
	setNextState("");
	restartButton->reset();
}