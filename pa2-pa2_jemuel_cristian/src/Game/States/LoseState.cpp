#include "LoseState.h"

LoseState::LoseState() {
	string text = "Restart";
	restartButton = new Button(ofGetWidth()/2 - text.length()*8, ofGetHeight()/2 - text.length()*11, 64, 50, "Restart");
	ofDrawBitmapString("GAME OVER!", ofGetWidth() / 2, 255);
}
void LoseState::tick() {
	restartButton->tick();
	if(restartButton->wasPressed()){
		setNextState("Game");
		setFinished(true);

	}
}
void LoseState::render() {
	ofSetBackgroundColor(230, 230, 250);
	restartButton->render();
}

void LoseState::keyPressed(int key){
	
}

void LoseState::mousePressed(int x, int y, int button){
	restartButton->mousePressed(x, y);
}

void LoseState::reset(){
	setFinished(false);
	setNextState("");
	restartButton->reset();
}