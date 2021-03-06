
#ifndef HEADER_POCKET_ORGAN
  #define HEADER_POCKET_ORGAN

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define MIDI_SERIAL Serial2
#define CONSOLE Serial1

/////////////////
//Choose output
//#define OUT_USB //Send Midi commands to the USB as a Midi device (with 32u4 or Arduino; use a computer as synth)
#define OUT_SERIAL //Send Midi commands on the serial line, to a Midi chip (embedded synth)

///////////////////
//Function buttons
#define B_SHARP  0
#define B_MIN    1 
#define B_7      2
#define B_SUS    3
#define B_AUG    4
#define B_VOL    5
#define B_INSTR  6
#define B_LOOP   7
#define B_RYTHM  8
#define B_MELODY_LOCK  8
#define B_MELODY 9 
#define B_PLUS   2
#define B_MINUS  4
#define B_ZERO   3
#define B_TRANSP 6
#define B_TUNE   7

//TODO
#define B_SUS2   8
#define B_ADD9   8
#define B_FAST   8

/////////////////
//MIDI codes
#define CHANNEL 0
#define MIDI_VOLUME 7
#define MIDI_BANK 0
#define MIDI_MODULATION 1
#define MIDI_EXPRESSION 0x0B
#define MIDI_EFFECT1 0x0C
#define MIDI_EFFECT2 0x0D
#define MIDI_ATTACK 0x49
#define MIDI_RELEASE 0x48
#define MIDI_DECAY 0x4B
#define MIDI_SOUND_VARIATION 0x46
#define MIDI_SOUND_TIMBRE 0x47
#define MIDI_BRIGHTNESS 0x4A
#define MIDI_VIBRATO_RATE 0x4C
#define MIDI_VIBRATO_DEPTH 0x4D
#define MIDI_PITCH_BEND 0xE0


/////////////////
//Global variables
extern Adafruit_SSD1306 display;
extern byte current_instrument;

/////////////////
//Digital buttons
#define NB_DB 4
static char DB[NB_DB] = {PB0, PC4, PA3, PA0};

/////////////////
//Digital buttons
#define LED_BUILTIN PC13

/////////////////
//EEPROM addresses

#define E_VOLUME 0
#define E_AB_CALIBRATION 1    //28 octets
#define E_LOOP_STATUS 30      //1 octet; which loops were recorded
#define E_LOOP_LENGTHS 32     //16 octets
#define E_LOOP_DURATIONS 48   //32 octets


/////////////////
//I2C addresses

#define ADDR_EEPROM 0x50

/////////////////
//Prototypes
void playNote(byte pitch);
void chordUpdate(char vel);
void chordStop();


#endif //HEADER_POCKET_ORGAN
