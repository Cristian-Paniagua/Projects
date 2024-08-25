#pragma once
#include "ofMain.h"

class Entity {


    public:

        int x, y;
        int width, height;
        
        Entity(int x, int y, int width, int height) {
            this->x = x;
            this->y = y;
            this->width = width;
            this->height = height;
        }
        
        virtual void draw();
        virtual int getX() {return this->x;};
        virtual int getY() {return this->y;};       
};