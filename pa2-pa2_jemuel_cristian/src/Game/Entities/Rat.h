#pragma once

#include "Entity.h"
#include "Animation.h"
#include "EntityManager.h"

class Rat: public Entity{

    private:
        int speed = 5;
        string facing = "right";
        Animation *ratAnim;
        EntityManager* entityManager;

    public:
        Rat(int x, int y, int width, int height, ofImage sprite, EntityManager* em);
        void tick();
        void render();
        void keyPressed(int);
        void keyReleased(int);
        void mousePressed(int, int, int);
        void setFacing(string);
};