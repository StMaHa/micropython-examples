from machine import Pin, PWM


class Motor:      
    def __init__(self, pin1, pin2, pwm=true):
        self.max_duty_cycle = 1023
        self.pwm = pwm
        if self.pwm:
            self.pin1 = PWM(Pin(pin1), freq=500, duty=0)
            self.pin2 = PWM(Pin(pin2), freq=500, duty=0)
        else:
            self.pin1 = pin1
            self.pin2 = pin2

    def forward(self, speed = 1):
        if self.pwm:
            self.pin1.duty(0)
            self.pin2.duty(max_duty_cycle * speed)
        else:
            self.pin1.value(0)
            self.pin2.value(1)
    
    def backwards(self, speed = 1):
        if self.pwm:
            self.pin1.duty(max_duty_cycle * speed)
            self.pin2.duty(0)
        else:
            self.pin1.value(1)
            self.pin2.value(0)

    def stop(self):
        if self.pwm:
            self.pin1.duty(0)
            self.pin2.duty(0)
        else:        
            self.pin1.value(0)
            self.pin2.value(0)
