#include "GameState.h"

GameState::GameState() {
    this->restaurant = new Restaurant();
}
void GameState::tick() {
	restaurant->tick();
	if(restaurant->ilose()){
	setFinished(true);
	setNextState("Lose");
	restaurant->changetoLoseState();
	this->restaurant=new Restaurant();
	}
	 else if(restaurant->iWin()){
	setFinished(true);
	setNextState("Win");
	restaurant->changetoWinState();
	this->restaurant= new Restaurant();
	}
}
void GameState::render() {
	restaurant->render();
}

void GameState::keyPressed(int key){
	restaurant->keyPressed(key);
}

void GameState::mousePressed(int x, int y, int button){
}

void GameState::keyReleased(int key){
}

void GameState::reset(){
	setFinished(false);
	setNextState("");
}