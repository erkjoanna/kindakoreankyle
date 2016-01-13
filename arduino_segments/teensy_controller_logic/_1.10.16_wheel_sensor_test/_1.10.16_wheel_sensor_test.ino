//Hi Kyle! All you have to do is change the 1,2,3,4 to whatever
//pins you want to use and it should work!

/* READ THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
some cytron info:
DIRx is direction - HIGH is forward and LOW is reverse I think
PWMx is the PWM lol
If you look at the cytron motor guide I sent you, I am using
the sign-magnitude mode, with 2 separate signals needed from
the PWM and DIR
*/

 const int DIR1 = 27;
 const int PWM1 = 3;
   const int DIR2 = 28; 
 const int PWM2 = 4;
 float DSENSE = 23; 
 
 void setup() {
  // put your setup code here, to run once:
  
  //WHEELS  
  //wheel 1
  pinMode(DIR1, OUTPUT); //direction
  pinMode(PWM1, OUTPUT); //power
  
  //wheel 2
  pinMode(DIR2, OUTPUT); //direction
  pinMode(PWM2, OUTPUT); //power

  //sensors
  pinMode(DSENSE, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
/*
  //TEST for both wheels to run forward at 100 for 1s and then
  //run backwards for 1s
motor1(100); //motor 1 positive is forward
motor2(-100); //motor 2 negative is forward
delay(1000); 
motor1(-100);
motor2(100);
delay(1000);
*/

  //TEST for the robot to move backwards if it senses something
  //within 5cm;
int distance = digitalRead(DSENSE); 
  //ultra-short sensor output is 0 if object is within nominal 2cm to 10cm
  //sensor output is 1 if space is detected
Serial.print(distance);
Serial.print("\n");
if (distance == 0){
  motor1(-50);
  motor2(50);
  delay(1000);
}
else if (distance == 1) {
  motor1(50);
  motor2(-50);
 }


}

//motor functions
void motor1 (int speed1){
  motorWrite(speed1, DIR1, PWM1);
}

void motor2 (int speed2){
  motorWrite(speed2, DIR2, PWM2);
}

void motorWrite(int motorSpeed, int DIRx, int PWMx)
{
  if (motorSpeed > 0) //it's forward
  { digitalWrite(DIRx, HIGH);
  }
  if (motorSpeed < 0) //it's reverse
  { digitalWrite(DIRx, LOW);
  }

  motorSpeed = abs(motorSpeed);
  motorSpeed = constrain (motorSpeed, 0, 255);
  analogWrite(PWMx, motorSpeed);
}
