#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);
String titre = "Menu:";
String option1 = "1: Debut journee";
String option2 = "2: Fin journee";
String option3 = "3: Debut pause";
String option4 = "4: Fin pause";
String option0 = "Code:";
String text = "1234";

#define yAxisPin A0
#define button3 7
#define touchText 4

int menuPos = 1;
int yValue;
int touchValue;
int touchValueTexte;

void setup() {
  lcd.init(); // initialisation de l'afficheur
  lcd.backlight();
  // lcd.blink_on();
  Serial.begin(9600);
  // Serial.flush();
  pinMode(yAxisPin, INPUT);
  pinMode(button3, INPUT);
  pinMode(touchText, INPUT);

  /*for (int i=0; i < 7; i++) {
    lcd.setCursor(i, 0);
    lcd.print("_");
  }*/
}

void loop() {
  yValue = analogRead(yAxisPin);
  yValue = map(yValue, 0, 1023, 0, 180);
  touchValue = digitalRead(button3);
  touchValueTexte = digitalRead(touchText);


  if (touchValue) {
    menuPos = 0;
  }

  if (touchValueTexte) {
    lcd.clear();
    lcd.print(text);
  }

  // Serial.println(yValue);

  if (yValue < 40 && menuPos > 0) {
    menuPos --;
  } else if (yValue > 140 && menuPos < 4) {
    menuPos ++;
  }

  //Serial.println(menuPos);


switch(menuPos) {
      case 0 :
        lcd.clear();
        lcd.print(option0);
        lcd.setCursor(5, 0);
        lcd.blink_on();
        break;
      case 1:
        lcd.clear();
        lcd.print(titre);
        lcd.setCursor(0, 1);
        lcd.print(option1);
        break;
      case 2:
        lcd.clear();
        lcd.print(option1);
        lcd.setCursor(0, 1);
        lcd.print(option2);
        break;
      case 3:
        lcd.clear();
        lcd.print(option2);
        lcd.setCursor(0, 1);
        lcd.print(option3);
        break;
      case 4:
        lcd.clear();
        lcd.print(option3);
        lcd.setCursor(0, 1);
        lcd.print(option4);
        break;
      default:
        break;
    }


  /* (Serial.available() > 0) {
    int command = Serial.parseInt();
    switch(menuPos) {
      case 1:
        lcd.clear();
        lcd.print(titre);
        lcd.setCursor(0, 1);
        lcd.print(option1);
        break;
      case 2:
        lcd.clear();
        lcd.print(option1);
        lcd.setCursor(0, 1);
        lcd.print(option2);
        break;
      case 3:
        lcd.clear();
        lcd.print(option2);
        lcd.setCursor(0, 1);
        lcd.print(option3);
        break;
      case 4:
        lcd.clear();
        lcd.print(option3);
        lcd.setCursor(0, 1);
        lcd.print(option4);
        break;
      default:
        break;
    }
  }*/


  


  delay(200);
}
