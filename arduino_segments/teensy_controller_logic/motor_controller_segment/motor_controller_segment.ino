void setup() {
  // put your setup code here, to run once:
//define the motor controller output pins
      //motor A = Right motor B = left
const int ADIR = 18;  //Analog and Digital pins
const int BDIR = 19;  //Analog and Digital pins
const int ASPEED = 20; //Analog, Digital, PWM pins
const int BSPEED = 21; //Analog, Digital, PWM pins

//set motor pin modes to OUTPUT
pinMode(ADIR, OUTPUT);
pinMode(BDIR, OUTPUT);
pinMode(ASPEED, OUTPUT);
pinMode(ASPEED, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
//write HIGH to ADIR digital pin and LOW to BDIR digital pin
pinMode(13, OUTPUT);

delay(300);
digitalWrite(13,HIGH);
delay(300);
digitalWrite(13,LOW);

}


