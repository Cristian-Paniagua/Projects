#pragma once

#include "Client.h"

class Inspector: public Client {

    private:
        Burger* burger;

        int originalPatience;
        int patience=2000;
        float PCP = (float)255 / patience; // PCP = Per Client's Patience
        float sum = (float)255 / patience;

    public:

        Inspector(int x, int y, int width, int height, ofImage sprite, Burger* burger, bool isInspector) : 
        Client(x, y, width, height, sprite, burger, isInspector) {}

       
};