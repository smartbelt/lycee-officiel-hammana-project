import time
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import os
import email
import smtplib
def setupSpiPins(clk,miso,mosi,cs): 
        GPIO.setmode(GPIO.BOARD)
	GPIO.setup(clk,GPIO.OUT) 
	GPIO.setup(miso,GPIO.IN) 
	GPIO.setup(mosi,GPIO.OUT) 
	GPIO.setup(cs,GPIO.OUT)
        time.sleep(0.3)
        
def send_email(address, subject, body):
    msg = email.message_from_string(body)
    msg['From'] = "rpi_loh@hotmail.com"
    msg['To'] = address
    msg['Subject'] = subject
    s = smtplib.SMTP("smtp.live.com", 587)
    s.ehlo()
    s.starttls()
    s.login('rpi_loh@hotmail.com','loh321loh')
    s.sendmail("rpi_loh@hotmail.com",address,msg.as_string())
    s.quit()    

def ultrasonicReading() :
        GPIO.output(TRIG, False)
        time.sleep(1)
        GPIO.output(TRIG, True)
        time.sleep(0.01)
        GPIO.output(TRIG, False)
        signalOff = time.time()
        while GPIO.input(ECHO)==0:
                signalOff=time.time()

        while GPIO.input(ECHO)==1:
                signalOn=time.time()

        timePassed=signalOn-signalOff
        distance=timePassed*17150
        return distance
 #readadc function
def readadc(adcnum, clockpin, mosipin,misopin,cspin):
	if ((adcnum >7) or (adcnum<0)): 
		return -1
	GPIO.output(cspin,True) 
	GPIO.output(clockpin,False) 
	GPIO.output(cspin,False) 
	commandout = adcnum 
	commandout |= 0x18 
	commandout <<= 3
	for i in range(5):
		if (commandout & 0x80):
			GPIO.output(mosipin, True) 
		else:
			GPIO.output(mosipin,False) 
		commandout<<=1
		GPIO.output(clockpin,True)
		GPIO.output(clockpin,False) 
	adcout =0	
	for i in range(12): 
		GPIO.output(clockpin,True) 
		GPIO.output(clockpin,False) 
		adcout<<=1 
		if(GPIO.input(misopin)):
			adcout |= 0x1 
	GPIO.output(cspin,True)
	adcout >>=1 
	return adcout




GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

    


CLK = 23 
MISO = 21 
MOSI = 19 
CS = 26
TRIG = 8
ECHO = 10
setupSpiPins(CLK,MISO,MOSI,CS)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
distance = 50
try: 
        while True:
                time.sleep(1)
                readingDistance = ultrasonicReading()
                volt = readadc(1,CLK,MOSI,MISO,CS)
                temp = (volt /1024.0) *3300.0
                temp = temp/10.5
                h,t = dht.read_retry(dht.DHT11, 4)
                print 'Temp={0:01f}*C Humidity={1:0.1f}%'.format(t, h)
                print 'temperature is ',temp
                print 'distance is ',readingDistance
                print "\n\n\n\n"
                send = 0
                if 20<t:
                        send = (send +1)%3
                        if send == 0:
                                msg = "temperature : " + str(t) + "\n Temperature de .. : " + str(temp) + " \n distance : "+str(readingDistance)
                                send_email("maroun_sahyoun1999@hotmail.com","check your baby",msg)

                if  distance< readingDistance < distance + 30:
                        for i in range (3):
                                GPIO.output(15,GPIO.HIGH)
                                time.sleep(2)
                                GPIO.output(15,GPIO.LOW)
                                time.sleep(1) 
                if 10<temp <= 42 :
                        for i in range (3):
                                GPIO.output(15,GPIO.HIGH)
                                time.sleep(1)
                                GPIO.output(15,GPIO.LOW)
                                time.sleep(1)
                elif 42<temp<= 50:
                        for i in range (3):
                                GPIO.output(15,GPIO.HIGH)
                                time.sleep(0.5)
                                GPIO.output(15,GPIO.LOW)
                                time.sleep(0.5)
                elif temp >= 50:
                        GPIO.output(15,GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(15,GPIO.LOW)
                elif temp <= 10:
                        GPIO.output(15,GPIO.LOW)
                if h > 20 :
                        msg = "humidty : " + str(h) + "\n temperature : " + str(t) + "\n Temperature de .. : " + str(temp) + " \n distance : "+str(readingDistance)
                        send_email("maroun_sahyoun1999@hotmail.com","check your baby",msg)



except KeyboardInterrupt:
        GPIO.output(15,GPIO.LOW)


    




