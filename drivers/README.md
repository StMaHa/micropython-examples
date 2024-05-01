# Drivers

## BMP180 Barometric Pressure/Temperature/Altitude Sensor

## HC-SR04 ultrasonic distance sensor

## Motor driver

## Servo - turning by angle
How to calculate the angle?  

E.g.: **0.001s**<sub>(y1)</sub> **... 0.002s**<sub>(y2)</sub> 🠲 **0°**<sub>(x1)</sub> **... 180°**<sub>(x2)</sub>  

$$
\begin{flalign}
 & \\
 &y = mx + b  🠲  \mathbf{pulselength = m * angle + b} \\
 & \\
 &y1 = m x1 + b  🠲  b = y1 - m x1 \\
 &y2 = m x2 + b  🠲  b = y2 - m x2 \\
 & \\ 
 &y1 - m x1 = y2 - m x2 && \\
 & \\
 &y1 = y2 + m (x1 - x2) \\
 &y1 - y2 = m (x1 - x2) \\
 & \\
 &m = (y1 - y2) : (x1 - x2)  🠲  \mathbf{m = \frac{y1 - y2}{x1 - x2}} \\
 & \\
 &b = y1 - mx1  🠲  \mathbf{b = y1 - x1\frac{y1 - y2}{x1 - x2}} \\
 & \\
 &🠲   x1 = 0 \\
 &🠲   b = y1  🠲  b = 0.001s = 1ms \\
 &🠲   m = \frac{y2 - y1}{x2} = \frac{0.002s - 0.001s}{180°} = 0.0056 \frac{ms}{°}
\end{flalign}
$$


# LICENSE
See the [LICENSE](LICENSE) file for license rights and limitations.
Submodules might have a different license.
