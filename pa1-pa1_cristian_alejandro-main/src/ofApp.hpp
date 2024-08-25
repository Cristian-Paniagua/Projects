#pragma once

#include "AudioVisualizer.hpp"
#include "ofMain.h"

class PausePlayButton{
    int buttonX;
    int buttonY;
    int buttonWidth;
    int buttonHeight;
  public:
    //Constructor
    PausePlayButton(int buttonX, int buttonY, int buttonWidth, int buttonHeight){
      this->buttonX = buttonX;
      this->buttonY = buttonY;
      this->buttonWidth = buttonWidth;
      this->buttonHeight = buttonHeight;
    }
    //Setters and Getters
    int getbuttonX(){ return buttonX; }
    int getbuttonY(){ return buttonY; }
    int getbuttonWidth(){ return buttonWidth; }
    int getbuttonHeight(){ return buttonHeight; }
    //__________________________________________
    void setbuttonX(int x){ buttonX = x; }
    void setbuttonY(int y){ buttonY = y; }
    void getbuttonHeight(int height){ buttonHeight = height; }
    void getbuttonWidht(int width){ buttonWidth = width; }
  
    //Draw Methods
    void drawPauseButton(){
      ofDrawRectangle(buttonX, buttonY, buttonWidth, buttonHeight);
    }
    void drawPlayButton();

};

class ofApp : public ofBaseApp {

  private:
    ofSoundPlayer sound;
    AudioVisualizer visualizer;
    ofImage backgroundImage;

    bool playing = false;
    char mode = '1';

    int cur_x, cur_y = 0;
    float sound_length;

    float progress = 0;
    float lastPos = 0;

    //Mode 1 Color 
    int randBlue = ofRandom(255);

    bool pause = false;

    double volume = 0.5;

    //Progress Bar
    float p_position;         
    float songDuration = 1;
    bool isDragging = false;
    float m_prevPosition = 0;
    //Dimensions for progress bar
    float p_x = 0;
    float p_y = ofGetHeight() - 50;
    float p_width = ofGetWidth();
    float p_height = 25;

    //Loop key
    bool loopMode = false;
    vector <string> songs = {"beat.wav", "geesebeat.wav", "pigeon-coo.wav", "rock-song.wav"};
    int currentSong = 0;

    //Repeat key
    bool repeatMode = false; 
  
    //Shuffle key
    bool shuffleMode = false;
    int lastSong = 0;

    //Custom Mode 3 
    ofPoint center;     // Center of the circle
    float radius;       // Radius of the circle
    int numLines;       // Number of lines around the circle
    float angle;        // Angle between the lines
    float lineLength;   // Length of the lines

    

  public:
    void setup();
    void update();
    void draw();

    void drawMode1(vector<float> amplitudes);
    void drawMode2(vector<float> amplitudes);
    void drawMode3(vector<float> amplitudes);

    void keyPressed(int key);
    void keyReleased(int key);
    void mouseMoved(int x, int y);
    void mouseDragged(int x, int y, int button);
    void mousePressed(int x, int y, int button);
    void mouseReleased(int x, int y, int button);
    void mouseEntered(int x, int y);
    void mouseExited(int x, int y);
    void windowResized(int w, int h);
    void dragEvent(ofDragInfo dragInfo);
    void gotMessage(ofMessage msg);
};
