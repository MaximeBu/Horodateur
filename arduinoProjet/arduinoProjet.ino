#define yAxisPin A0

int yValue;

void setup() {
  Serial.begin(9600); // Initialisation du Serial
  Serial.flush();
  pinMode(yAxisPin, INPUT);
}

void loop() {
  yValue = analogRead(yAxisPin); // Lecture des données du Joystick
  yValue = map(yValue, 0, 1023, 0, 180); // Formatage des données vers un angle entre 0 et 180

  Serial.println(yAxisPin + ":" +yValue);

  delay(200);
}
