
#include <Wire.h>
#include <LIDARLite.h>

LIDARLite Lidar0;

void setup()
{
  // Initialize serial connection to display distance readings
  Serial.begin(115200);

  // Set configuration to default and I2C to 400 kHz
  Lidar0.begin(0, true, 0x96);
  Lidar0.configure(0);

}

void loop()
{
  Serial.println(String(Lidar0.distance()));
}

int readLIDAR(LIDARLite lidar)
{
  // Take a measurement with receiver bias correction
  lidar.distance();
  
  float average_distance = 0;

  for(int i = 0; i < 10; i++)
  {
    average_distance += float(lidar.distance(false));
  }

  // Take a measurements without receiver bias correction and print to serial terminal
  return(int(average_distance / 10));
}
