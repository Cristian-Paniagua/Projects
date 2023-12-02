#include "Client.h"

Client::Client(int x, int y, int width, int height, ofImage sprite, Burger* burger, bool isInspector): Entity(x, y, width, height, sprite){
    this->burger = burger;
    this->isInspector = isInspector;
}
Client::~Client(){
    delete burger;
}
void Client::render(){
    ofSetColor(255, 255, 255);
    burger->render();
    ofSetColor(255, 255 - sum , 255 - sum);
    sprite.draw(x, y, width, height);
    sum += PCP;
    if(nextClient != nullptr){
        nextClient->render();
    }
}

void Client::tick(){
    patience--;
    burger->setY(y);
    if(patience == 0){
        isLeaving = true;
        
    }
    if(nextClient != nullptr){
        nextClient->tick();
    }

}
int Client::getPatience(){
    return patience;
}

int Client::serve(Burger* burger) {
    
    if(burger->burgerEquals(this->burger)) {
        isLeaving = true;
        return burger->getBurgerPrice(burger);
    } else {
        if(this->nextClient != nullptr) {
            return this->nextClient->serve(burger);
        }      
        return 0;
    }
}

