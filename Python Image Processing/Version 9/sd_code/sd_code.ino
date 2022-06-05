#include <SPI.h>
#include <SD.h>

/*
 * MOSI - 11
 * MISO - 12
 * CLK
 * 
 */

File myFile;

void basicExample() {
  Serial.begin(9600);
  while(!Serial) {}

  Serial.print("Loading SD card... ");

  if (!SD.begin(4)) {
    Serial.println(" Failed :(");
    while (1);
  }
  Serial.println(" Success!");

  myFile = SD.open("test.txt", FILE_WRITE);

  // If file opens correctly
  if (myFile) {
    Serial.print("Writing to test.txt...");
    myFile.println("Testing...");
    myFile.println("1, 2, 3");
    myFile.close();
    Serial.println(" Done!");
  } 
  else {
    Serial.println("Error opening test.txt");
  }

  myFile = SD.open("test.txt");
  if (myFile) {
    Serial.println("Contents of test.txt:");

    while (myFile.available()) {
      Serial.write(myFile.read());
    }

    myFile.close();
  }
  else {
    Serial.println("Error opening test.txt");
  }
}

void numericReadTest() {
  Serial.begin(9600);
  while(!Serial) {}

  Serial.print("Loading SD card... ");

  if (!SD.begin(4)) {
    Serial.println(" Failed :(");
    while (1);
  }
  Serial.println(" Success!");

  unsigned int a;

  myFile = SD.open("NUM.TXT");
  if (myFile) {
    
    while (myFile.available()) {
      a = (unsigned int) myFile.read();
      Serial.print(a);
      Serial.print(", ");
      Serial.println(a + 1);
    }

    myFile.close();
  }
  else {
    Serial.println("Error opening file");
  }
}

void numericWriteTest() 
{
  Serial.begin(9600);
  while(!Serial) {}

  Serial.print("Loading SD card... ");

  if (!SD.begin(4)) 
  {
    Serial.println(" Failed :(");
    while (1);
  }
  Serial.println(" Success!");

  SD.remove("writeData.txt");
  
  myFile = SD.open("WRITE.TXT", FILE_WRITE);

  // If file opens correctly
  if (myFile) 
  {
    Serial.print("Writing...");
    myFile.write(0xAAAA);
    myFile.write(0x1000);
    myFile.write(0x0001);
    myFile.write(0x1234);
    myFile.close();
    Serial.println(" done.");
  } 
  else 
  {
    Serial.println("Error opening file");
  }

  unsigned int a[4];
  unsigned int index = 0;

  myFile = SD.open("WRITE.TXT");
  if (myFile) {
    Serial.println("Contents of test.txt:");

    while (myFile.available()) {
      a[index++] = myFile.read(a, 4);
      Serial.print("index = ");
      Serial.println(index);
      for (unsigned char i = 0; i < 4; i++) {
        Serial.println(a[i]);
      }
//      Serial.write(myFile.read());
    }

    myFile.close();
  }
  else 
  {
    Serial.println("Error opening test.txt");
  }

//  for (unsigned char i = 0; i < 4; i++) {
//    Serial.println(a[i]);
//  }
}
void pngRead() {
  Serial.begin(9600);
  while(!Serial) {}

  Serial.print("Loading SD card... ");

  if (!SD.begin(4)) {
    Serial.println(" Failed :(");
    while (1);
  }
  Serial.println(" Success!");

//  myFile = SD.open("test.txt", FILE_WRITE);
//
//  // If file opens correctly
//  if (myFile) {
//    Serial.print("Writing to test.txt...");
//    myFile.println("Testing...");
//    myFile.println("1, 2, 3");
//    myFile.close();
//    Serial.println(" Done!");
//  } 
//  else {
//    Serial.println("Error opening test.txt");
//  }

  myFile = SD.open("out.png");
  if (myFile) {
    Serial.println("Contents of out.png:");

    while (myFile.available()) {
      Serial.write(myFile.read());
    }

    myFile.close();
  }
  else {
    Serial.println("Error opening out.png (I mean, what were you expecting?)");
  } 
}

void setup() {
//  basicExample();
  numericReadTest();
//  numericWriteTest();
//  pngRead();
}

void loop() {
  
}
