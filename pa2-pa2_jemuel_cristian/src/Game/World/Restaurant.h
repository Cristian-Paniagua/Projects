//
// Created by joshu on 11/3/2020.
//
#pragma once

#include "BaseCounter.h"
#include "EntityManager.h"
#include "Player.h"
#include "ofMain.h"
#include "Item.h"
#include "Rat.h"

class Restaurant {
    private:
        Player* player;
        Rat* rat;
        EntityManager* entityManager;
        int ticks=0;
        std::vector<ofImage> people;
        int money = 0;
        bool lose=false;
        bool didiWin=false;
        

    public:
        Restaurant();
        Player* getPlayer();
        void setPlayer(Player *player);
        Rat* getRat();
        void setRat(Rat *rat);

        int getMoney(){return money;}
        void setMoney(int money) {this->money = money;}
        
        Item* cheese;
        Item* lettuce;
        Item* tomato;
        Item* burger;
        Item* botBread;
        Item* topBread;
        ofImage floor;
        ofImage inspectorPNG;
        ofImage chair;
        ofImage plant1;
        ofImage table1;
        void initItems();
        void initCounters();
        void initClients();
        void inDecoration();
        void generateClient();
        void serveClient();
        void tick();
        void render();
        void keyPressed(int key);
        bool ilose();
        bool iWin();
        void changetoWinState();
        void changetoLoseState();

  

};
