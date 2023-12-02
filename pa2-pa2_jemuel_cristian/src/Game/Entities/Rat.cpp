#include "Rat.h"

Rat::Rat(int x, int y, int width, int height, ofImage sprite, EntityManager* em) : Entity(x, y, width, height, sprite){
     
    vector<ofImage> ratAnimframes;
    ofImage temp;
    temp.cropFrom(sprite, 0,74,70,35);
    ratAnimframes.push_back(temp);
    temp.cropFrom(sprite, 212,133,70,35);
    ratAnimframes.push_back(temp);
    
    this->ratAnim = new Animation(50, ratAnimframes);
    this->entityManager = em;
}

void Rat::tick(){
    ratAnim->tick();
    if(facing == "left"){
        x-=speed;
    }else if(facing == "right"){
        x+=speed;
    }
    if(x <= 0){
        facing = "right";
    }else if(x + width >= ofGetWidth()){
        facing = "left";
    }

}

void Rat::render(){
    ofSetColor(256, 256, 256);
    ofImage currentFrame = ratAnim->getCurrentFrame();
    if (facing == "left") {
        currentFrame.mirror(false, true);
    }
    currentFrame.draw(x, y + 70, width, height);
}


void Rat::keyPressed(int key){

    if(key==OF_KEY_RIGHT){
        if(facing=="left"){
            facing="right";
        }
    }
    else if(key==OF_KEY_LEFT){
        if(facing=="right"){
            facing="left";
        }
    }
    
}

void Rat::setFacing(string facing){ this->facing = facing; }