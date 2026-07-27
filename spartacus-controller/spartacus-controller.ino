#include <PinChangeInterrupt.h>

#define T_PIN 4  // Left vertical
#define A_PIN 6 // right horizontal
#define R_PIN 5 // left horizontal
#define E_PIN 7 // right vertical

#define T_CENTER 1580
#define T_DEVIATION 345

#define A_CENTER 1544
#define A_DEVIATION 412

#define R_CENTER 1560
#define R_DEVIATION 404

#define E_CENTER 1560
#define E_DEVIATION 430

#define MOVE_THRESH 0.1

bool connected = false;

float left_power = 1;
float right_power = 1;

volatile unsigned long t_start, a_start, r_start, e_start;
volatile int t_val = 1500, a_val = 1500, r_val = 1500, e_val = 1500;

void t_ISR() {
  if (digitalRead(T_PIN) == HIGH) t_start = micros();
  else t_val = micros() - t_start;
}

void a_ISR() {
  if (digitalRead(A_PIN) == HIGH) a_start = micros();
  else a_val = micros() - a_start;
}

void r_ISR() {
  if (digitalRead(R_PIN) == HIGH) r_start = micros();
  else r_val = micros() - r_start;
}

void e_ISR() {
  if (digitalRead(E_PIN) == HIGH) e_start = micros();
  else e_val = micros() - e_start;
}

void setup() {
  pinMode(T_PIN, INPUT);
  attachPCINT(digitalPinToPCINT(T_PIN), t_ISR, CHANGE);

  pinMode(A_PIN, INPUT);
  attachPCINT(digitalPinToPCINT(A_PIN), a_ISR, CHANGE);

  pinMode(R_PIN, INPUT);
  attachPCINT(digitalPinToPCINT(R_PIN), r_ISR, CHANGE);

  pinMode(E_PIN, INPUT);
  attachPCINT(digitalPinToPCINT(E_PIN), e_ISR, CHANGE);

  Serial.begin(115200);
}

void loop() {
  Serial.print(connected);
  Serial.print(" ");
  Serial.print(t_val);
  Serial.print(" ");
  Serial.print(a_val);
  Serial.print(" ");
  Serial.print(r_val);
  Serial.print(" ");
  Serial.println(e_val);



  float lv = float(t_val - T_CENTER) / float(T_DEVIATION);
  float lh = float(r_val - R_CENTER) / float(R_DEVIATION);

  float rv = float(e_val - E_CENTER) / float(E_DEVIATION);
  float rh = float(a_val - A_CENTER) / float(A_DEVIATION);

  if (lv < MOVE_THRESH)
    lv = 0;

  lv = min(lv, 1);
  lv = max(lv, -1);

  if (lv > 0){
    connected = true;
  }else{
    connected = false;
    left_power = 0;
    right_power = 0;
    delay(100);
    return;
  }

  if (lh < MOVE_THRESH)
    lh = 0;

  lh = min(lh, 1);
  lh = max(lh, -1);

  if (rv < MOVE_THRESH)
    rv = 0;

  rv = min(rv, 1);
  rv = max(rv, -1);

  if (rh < MOVE_THRESH)
    rh = 0;

  rh = min(rh, 1);
  rh = max(rh, -1);



  delay(100);
}