import image
import lcd
import sensor
import sys
import time
import utime
from board import board_info
import KPU as kpu
from Maix import GPIO
from fpioa_manager import *
from pmu import axp192
from machine import I2C
#pmu = axp192() - breaks IMU data -
#pmu.enablePMICSleepMode(True) - breaks IMU data -

i2c = I2C(I2C.I2C0, freq=400000, scl=28, sda=29)
#devices = i2c.scan()
lcd.init()

# IMU6866 define
MPU6886_ADDRESS=0x68
MPU6886_WHOAMI=0x75
MPU6886_ACCEL_INTEL_CTRL=0x69
MPU6886_SMPLRT_DIV=0x19
MPU6886_INT_PIN_CFG=0x37
MPU6886_INT_ENABLE=0x38
MPU6886_ACCEL_XOUT_H=0x3B
MPU6886_TEMP_OUT_H=0x41
MPU6886_GYRO_XOUT_H=0x43
MPU6886_USER_CTRL= 0x6A
MPU6886_PWR_MGMT_1=0x6B
MPU6886_PWR_MGMT_2=0x6C
MPU6886_CONFIG=0x1A
MPU6886_GYRO_CONFIG=0x1B
MPU6886_ACCEL_CONFIG=0x1C
MPU6886_ACCEL_CONFIG2=0x1D
MPU6886_FIFO_EN=0x23

# IMU6866 Initialize
def write_i2c(address, value):
    i2c.writeto_mem(MPU6886_ADDRESS, address, bytearray([value]))
    time.sleep_ms(10)

write_i2c(MPU6886_PWR_MGMT_1, 0x00)
write_i2c(MPU6886_PWR_MGMT_1, 0x01<<7)
write_i2c(MPU6886_PWR_MGMT_1,0x01<<0)
write_i2c(MPU6886_ACCEL_CONFIG,0x10)
write_i2c(MPU6886_GYRO_CONFIG,0x18)
write_i2c(MPU6886_CONFIG,0x01)
write_i2c(MPU6886_SMPLRT_DIV,0x05)
write_i2c(MPU6886_INT_ENABLE,0x00)
write_i2c(MPU6886_ACCEL_CONFIG2,0x00)
write_i2c(MPU6886_USER_CTRL,0x00)
write_i2c(MPU6886_FIFO_EN,0x00)
write_i2c(MPU6886_INT_PIN_CFG,0x22)
write_i2c(MPU6886_INT_ENABLE,0x01)

# Read IMU6866 and Scaling
def read_imu():
    aRes=255/4096/2
    gRes = 2000.0/32768.0
    offset=128
    accel = i2c.readfrom_mem(MPU6886_ADDRESS, MPU6886_ACCEL_XOUT_H, 6)
    accel_x = (accel[0]<<8|accel[1])
    accel_y = (accel[2]<<8|accel[3])
    accel_z = (accel[4]<<8|accel[5])
    if accel_x>32768:
        accel_x=accel_x-65536
    if accel_y>32768:
        accel_y=accel_y-65536
    if accel_z>32768:
        accel_z=accel_z-65536
    ax=int(accel_x*aRes+offset)
    if ax<0: ax=0
    if ax>255: ax=255
    ay=int(accel_y*aRes+offset)
    if ay<0: ay=0
    if ay>255: ay=255
    az=int(accel_z*aRes+offset)
    if az<0: az=0
    if az>255: az=255
    accel_array = [ax,ay,az]
    gyro = i2c.readfrom_mem(MPU6886_ADDRESS, MPU6886_GYRO_XOUT_H, 6)
    gyro_x = (gyro[0]<<8|gyro[1])
    gyro_y = (gyro[2]<<8|gyro[3])
    gyro_z = (gyro[4]<<8|gyro[5])
    if gyro_x>32768:
        gyro_x=gyro_x-65536
    if gyro_y>32768:
        gyro_y=gyro_y-65536
    if gyro_z>32768:
        gyro_z=gyro_z-65536
    gx=int(gyro_x*gRes+offset)
    if gx<0: gx=0
    if gx>255: gx=255
    gy=int(gyro_y*gRes+offset)
    if gy<0: gy=0
    if gy>255: gy=255
    gz=int(gyro_x*gRes+offset)
    if gz<0: gz=0
    if gz>255: gz=255
    gyro_array = [gx,gy,gz]
    return accel_array, gyro_array


lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.run(1)
lcd.clear()
while(True):
    accel_array,gyro_array = read_imu()
    img = sensor.snapshot()
    lcd.display(img)
    lcd.draw_string(40, 20, str(accel_array))
    lcd.draw_string(40, 40, str(gyro_array))
sys.exit()
