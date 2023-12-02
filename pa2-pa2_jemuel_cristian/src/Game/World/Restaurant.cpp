//
// Created by joshu on 11/3/2020.
//

#include "Restaurant.h"

Player *Restaurant::getPlayer() { return player; }
void Restaurant::setPlayer(Player *player) { this->player = player; }
Rat *Restaurant::getRat() { return rat; }
void Restaurant::setRat(Rat *rat) { this->rat = rat; }

Restaurant::Restaurant() {
    floor.load("images/floor.jpg");
  
    table1.load("images/table.png");



    plant1.load("images/realplant.png");
    entityManager = new EntityManager();
    ofImage chefPlayerImage;
    chefPlayerImage.load("images/chef.png");
    this->player = new Player(0, 600, 64, 64, chefPlayerImage, entityManager);    
    ofImage ratImage;
    ratImage.load("images/rat-charset.png");
    this->rat = new Rat(0, 600, 64, 64, ratImage, entityManager);
    initItems();
    initCounters();
    initClients();
    generateClient();

}
void Restaurant::initItems(){
    ofImage burgerSpriteSheet, cheeseImg, lettuceImg, tomatoImg, burgerImg, botBreadImg, topBreadImg, plateImg;
    burgerSpriteSheet.load("images/burger.png");
    topBreadImg.cropFrom(burgerSpriteSheet, 25, 16, 112, 43); // top bun
    burgerImg.cropFrom(burgerSpriteSheet, 30, 134, 103, 48); // patty
    cheeseImg.cropFrom(burgerSpriteSheet, 169, 213, 102, 39); // cheese
    tomatoImg.cropFrom(burgerSpriteSheet, 169, 158, 110, 41); // tomato
    lettuceImg.cropFrom(burgerSpriteSheet, 161, 62, 117, 34); // lettuce
    botBreadImg.cropFrom(burgerSpriteSheet, 444, 270, 115, 39); // bottom bun
    plateImg.cropFrom(burgerSpriteSheet, 575, 263, 131, 51); // plate

    cheese = new Item(cheeseImg, "cheese", 3.00);
    lettuce = new Item(lettuceImg, "lettuce", 2.00);
    tomato = new Item(tomatoImg, "tomato", 2.00);
    burger = new Item(burgerImg, "patty",4.00);
    botBread = new Item(botBreadImg, "bottomBun", 1.00);
    topBread = new Item(topBreadImg, "topBun", 1.00);
}
void Restaurant::initCounters(){
    int counterWidth = 96;
    int yOffset = 500;
    ofImage counterSheet, plateCounterImg, cheeseCounterImg, stoveCounterImg, lettuceCounterImg, emptyCounterImg, tomatoCounterImg, breadCounterImg;
    counterSheet.load("images/kitchen_cabinets_by_ayene_chan.png");
    stoveCounterImg.cropFrom(counterSheet, 224,12,32,43);//stoveTop
    lettuceCounterImg.cropFrom(counterSheet,96,76,32,43);//Vegetables
    emptyCounterImg.cropFrom(counterSheet,0,245,30,43);//Empty
    tomatoCounterImg.cropFrom(counterSheet,96,200,32,48);//fruit basket
    cheeseCounterImg.cropFrom(counterSheet,64,73,32,46);//cheese
    plateCounterImg.cropFrom(counterSheet,0,133,32,50);//plates
    breadCounterImg.cropFrom(counterSheet,0,63,34,56);//buns
    entityManager->addEntity(new BaseCounter(0,yOffset-16, counterWidth, 117, nullptr, plateCounterImg));
    entityManager->addEntity(new BaseCounter(counterWidth,yOffset-7, counterWidth,108, cheese, cheeseCounterImg));
    entityManager->addEntity(new BaseCounter(counterWidth*2,yOffset, counterWidth, 102, burger, stoveCounterImg));
    entityManager->addEntity(new BaseCounter(counterWidth*3, yOffset, counterWidth, 102, lettuce, lettuceCounterImg));
    entityManager->addEntity(new BaseCounter(counterWidth*4,yOffset, counterWidth, 102, nullptr, emptyCounterImg));
    entityManager->addEntity(new BaseCounter(counterWidth*5, yOffset -10, counterWidth, 113, tomato, tomatoCounterImg));
    entityManager->addEntity(new BaseCounter(counterWidth*6, yOffset-32, counterWidth, 133, botBread, breadCounterImg));
    entityManager->addEntity(new BaseCounter(counterWidth*7, yOffset-32, counterWidth, 133, topBread, breadCounterImg));

}

void Restaurant::initClients(){
    ofImage temp;
    temp.load("images/People/Car_Designer3Female.png");
    people.push_back(temp);
    temp.load("images/People/Freedom_Fighter2Male.png");
    people.push_back(temp);
    temp.load("images/People/Hipster.png");
    people.push_back(temp);
    temp.load("images/People/Lawyer2Male.png");
    people.push_back(temp);
    temp.load("images/People/Mad_Scientist3Female.png");
    people.push_back(temp);
    temp.load("images/People/Programmer2Male.png");
    people.push_back(temp);
    temp.load("images/People/Songwriter3Male.png");
    people.push_back(temp);
    temp.load("images/People/Weather_Reporter2Female.png");
    people.push_back(temp);
    
}
void Restaurant::tick() {
    ticks++;
    if(ticks % 600 == 0){
        generateClient();
    }
    player->tick();
    rat->tick();
    
    if(player->iAddedIngredient()){
        money-=1;
        player->setAddedIngredient(false);
    }
    this->setMoney(entityManager->inspectorLeaving(money));
    entityManager->tick();
    lose = entityManager->loseGame();

}


bool Restaurant::ilose(){
        return lose;
}
void Restaurant::changetoLoseState(){
    entityManager->changeLoseState();
}

void Restaurant::generateClient(){
    Burger* b1 = new Burger(72, 100, 50, 25);   
    vector<Item*> ingredients= {burger, cheese, tomato, lettuce};

    b1->addIngredient(botBread);
    b1->addIngredient(ingredients[ofRandom(4)]);
    b1->addIngredient(ingredients[ofRandom(4)]);
    b1->addIngredient(ingredients[ofRandom(4)]);
    b1->addIngredient(ingredients[ofRandom(4)]);
    b1->addIngredient(topBread);

    ofImage inspectorPNG;
    inspectorPNG.load("images/People/Inspector.png");
    int random = ofRandom(9); // 1/8 chances to make the inspector appear in each addClient method
    if(random == 0) {      
        entityManager->addClient(new Inspector(0, 50, 64, 72, inspectorPNG, b1, true));
    } else {
            entityManager->addClient(new Client(0, 50, 64, 72,people[ofRandom(8)], b1, false));
    }
    
}
void Restaurant::render() {
    floor.draw(0,0, ofGetWidth(), ofGetHeight());
    table1.draw(ofGetWidth()/2 -130, ofGetHeight()/2- 150, 100, 100);
    table1.draw(ofGetWidth()/2 + 80, ofGetHeight()/2 -150, 100,100);
    plant1.draw(ofGetWidth()-100 , 10, 30, 50);

    for(int i=0; i<3; i++){
    plant1.draw(10+300*i, ofGetHeight()-100, 30,50);
    
    }

    player->render();
    rat->render();
    entityManager->render();
    ofSetColor(0, 100, 0);
    ofDrawBitmapString("Money: " + to_string(money), ofGetWidth()/2, 10);
    ofSetColor(256, 256, 256);
    
}
void Restaurant::serveClient(){
    if(entityManager->firstClient!= nullptr){
        money += entityManager->firstClient->serve(player->getBurger());
        player->resetPrice();
        if(money>=100){
            didiWin=true;
            money= 0;
        }
    }
}
bool Restaurant::iWin(){
    return didiWin;
}

void Restaurant::changetoWinState(){
    if(didiWin) didiWin=false;
}

void Restaurant::keyPressed(int key) {
    player->keyPressed(key);
    if(key == 's'){
        serveClient();
        player->getBurger()->eraseBurger();
    }
}
