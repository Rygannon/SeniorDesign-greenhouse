
#include<DHTesp.h>

// pin declarations
#define DHT11PIN 4 
#define SOILMOISTUREAO A0  
#define SOILMOISTUREDO 0
#define LIQUIDLEVEL A1

// temperature and humidity globals
DHTesp dht11; //initialize sensor
TempAndHumidity dht11Data; //data from sensor put into TempAndHumidity struct (


// read dht sensor
float DhtRead(char TorH) {
  // collect temperature and humidity data
  dht11Data = dht11.getTempAndHumidity();

  // check if we want temp or humidity and return the value
  if(TorH == 'T'){
    return dht11Data.temperature; // check this cuz struct is weird
  }
  else if(TorH == 'H'){
    return dht11Data.humidity; // check this cuz struct is weird
  }
  // return null if there was an issue
  return NAN;
}


// read the soil moisture sensor
int SoilMoistureRead(){
  int soilMoisture = analogRead(SOILMOISTUREAO);
  return soilMoisture;
}

int LiquidLevelRead(){
  int liquidLevel = analogRead(LIQUIDLEVEL);
  return liquidLevel;
}

void setup() {
   // temperature and humidity setup
  dht11.setup(DHT11PIN, DHTesp::DHT11);
  delay(1500); //The DHT sensor needs one second after power on before recieving any instructions
  
  // serial setup
  Serial.begin(9600);
}

  
void loop() {
  delay(100);
  // check for data on serial
   if(Serial.available() > 0){
    String rc = Serial.readString();
    
    // temperature request
    if (rc == "T"){
      //confirm request
      Serial.print("T");
      delay(100);
      //collect temperature data and send as string
      Serial.println(String(DhtRead('T')));
      
    }
    // humidity request
    else if(rc == "H"){
      //confirm request
      Serial.print("H");
      delay(100);
      // collect humidity data and send as string
      Serial.println(String(DhtRead('H')));
    }
    // soil moisture request
    else if(rc == "M"){
      //confirm request
      Serial.print("M");
      delay(100);
      // collect soil moisture data and send as string
      Serial.println(String(SoilMoistureRead()));
    }
    // liquid level request
    else if(rc == "L"){
      // confirm request
      Serial.print("L");
      delay(100);
      // collect liquid level data from pond and send as string
      Serial.println(String(LiquidLevelRead()));
   }
    // invalid request
    else{
      Serial.println("Request Not Valid");
    }
  }
}
