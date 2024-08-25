#pragma once
#include "Entity.h"

class StaticEntity : public Entity {

    public:

        StaticEntity(float x, float y, float width, float height) : Entity(x, y, width, height) {
        

        }

        void draw();

};

