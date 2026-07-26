#include <PinChangeInterrupt.h>

#define T_PIN 4  // Left vertical
#define A_PIN 6 // right horizontal
#define R_PIN 5 // left horizontal
#define E_PIN 7 // right vertical


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
  Serial.print(t_val);
  Serial.print(" ");
  Serial.print(a_val);
  Serial.print(" ");
  Serial.print(r_val);
  Serial.print(" ");
  Serial.println(e_val);

  delay(100);
}