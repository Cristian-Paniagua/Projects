#pragma once
#include "Animation.h"
#include "Burger.h"
#include "EntityManager.h"
#include "BaseCounter.h"
class Player: public Entity{

    private:
        int speed = 5;
        string facing = "right";
        Animation *chefAnim;
        Burger *burger;
        EntityManager* entityManager;
        double priceBurger=0;
        bool addedIngredient= false;

    public:
        Player(int x, int y, int width, int height, ofImage sprite, EntityManager* em);
        void tick();
        void render();
        void keyPressed(int);
        void keyReleased(int);
        void mousePressed(int, int, int);
        void setFacing(string);
        BaseCounter* getActiveCounter();
        Burger* getBurger(){ return burger;
        }
        double getBurgerPrice();
        void resetPrice();
        bool iAddedIngredient(){ return addedIngredient;}
        void setAddedIngredient(bool i) {this->addedIngredient= i;}
};