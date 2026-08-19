from machine import Pin, PWM


class Motor:      
    def __init__(self, pin1, pin2, pwm=False):
        self.max_duty_cycle = 65535
        self.frequency = 500
        self.pwm = pwm
        if self.pwm:
            self.pin1 = PWM(Pin(pin1))
            self.pin1.freq(self.frequency)
            self.pin1.duty_u16(0)
            self.pin2 = PWM(Pin(pin2))
            self.pin2.freq(self.frequency)
            self.pin1.duty_u16(0)
        else:
            self.pin1 = Pin(pin1, Pin.OUT)
            self.pin2 = Pin(pin2, Pin.OUT)

    def forward(self, speed = 1):
        if self.pwm:
            self.pin1.duty_u16(0)
            self.pin2.duty_u16(int(self.max_duty_cycle * speed))
        else:
            self.pin1.off()
            self.pin2.on()
    
    def backward(self, speed = 1):
        if self.pwm:
            self.pin1.duty_u16(int(self.max_duty_cycle * speed))
            self.pin2.duty_u16(0)
        else:
            self.pin1.on()
            self.pin2.off()

    def stop(self):
        if self.pwm:
            self.pin1.duty_u16(0)
            self.pin2.duty_u16(0)
        else:        
            self.pin1.off()
            self.pin2.off()
