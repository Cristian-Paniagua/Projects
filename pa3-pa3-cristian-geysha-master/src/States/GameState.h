#pragma once

#include "State.h"
#include "Snake.h"
#include "ofMain.h"
#include "StaticEntity.h"
#include <vector>

class GameState : public State {
    public:
        GameState();
        ~GameState();
        void reset();
        void update();
        void draw();
        void keyPressed(int key);
        void mousePressed(int x, int y, int button);
        void foodSpawner();
        void rockSpawner();
        void powerupSpawner();
        void drawFood(); 
        void drawPowerup();
        void drawStartScreen();
        void drawLostScreen();
        void drawBoardGrid();
        
        Snake* snake;
        vector<StaticEntity* > rocks; 
        
        bool foodSpawned = false;
        int timer = 0;
        int speedBoostTimer = 0;
        int godModeTimer = 0;

        int currentFoodX;
        int currentFoodY;

        int boardSizeWidth, boardSizeHeight;
        int cellSize; // Pixels

        int getScore() {return snake->score;}
        void setScore(int score) {snake->score = score;}

        enum Color { Red, DarkRed, Brown}
        currentColor;
        
        enum Powerup {Powerless, SpeedBoost, BetterApple, GodMode}
        currentPowerup, // powerup at UI
        storedPowerup; // powerup stored

        bool speedBoostSpawned = false;
        bool betterAppleSpawned = false;
        bool godModeSpawned = false;

        enum GodModeCollision {LeftBorder, UpperBorder, RightBorder, LowerBorder, NoCollision}
        godModeCollision;

        bool speedBoostActive = false;
        bool godModeActive = false;

        bool move = true;
};      

