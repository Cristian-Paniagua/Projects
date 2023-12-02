#pragma once
#include "Entity.h"
#include "Burger.h"


class Client: public Entity{
    private:
        Burger* burger;

        int originalPatience;
        int patience=2000;
        float PCP = (float)255 / patience; // PCP = Per Client's Patience
        float sum = (float)255 / patience;
    public:
        Client(int, int, int, int, ofImage, Burger*, bool);
        virtual ~Client();
        void tick();
        void render();
        int serve(Burger*);
        Client* nextClient=nullptr;
        bool isLeaving=false;
        int getPatience();
        bool isInspector = false;





};