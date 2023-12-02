//
// Created by joshu on 11/4/2020.
//
#pragma once

#include "ofMain.h"

class Item {
private:

    double priceItem;

public:
    Item(ofImage, string, double);
    ofImage sprite;
    string name;
    string getName(){ return name;}
    double getPrice(){ return priceItem;}
   
};
