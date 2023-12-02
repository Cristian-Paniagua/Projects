#include "MenuState.h"

MenuState::MenuState() {
	string text = "Start";
	startButton = new Button(ofGetWidth()/2 - text.length()*8, ofGetHeight()/2 - text.length()*11, 64, 50, "Start");
	if(instructions){
		ofSetColor(ofColor::black);
		ofDrawBitmapString("Press 'e' on top of the item to add it to the burger\n Press 's' to serve the burger\n To hide instrcutions press 'i' again", ofGetWidth()-400, 20);
	}else{
		ofSetColor(ofColor::black);
		ofDrawBitmapString("Press 'i' for see instructions", ofGetWidth()-100, 20);
	}
}
void MenuState::tick() {
	startButton->tick();
	if(startButton->wasPressed()){
		setNextState("Game");
		setFinished(true);

	}
}
void MenuState::render() {
	ofSetBackgroundColor(230, 230, 250);
	startButton->render();
}

void MenuState::keyPressed(int key){
	switch(key){
		case 'i':
		if(!instructions)
		instructions= true;
		else
		instructions= false;
	}
}

void MenuState::mousePressed(int x, int y, int button){
	startButton->mousePressed(x, y);
}

void MenuState::reset(){
	setFinished(false);
	setNextState("");
	startButton->reset();
}