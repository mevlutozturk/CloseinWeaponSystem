

#define ENA   14          // Sag motor girisi                 GPIO14(D5)
#define ENB   12          // Sol motor girisi                 GPIO12(D6)
#define IN_1  15          // L298N in1 Sag motorlar           GPIO15(D8)
#define IN_2  13          // L298N in2 Sag motorlar           GPIO13(D7)
#define IN_3  2           // L298N in3 Sol motorlar           GPIO2(D4)
#define IN_4  0           // L298N in4 Sol motorlar           GPIO0(D3)

#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>

String Komut;             //Komut Gönderimi
int AracHizi = 800;         // 400 - 1023.
int speed_Coeff = 3;

const char* ssid = "NodeMCU Car";
ESP8266WebServer server(80);

void setup() {
 
 pinMode(ENA, OUTPUT);
 pinMode(ENB, OUTPUT);  
 pinMode(IN_1, OUTPUT);
 pinMode(IN_2, OUTPUT);
 pinMode(IN_3, OUTPUT);
 pinMode(IN_4, OUTPUT); 
  
  Serial.begin(115200);
  
// Wifi Baglanmasi

  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
 
 // Starting WEB-server 
     server.on ( "/", HTTP_handleRoot );
     server.onNotFound ( HTTP_handleRoot );
     server.begin();    
}

void İleriGit(){ 

      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, AracHizi);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, AracHizi);
  }

void GeriGit(){ 

      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, AracHizi);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, AracHizi);
  }

void SagaGit(){ 

      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, AracHizi);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, AracHizi);
  }

void SolaGit(){

      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, AracHizi);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, AracHizi);
  }

void Sagİleri(){
      
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, sAracHizi/speed_Coeff);
 
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, AracHizi);
   }

void Solİleri(){
      
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, AracHizi);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, AracHizi/speed_Coeff);
  }

void SagGeri(){ 

      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, AracHizi/speed_Coeff);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, AracHizi);
  }

void SolGeri(){ 

      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, AracHizi);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, AracHizi/speed_Coeff);
  }

void RobotDur(){  

      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, AracHizi);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, AracHizi);
 }

void loop() {
    server.handleClient();
    
      Komut = server.arg("Durum");
      if (Komut == "F") İleriGit();
      else if (Komut == "B") GeriGit();
      else if (Komut == "L") SolaGit();
      else if (Komut == "R") SagaGit();
      else if (Komut == "I") Sagİleri();
      else if (Komut == "G") Solİleri();
      else if (Komut == "J") SagGeri();
      else if (Komut == "H") SolGeri();
      else if (Komut == "0") AracHizi = 400;
      else if (Komut == "1") AracHizi = 470;
      else if (Komut == "2") AracHizi = 540;
      else if (Komut == "3") AracHizi = 610;
      else if (Komut == "4") AracHizi = 680;
      else if (Komut == "5") AracHizi = 750;
      else if (Komut == "6") AracHizi = 820;
      else if (Komut == "7") AracHizi = 890;
      else if (Komut == "8") AracHizi = 960;
      else if (Komut == "9") AracHizi = 1023;
      else if (Komut == "S") RobotDur();
}

void HTTP_handleRoot(void) {

if( server.hasArg("State") ){
       Serial.println(server.arg("Durum"));
  }
  server.send ( 200, "text/html", "" );
  delay(1);
}
