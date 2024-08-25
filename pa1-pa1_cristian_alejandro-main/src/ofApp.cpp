#include "ofApp.hpp"

//--------------------------------------------------------------
void ofApp::setup() {
    backgroundImage.load("basic-background.jpg");
    sound.load("beat.wav");           // Loads a sound file (in bin/data/)
    sound.setVolume(volume);               // Sets the song volume
    ofSetBackgroundColor(60, 60, 60); // Sets the Background Color
    //Setup for Custom Mode 3
    center.set(ofGetWidth() / 2, (ofGetHeight() / 2) - 130);  // Define the center of the screen
    radius = 200;                                   //Defines the radius of the circle
    numLines = 64;                                   //number of lines
    angle = 360.0 / numLines;                         //Define the angle between the lines
    lineLength = (radius * 0.5);
}

//--------------------------------------------------------------
void ofApp::update() {
    /* The update method is called muliple times per second
    It's in charge of updating variables and the logic of our app */
    ofSoundUpdate();               // Updates all sound players
    if(!pause) {
        visualizer.updateAmplitudes(); // Updates Amplitudes for visualizer
    } 
    //Keeps the background and center with the correct dimensions
    backgroundImage.resize(ofGetWidth(), ofGetHeight());
    center.set(ofGetWidth() / 2, (ofGetHeight() / 2) - 130);
    p_y = ofGetHeight() - 50;
    p_width = ofGetWidth();
    //Controls the loopMode behavior 
    if (loopMode && playing && !sound.isPlaying() && currentSong <= songs.size() - 2 && !isDragging) {
        currentSong += 1; 
        sound.load(songs[currentSong]);
        sound.play();
    }
    if (loopMode && playing && !sound.isPlaying() && currentSong == songs.size() - 1 && !isDragging){
        currentSong = 0;
        sound.load(songs[currentSong]);
        sound.play();
    }
    //Controls the behavior of shuffleMode
    if (shuffleMode && playing && !sound.isPlaying() && !isDragging){
        while (currentSong == lastSong){
            currentSong = ofRandom(4); 
        }
        lastSong = currentSong;
        sound.load(songs[currentSong]);
        sound.play();
    }

    if (playing && !sound.isPlaying() && !loopMode && !isDragging){
        playing = false;
    }

    progress = sound.getPosition();
}

//--------------------------------------------------------------
void ofApp::draw() {
    /* The update method is called muliple times per second
    It's in charge of drawing all figures and text on screen */
    vector<float> amplitudes = visualizer.getAmplitudes();
    if (mode == '1') {
        drawMode1(amplitudes);
    } else if (mode == '2') {
        drawMode2(amplitudes);
    } else if (mode == '3') {
        drawMode3(amplitudes);
    } 
    // Progress Bar
    if (mode == '3'){ ofSetColor(0); }
    else { ofSetColor(255); }
    ofFill();

   // Current Song
    if (mode == '3'){ ofSetColor(0); }
    else { ofSetColor(255); }
    ofDrawBitmapString("Current Song: " + songs[currentSong], 0, 30);
    ofDrawBitmapString("Volume: " + to_string(int(volume * 100)), 0, 60);
   
   
    float pos = playing ? progress : lastPos;
    int percent = pos * 100;
    ofDrawBitmapString("Song Progress: " + ofToString(percent) + "%", 0, 45);

    // Mode Selection
    if (!playing) {
        ofDrawBitmapString("Press 'p' to play some music!", ofGetWidth() / 2 - 100, ofGetHeight() / 2);
        //Play Button
        ofSetColor(255,0,0);
        ofDrawTriangle(ofGetWidth() / 2,ofGetHeight() - 110,ofGetWidth() / 2,ofGetHeight() - 65, (ofGetWidth() / 2) + 30, ofGetHeight() - 85);
    }
    else if (playing){
        //Pause Button
        ofSetColor(255,0,0);
        ofDrawRectRounded(ofGetWidth() / 2, ofGetHeight() - 110, 40, 40, 10);
    }

    //Visual Progress Bar
    ofFill(); 
    ofPushStyle();
    ofSetColor(200);
    ofDrawRectRounded(0, ofGetHeight() - 50, 99 * ofGetWidth() / 99, 25, 10);
    ofSetColor(255);
    float progressWidth = (progress / songDuration * p_width);
    ofDrawRectRounded(p_x, p_y, progressWidth, p_height, 10);
    ofPopStyle();
    
    //LoopMode
    if (mode == '3'){ ofSetColor(0); }
    else { ofSetColor(255); }
    if (loopMode){
        ofDrawBitmapString("Current mode: Loop-Mode", 0, 75);
    }
    // ofDrawBitmapString("Current Mouse Position: " + ofToString(cur_x) + ", " + ofToString(cur_y), 0, 75);
    // Repeat Mode
    if (repeatMode){
        ofDrawBitmapString("Current mode: Repeat-Mode", 0, 75);
    }

    if (shuffleMode){
        ofDrawBitmapString("Current mode: Shuffle-Mode", 0, 75);
    }
}
void ofApp::drawMode1(vector<float> amplitudes) {
    ofSetBackgroundColor(120, 120, 120);
    ofFill();        // Drawn Shapes will be filled in with color
    ofSetColor(255);
    ofDrawBitmapString("Rectangle Height Visualizer", 0, 15);
    ofSetColor(0,randBlue,255); // This resets the color of the "brush" to white
    for (int i = 0; i < amplitudes.size(); i++) {
        ofDrawRectRounded(i * ((ofGetWidth() / amplitudes.size()) - 1), ofGetHeight() - 100,  ofGetWidth() / amplitudes.size(), amplitudes[i], 10);
    }
}
void ofApp::drawMode2(vector<float> amplitudes) {
    ofSetLineWidth(5); // Sets the line width
    ofNoFill();        // Only the outline of shapes will be drawn
    ofSetColor(256);   // This resets the color of the "brush" to white
    ofDrawBitmapString("Circle Radius Visualizer", 0, 15);
    ofSetBackgroundColor(90, 90 ,90);
    int bands = amplitudes.size();
    for (int i = 0; i < bands; i++) {
        ofSetColor((bands - i) * 32 % 256, 18, 144); // Color varies between frequencies
        ofDrawCircle(ofGetWidth() / 2, ofGetHeight() / 2, amplitudes[0] / (i + 1));
    }
}

void ofApp::drawMode3(vector<float> amplitudes) {
    ofSetColor(255); // This resets the color of the "brush" to white
    // YOUR CODE HERE
    backgroundImage.draw(0,0);
    ofSetColor(0);
    ofDrawBitmapString("Custom Visualizer", 0, 15); 
    ofSetLineWidth(2); 
    for (int i = 0; i < amplitudes.size(); i++) {
        float x = center.x + radius * cos(ofDegToRad(angle * i)) * amplitudes[i] * 0.05; //The length of the lines
        float y = center.y + radius * sin(ofDegToRad(angle * i)) * amplitudes[i] * 0.05; //depends on the amplitude of the sound
        ofDrawLine(center, ofPoint(x, y));   // Draws the lines
    }

}

//--------------------------------------------------------------
void ofApp::keyPressed(int key) {
    // This method is called automatically when any key is pressed
    switch (key) {
    case 'p':
        if (playing) {
            sound.stop();
        } else if (!playing) {
            sound.play();
        }
        playing = !playing;
        break;
    case 'a':
        pause = !pause; 
        break;
    case 'd':
        sound.load(songs[1]);
        sound.play();
        while(playing == false){  //While loop to reset the song's %, progress bar, and center message
            playing = !playing;
        }
        currentSong = 1;
        break;
    case 'f':
        sound.load(songs[2]);
        sound.play();
        while(playing == false){
            playing = !playing;
        }
        currentSong = 2;
        break;
    case 'g':
        sound.load(songs[0]);
        sound.play();
        while(playing == false){
            playing = !playing;
        }
        currentSong = 0;
        break;
    case 'h':
        sound.load(songs[3]);
        sound.play();
        while(playing == false){
            playing = !playing;
        }
        currentSong = 3;
        break;
    case '=':
        if((volume * 100) < 99) {
            volume += 0.1;
            sound.setVolume(volume);
        }
        break;
    case '-':
        if((volume * 100) > 0.10) {
            volume -= 0.1;
            sound.setVolume(volume);
        }
        break;
    case 'l':
        if (loopMode){
            loopMode = false; 
            break;
        }
        sound.setLoop(false);
        loopMode = true;
        repeatMode = false;
        shuffleMode = false;
        break;
    case 'r':
        if (repeatMode){
            repeatMode = false;
            sound.setLoop(false);
            break;
        }
        repeatMode = true;
        loopMode = false;
        shuffleMode = false;
        sound.setLoop(true);
        break;
    case 'b':
        if (shuffleMode){
            shuffleMode = false;
            break;
        }
        shuffleMode = true;
        loopMode = false;
        repeatMode = false;
        sound.setLoop(false);
        break;
    case '1':
        mode = '1';
        randBlue = ofRandom(255);
        break;
    case '2':
        mode = '2';
        break;
    case '3':
        mode = '3';
        break;
    }
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key) {
}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y) {
    cur_x = x;
    cur_y = y;
}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button) 
{
    if (isDragging){
        cur_x = x;
        cur_y = y;
        progress = ofClamp((mouseX - p_x) / p_width * songDuration, 0, songDuration);
        sound.setPosition(progress);
        sound.setPaused(true);
    }
}
// ofDrawTriangle(ofGetWidth() / 2,ofGetHeight() - 110,ofGetWidth() / 2,ofGetHeight() - 65, (ofGetWidth() / 2) + 30, ofGetHeight() - 85);
//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button) {
    if (button == 0){
        if (cur_x >= ofGetWidth() / 2 && cur_x <= (ofGetWidth() / 2) + 40 && cur_y >= ofGetHeight() - 110 && cur_y <= ofGetHeight() - 60 && playing){
            playing = false;
            sound.stop();
        }
        else if (cur_x >= ofGetWidth() / 2 && cur_x <= (ofGetWidth() / 2) + 40 && cur_y >= ofGetHeight() - 110 && cur_y <= ofGetHeight() - 60 && !playing){
            playing = true;
            sound.play();
        }
        else if (cur_x >= 0 && cur_x <= p_width && cur_y >= ofGetHeight() - 50 && cur_y <= ofGetHeight() - 25)
        {
            isDragging = true;
            m_prevPosition = progress;
        }
    }

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button) {
    if(button == 0 && isDragging && !playing){
        isDragging = false; 
        sound.setPaused(false);
        sound.play();
        playing = true;
    }
    else if(button == 0 && isDragging && playing){
        isDragging = false; 
        sound.setPaused(false);
    }
}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y) {
}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y) {
}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h) {
}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg) {
}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo) {
}
//--------------------------------------------------------------