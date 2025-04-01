# Maddison's 1st Ammendment Calculator

This project's goal is to present what it would look like if the original first ammendment that maddison proposed would have been ratified. What would the House of Representatives look like in this alternate universe?

I have taken the most recent census data, imported it and processed it state by state based on the formula Maddison provided to determine how many representatives each state would have today.

Please share and if you see any errors or improvements feel free to contribute.

You can also view this calculator live @ [www.kevinchriste.pythonanywhere.com](https://kevinchriste.pythonanywhere.com)

**From the Transcript of the 1789 Joint Resolution of Congress ("Original" 1st Ammendment)**
"After the first enumeration required by the first article of the Constitution, there shall be one Representative for every thirty thousand, until the number shall amount to one hundred, after which the proportion shall be so regulated by Congress, that there shall be not less than one hundred Representatives, nor less than one Representative for every forty thousand persons, until the number of Representatives shall amount to two hundred; after which the proportion shall be so regulated by Congress, that there shall not be less than two hundred Representatives, nor more than one Representative for every fifty thousand persons.

[" https://www.archives.gov/founding-docs/bill-of-rights-transcript](https://www.archives.gov/founding-docs/bill-of-rights-transcript)

**Formula:**  
The following formula is used to calculate the number of representatives per state.  
Where \(P\) is the state's population and \(R(P)\) is the number of representatives allocated to that state.

1. **For \( P \leq 3{,}000{,}000 \):**  
   \( R(P) = \left\lfloor \frac{P}{30\,000} \right\rfloor \)  
   (This gives one representative for every 30,000 people.)

2. **For \( 3{,}000{,}000 < P \leq 8{,}000{,}000 \):**  
   \( R(P) = \max\left(100,\ \left\lfloor \frac{P}{40\,000} \right\rfloor\right) \)  
   (In this range, a state gets at least 100 representatives, and thereafter one representative for every 40,000 people, up to 200 reps.)

3. **For \( P > 8{,}000{,}000 \):**  
   \( R(P) = \max\left(200,\ \left\lfloor \frac{P}{50\,000} \right\rfloor\right) \)  
   (For populations above 8,000,000, a state must have at least 200 representatives, but not more than one representative for every 50,000 people.)
