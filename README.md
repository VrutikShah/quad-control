# Quadcotper Control using Python

1. ~~fix rotation scale issue~~
2. ~~fix linear + rotation issue~~
3. ~~thrust based movement~~
4. ~~add gravity~~
5. unequal thrust - rotation
6. fix quad trail
7. Start P I D control
    1. Write PID for translation only - using u1
    2. Test vertical control
    3. Add another PID loop for u2
    4. determine F1 and F2 using that

each PID Loop is supposed to take the current coordinates as input and calculate error wrt destination coordinates. Then 