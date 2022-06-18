# Dynamic analysis tool of Android applications to extract spam Caller-IDs

*This research is part of the [Research Project 2022](https://github.com/TU-Delft-CSE/Research-Project) of [TU Delft](https://https//github.com/TU-Delft-CSE).*

## Short description of research & tool
Spam calls are becoming an increasing problem, with people receiving multiple spam calls per month on average. Multiple Android Applications exist that are able to detect spam calls and display a warning or block such calls. Little is known however on how these applications work and what numbers they block.
In this research, the following question is investigated: Can we do a brute force dynamic analysis on Android spam call blocking apps, to extract Caller-ID information from apps that cannot be or is not extracted through static analysis?
A tool is created that is capable of doing such a dynamic analysis, by installing multiple android apps (one at a time) on an emulator, sending emulated phone calls to the emulator, and using screenshot comparison techniques to determine whether the call is classified as allowed or blocked by the respective app. 
This fully automated tool can test Caller-IDs on 8 different Android apps. Apart from a number of initial setup steps to install and configure the apps in the emulator, the tool takes about 1.5 seconds on average to analyze 1 Caller-ID on one app.

## Usage: 

First install appium, it can be installed directly from NPM:
```
npm install -g appium
```

Then install OpenCV for Node, which is required for image comparison functions. [Detailed instructions can be found here](https://github.com/justadudewhohacks/opencv4nodejs#how-to-install)
```
npm install --save opencv4nodejs
```

Finally, you need to set up the emulators needed to run the analysis on. In [helper-scripts/base_emulator](helper-scripts/base_emulator/) you can find the optimal configuration of the emulator. It is adviced to use the helper script [helper-scripts/create-emulators.sh](helper-scripts/create-emulators.sh) to generate 10 emulators. You will then be able to run with a maximum of 10 threads. 
```
sh helper-scripts/create-emulators.sh
```


Then you can run the tool, using this syntax. The tool takes a list of numbers, one per line. An example can be found in [results/100-numbers.txt](results/100-numbers.txt). You can specify the file name as an argument or else the tool will read input from `stdin`.


```shell
python3 main.py  
    --google_username=YOUR_USERNAME_OR_EMAIL 
    --google_password=YOUR_PASSWORD
    --headless 
    --threads=1
    number-list.txt
```

### Detailed usage:
```
usage: main.py [-h] --google_username GOOGLE_USERNAME --google_password GOOGLE_PASSWORD [--headless] [--print_csv_lines] [--save_screenshots] [--threads THREADS] [infile]

Test numbers on Android Spam Call Blocking Applications

positional arguments:
  infile                Input file containing phone numbers, one per line

optional arguments:
  -h, --help            show this help message and exit
  --google_username GOOGLE_USERNAME
                        A google account's username
  --google_password GOOGLE_PASSWORD
                        A google account's password
  --headless            Run the emulator headless
  --print_csv_lines     Print the csv lines as they are generated by the tool
  --save_screenshots    Save the screenshots that are used for image comparison to the out/ folder
  --threads THREADS     The number of threads you want the tool to use
```

## Results
Example raw results can be found in the [results](results/) folder. These include a list of 100 numbers and the result of running the tool on this number list. 

## List of apps (+ used versions)
| Image                                                                                                               | Package ID                              | Name                                               | Version Name | Version Code |
| ------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | -------------------------------------------------- |--------------|--------------|
| ![](https://play-lh.googleusercontent.com/csDVvK9qQ2LXkhHmdUcV2A_GmJFSG-hHR4j1NSbbfLCPbyUD-yZsfdP1o_ztXVZ6vu8=s80)  | com.flexaspect.android.everycallcontrol | Call Control - SMS/Call Blocker. Block Spam Calls! | 2.2.8        | 272          |
| ![](https://play-lh.googleusercontent.com/v2dikPLxEt4uvoxTLTMqiCmOjP-Cc8yX6oNffyrSJmt0557RFyhyW7I5i1CxN8CJaQ=s80)   | com.callapp.contacts                    | CallApp: Caller ID & Recording                     | 1.962        | 1962         |
| ![](https://play-lh.googleusercontent.com/sCjUstQ7Jxe0p7rit4VmytmYAtLRgwJEYKOKcGNDSxnA_pYqI8hbGCyg8d_nAK6Y_A=s80)   | com.unknownphone.callblocker            | Call Blocker - Stop spam calls                     | 1.7.7        | 184          |
| ![](https://play-lh.googleusercontent.com/J7lc1iCnMWL0iK17QhgCXJ0JPTdTvr9PwMvHs-3f61cGhGLGqawT9k2XrfoCsjMjeA=s80)   | com.callerid.block                      | Caller ID, Phone Dialer, Block                     | 2.13.5       | 40155        |
| ![](https://play-lh.googleusercontent.com/NLEQ0dghITECObk6bmtnKmOV01AhSsh9O08qz_0VF75v-cBkbLIVQs-bibIWgK-kbmM=s80)  | org.mistergroup.shouldianswer           | Should I Answer?                                   | 2.3.21       | 382          |
| ![](https://play-lh.googleusercontent.com/SyqUM3cu-XL0w98qPSurxMRBlz7eOyQ_6iIN5EF9XxmHkz1nnNTQd3gG4tTtoD9tEBpe=s80) | com.allinone.callerid                   | Showcaller: Caller ID & Block                      | 1.1.1        | 791          |
| ![](https://play-lh.googleusercontent.com/llSnaRWfU9XQNoA-RJYrAt6asjpXuHaLFdt18CLa_zszbCNdemIHr8LCGJCWNVPucqZ9=s80) | com.mglab.scm                           | Stop Calling Me - Call Blocker                     | 12.30.6      | 1230006      |
| ![](https://play-lh.googleusercontent.com/dkJUZvWBAsR5LATWAvOow3yMgRi7-zsS6a9t6rYhkR8a9ylti1xK9mLrHUGm8Y8cF_o=s80)  | com.telguarder                          | Spam Call Blocker - telGuarder                     | 2.6.4        | 147          |
| ![](https://play-lh.googleusercontent.com/64ap3L-g_bp4j3Abt3fsY_N1K8J6zbhUIlYfeUNgIrV9JSRwU5D7VJ-PUjST-rd84g=s80)   | com.truecaller                          | Truecaller: Caller ID & Block                      | 12.1.0-9677  | 120100       |
| ![](https://play-lh.googleusercontent.com/0w58zzstVGY4rAbG2IBe7lSW4MHw79a-8v0SOEkHLc7tYe2E6XE6Kdawug6agWgbJg=s80)   | com.webascender.callerid                | Hiya - Call Blocker, Fraud Detection & Caller ID   | 1.0.206      | 206          |