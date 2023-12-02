//
// Created by joshu on 11/4/2020.
//

#include "Burger.h"

using namespace std;

Burger::Burger(int x, int y, int width, int height){
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
}

void Burger::addIngredient(Item *item) {
    ingredients.push_back(item);
}

void Burger::render(){
    int counter = 1;
    for (Item* ingredient:ingredients){
        ingredient->sprite.draw(x-5,y-(counter * 10)+55,width*0.70,height*0.70);
        counter++;
    }
}

bool Burger::burgerEquals(Burger* clientBurger) {
   vector<Item *> clientIngredients = clientBurger->getIngredients();
   vector<Item *> playerIngredients = this->getIngredients();
int clientbur=0;
int clientlet=0;
int clientcheese=0;
int clienttom=0;
int playbur=0;
int playlet=0;
int playcheese=0;
int playtom=0;
    if(playerIngredients.size()==0) {return false;}
    
    if(playerIngredients[0]->getName() != "bottomBun") {
            return false;
        }
    if(playerIngredients[playerIngredients.size() - 1]->getName() != "topBun") {
            return false;
        }

        if(clientIngredients.size()!= playerIngredients.size()) {return false;}

        else{
    for(int i=1; i<clientIngredients.size(); i++){
        if(clientIngredients[i]->getName()=="patty"){
            clientbur++;
        }
        if(playerIngredients[i]->getName()=="patty"){
            playbur++;
        }
        if(clientIngredients[i]->getName()=="cheese"){
            clientcheese++;
        }
        if(playerIngredients[i]->getName()=="cheese"){
            playcheese++;
        }
        if(clientIngredients[i]->getName()=="lettuce"){
            clientlet++;
        }
        if(playerIngredients[i]->getName()=="lettuce"){
            playlet++;
        }
        if(clientIngredients[i]->getName()=="tomato"){
            clienttom++;
        }
        if(playerIngredients[i]->getName()=="tomato"){
            playtom++;
        }
    }
        }
    if(clientbur==playbur&&clientcheese==playcheese&&clientlet==playlet&&clienttom==playtom) {return true;}
    else {return false;}

}

void Burger::clear(){
    ingredients.empty();
}

void Burger::eraseBurger() {
    ingredients.clear();
}

void Burger::undoIngredient() { 
    ingredients.pop_back();
}

vector<Item *> Burger::getIngredients() {
    return ingredients;
}

double Burger::getBurgerPrice(Burger* burger){
    
    vector<Item*> result= burger->getIngredients();
    for(int i=0; i<result.size(); i++){
        priceBurger+= result[i]->getPrice();
    }
    return priceBurger;
}