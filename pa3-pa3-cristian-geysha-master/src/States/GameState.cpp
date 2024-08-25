#include "GameState.h"

using namespace std;

//--------------------------------------------------------------
GameState::GameState() {
    foodSpawned = false;
    cellSize = 25;
    boardSizeWidth = 64;
    boardSizeHeight = 36;
    snake = new Snake(cellSize, boardSizeWidth, boardSizeHeight);
    for(int i = 0; i < (int)ofRandom(5, 10); i++) {
        rocks.push_back(new StaticEntity((int)ofRandom(1, boardSizeWidth-1), (int)ofRandom(1, boardSizeHeight-1), cellSize, cellSize));
    }

}
//--------------------------------------------------------------
GameState::~GameState() {
    delete snake;
}
//--------------------------------------------------------------
void GameState::reset() {
    delete snake;
    snake = new Snake(cellSize, boardSizeWidth, boardSizeHeight);
    rocks.clear();
    for(int i = 0; i < (int)ofRandom(5, 10); i++) {
       rocks.push_back(new StaticEntity((int)ofRandom(1, boardSizeWidth-1), (int)ofRandom(1, boardSizeHeight-1), cellSize, cellSize));
    }
    foodSpawned = false;
    speedBoostSpawned = false;
    betterAppleSpawned = false;
    godModeSpawned = false;
    currentPowerup = Powerless;
    storedPowerup = Powerless;
    speedBoostActive = false;
    godModeActive = false;
    
    setFinished(false);
    setNextState("");
}
//--------------------------------------------------------------
void GameState::update() {
    
    if(godModeActive) {     
        if(snake->getHead()[0] == -1 && move) { // Collision with left border
            godModeCollision = LeftBorder;
            snake->changeDirection(NONE);
            move = false;
        }
        else if(snake->getHead()[0] == boardSizeWidth - 1 && move) { // Collision with right border
            godModeCollision = RightBorder;
            snake->changeDirection(NONE);
            move = false;
        }
        else if(snake->getHead()[1] == -1 && move) { // Collision upper border
            godModeCollision = UpperBorder;
            snake->changeDirection(NONE);
            move = false;
        }
        else if(snake->getHead()[1] == boardSizeHeight - 1 && move) { // Collision with lower border
            godModeCollision = LowerBorder;
            snake->changeDirection(NONE);
            move = false;
        }
     }
    
    for(unsigned int i = 0; i < rocks.size(); i++) {
        if((snake->getHead()[0] == rocks[i]->getX()) && (snake->getHead()[1] == rocks[i]->getY())) {
            if(!godModeActive) {
                snake->setCrashed(true);
            }
                
        }
    }
    
    if(snake->isCrashed()) {
        this->setNextState("LoseState");
        this->setFinished(true);
        return;
    }

    if(snake->getHead()[0] == currentFoodX && snake->getHead()[1] == currentFoodY) {
        
        if(currentPowerup == SpeedBoost) {
            storedPowerup = SpeedBoost;
        }
        if(currentPowerup == BetterApple) {
            storedPowerup = BetterApple;
        }
        if(currentPowerup == GodMode) {
            storedPowerup = GodMode;
        }
        if(getScore() == 40) {
            currentPowerup = SpeedBoost;
            speedBoostSpawned = false;     
            setScore(getScore() + 10);
        } 
        else if(getScore() == 90) {
            currentPowerup = BetterApple;
            betterAppleSpawned = false;
            setScore(getScore() + 10);
        }
        else if(getScore() == 140) {
            currentPowerup = GodMode;
            godModeSpawned = false;
            setScore(getScore() + 10);
        } 
        else {     
        snake->grow();
        foodSpawned = false;
        currentPowerup = Powerless;
        
        }
    }

    if(currentPowerup == SpeedBoost || currentPowerup == BetterApple || currentPowerup == GodMode) {
        powerupSpawner();
    } else {
        foodSpawner(); 
    }

    if(speedBoostActive && speedBoostTimer == 85) {
        speedBoostTimer = 0;
        speedBoostActive = false;
    }
     if(godModeActive && godModeTimer == 57) {
        godModeTimer = 0;
        godModeActive = false;
        snake->setGodMode(false);
     } 
    if(speedBoostTimer < 85 && speedBoostActive) {
        if(ofGetFrameNum() % 5 == 0) {
        snake->update(); 
        }
        if(ofGetFrameNum() % 10 == 0) {
            timer++;  

            if(speedBoostTimer < 85 && speedBoostActive) {
                speedBoostTimer++;
            }
            if(godModeTimer < 57 && godModeActive) {
                godModeTimer++;
            }

        } 
    
    } else {

        if(ofGetFrameNum() % 10 == 0) {
            snake->update();
            timer++;  

            if(speedBoostTimer < 85 && speedBoostActive) {
                speedBoostTimer++;
            }
            if(godModeTimer < 57 && godModeActive) {
                godModeTimer++;
            }
        } 
    }
    
   

    switch (timer)
    {
    case 170:
        foodSpawned = false;
        currentColor = Red;
        timer = 0;
        break;
    case 57:
        currentColor = DarkRed;
        break;
    case 113:
        currentColor = Brown;
        break;
    }

}
//--------------------------------------------------------------
void GameState::draw() {
    drawBoardGrid();
    ofFill();
    snake->draw();
    rockSpawner();
    if(currentPowerup == SpeedBoost || currentPowerup == BetterApple || currentPowerup == GodMode) {
        drawPowerup();
    } else {
        drawFood();
    } 
    ofDrawBitmapString("Score: "+ofToString(getScore()), (ofGetWidth()/2)-30, 20);
}
//--------------------------------------------------------------
void GameState::keyPressed(int key) {
        
        if(key == 'a') { // key to add 10 to score
            setScore(getScore() + 10);
        }
        if(key == 's') { // debug key to subtract 10 to score
            setScore(getScore() - 10);
        }
        if(key == 'u') { // key to undo the tail of the snake
            snake->undo();
        }
        if(key == 'p') { //ckey to trigger pause state
            this->setNextState("PauseState");
            this->setFinished(true);
        }
        if(key == 'b') { // key to activate powerup
            if(storedPowerup == SpeedBoost) {
                speedBoostActive = true;
                storedPowerup = Powerless;
            }
            else if(storedPowerup == BetterApple) {
                snake->grow();
                snake->grow();
                setScore(getScore() - 20);
                storedPowerup = Powerless;
            }
            else if(storedPowerup == GodMode) {
                godModeActive = true;
                storedPowerup = Powerless;
                snake->setGodMode(true);
            }
        }

    if(key != OF_KEY_LEFT && key != OF_KEY_RIGHT && key != OF_KEY_UP && key != OF_KEY_DOWN) { return; }

    switch(key) {
        case OF_KEY_LEFT:
            if(godModeCollision != LeftBorder) {
               snake->changeDirection(LEFT);
               godModeCollision = NoCollision;
               move = true;
            }        
            break;
        case OF_KEY_RIGHT:
            if(godModeCollision != RightBorder) {
                snake->changeDirection(RIGHT);
                godModeCollision = NoCollision;
                move = true;
            }           
            break;
        case OF_KEY_UP:
            if(godModeCollision != UpperBorder) {
                snake->changeDirection(UP);
                godModeCollision = NoCollision;
                move = true;
            }           
            break;
        case OF_KEY_DOWN:
            if(godModeCollision != LowerBorder) {
                snake->changeDirection(DOWN);
                godModeCollision = NoCollision;
                move = true;
            }       
            break;
        
    }
}
//--------------------------------------------------------------
void GameState::foodSpawner() {
    if(!foodSpawned) {
        bool isInSnakeBody;
        do {
            isInSnakeBody = false;
            currentFoodX = ofRandom(1, boardSizeWidth-1);
            currentFoodY = ofRandom(1, boardSizeHeight-1);
            for(unsigned int i = 0; i < snake->getBody().size(); i++) {
                if(currentFoodX == snake->getBody()[i][0] and currentFoodY == snake->getBody()[i][1]) {
                    isInSnakeBody = true;
                }
            }
        } while(isInSnakeBody);
        foodSpawned = true;
        currentColor = Red;
        timer = 0;
    }
}

void GameState::powerupSpawner() {

    if(!speedBoostSpawned && currentPowerup == SpeedBoost) {
        bool isInSnakeBody;
        do {
            isInSnakeBody = false;
            currentFoodX = ofRandom(1, boardSizeWidth-1);
            currentFoodY = ofRandom(1, boardSizeHeight-1);
            for(unsigned int i = 0; i < snake->getBody().size(); i++) {
                if(currentFoodX == snake->getBody()[i][0] and currentFoodY == snake->getBody()[i][1]) {
                    isInSnakeBody = true;                  
                }
            }
        } while(isInSnakeBody);
        speedBoostSpawned = true;
        
        
    }
    else if(!betterAppleSpawned && currentPowerup == BetterApple) {
        bool isInSnakeBody;
        do {
            isInSnakeBody = false;
            currentFoodX = ofRandom(1, boardSizeWidth-1);
            currentFoodY = ofRandom(1, boardSizeHeight-1);
            for(unsigned int i = 0; i < snake->getBody().size(); i++) {
                if(currentFoodX == snake->getBody()[i][0] and currentFoodY == snake->getBody()[i][1]) {
                    isInSnakeBody = true;
                }
            }
        } while(isInSnakeBody);
        betterAppleSpawned = true;
        
        
    }
    else if(!godModeSpawned && currentPowerup == GodMode) {
        bool isInSnakeBody;
        do {
            isInSnakeBody = false;
            currentFoodX = ofRandom(1, boardSizeWidth-1);
            currentFoodY = ofRandom(1, boardSizeHeight-1);
            for(unsigned int i = 0; i < snake->getBody().size(); i++) {
                if(currentFoodX == snake->getBody()[i][0] and currentFoodY == snake->getBody()[i][1]) {
                    isInSnakeBody = true;                 
                }
            }
        } while(isInSnakeBody);
        godModeSpawned = true;
        
    }
}
//--------------------------------------------------------------

void GameState::rockSpawner() {
    
    for(unsigned int i = 0; i < rocks.size(); i++) {
        for(unsigned int i2 = 0; i2 < snake->getBody().size(); i2++) {
            if(rocks[i]->getX() == snake->getBody()[i2][0] and rocks[i]->getY() == snake->getBody()[i2][1]) {            
                } else {
                     rocks[i]->draw();
                }
        }
    }

}

//--------------------------------------------------------------
void GameState::drawFood() {

    switch (currentColor)
    {
    case Red:
        ofSetColor(255, 0 , 0);
        break;
    case DarkRed:
        ofSetColor(204, 0, 0);
        break;
    case Brown:
        ofSetColor(204, 102, 0);
        break;    
    default:
        ofSetColor(255, 0 , 0);
        break;
    }
    if(foodSpawned) {
        ofDrawRectangle(currentFoodX*cellSize, currentFoodY*cellSize, cellSize, cellSize);
    }
}

void GameState::drawPowerup() {

    if(speedBoostSpawned && currentPowerup == SpeedBoost) {
        ofSetColor(0, 0, 255);
        ofDrawRectangle(currentFoodX*cellSize, currentFoodY*cellSize, cellSize, cellSize);
    }
    else if(betterAppleSpawned && currentPowerup == BetterApple) {
        ofSetColor(255, 255, 0);
        ofDrawRectangle(currentFoodX*cellSize, currentFoodY*cellSize, cellSize, cellSize);
        
    }
    else if(godModeSpawned && currentPowerup == GodMode) {
        ofSetColor(0, 145, 145);
        ofDrawRectangle(currentFoodX*cellSize, currentFoodY*cellSize, cellSize, cellSize);
        
    }
}
//--------------------------------------------------------------
void GameState::drawStartScreen() {
    ofSetColor(ofColor::black);
    ofDrawRectangle(0,0,ofGetWidth(),ofGetHeight());
    ofSetColor(ofColor::white);
    string text = "Press any arrow key to start.";
    ofDrawBitmapString(text, ofGetWidth()/2-8*text.length()/2, ofGetHeight()/2-11);
    return;
}
//--------------------------------------------------------------
void GameState::drawLostScreen() {
    ofSetColor(ofColor::black);
    ofDrawRectangle(0,0,ofGetWidth(),ofGetHeight());
    ofSetColor(ofColor::white);
    string text = "You Lost!";
    string text2 = "Press any arrow key to play again or press ESC to exit.";
    ofDrawBitmapString(text, ofGetWidth()/2-8*text.length()/2, ofGetHeight()/2-11);
    ofDrawBitmapString(text2, ofGetWidth()/2-8*text2.length()/2, ofGetHeight()/2+2);
    return;
}
//--------------------------------------------------------------
void GameState::drawBoardGrid() {
    
    ofDrawGrid(25, 64, false, false, false, true);
    
    // ofSetColor(ofColor::white);
    // for(int i = 0; i <= boardSize; i++) {
    //     ofDrawLine(i*cellSize, 0, i*cellSize, ofGetHeight());
    //     ofDrawLine(0, i*cellSize, ofGetWidth(), i*cellSize);
    // }
}
//--------------------------------------------------------------
void GameState::mousePressed(int x, int y, int button){

}

