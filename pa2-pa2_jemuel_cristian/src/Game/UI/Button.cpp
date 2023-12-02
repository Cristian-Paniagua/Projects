#include "Button.h"
Button::Button(){
   this->xPos = ofGetWidth()/2;
    this->yPos = ofGetHeight()/2;
    this->width = 64;
    this->height = 20; 
}
Button::Button(int xPos, int yPos, int width, int height, string buttonText){
    this->xPos = xPos;
    this->yPos = yPos;
    this->width = width;
    this->height = height;
    this->buttonText = buttonText;
}

void Button::reset(){
    pressedCounter = -1;
    pressed = false;
}
void Button::tick(){
    pressedCounter--;
    if(pressedCounter == 0){
        pressed = false;
        pressedCounter = -1;
    }

}

void Button::mousePressed(int x, int y){
    if(xPos + width >= x && x >= xPos &&  yPos + height >= y && y >= yPos){
        pressed = true;
        pressedCounter = 10;
    }
}

void Button::render(){
    ofSetColor(0);
    ofDrawBitmapString(buttonText, xPos+width/2, yPos+height/2);
    ofDrawBitmapString("Instructions: ", 0, 15);
    ofDrawBitmapString("Press 'e' to pickup the ingredients\n Press 's' to serve the food\n Press 'u' to undo an ingredient\n For clear the burger press 'c'\n", 0, 30);

    ofDrawBitmapString("Tip: Be wary of the inspector, the terminator", ofGetWidth() / 3, 225);
    
}

bool Button::wasPressed(){
    return pressed;
}