#include "StaticEntity.h"

void StaticEntity::draw() {
        
        ofSetColor(ofColor::gray);
        ofDrawRectangle(this->x*this->width , this->y*this->height , this->width , this->height);
}