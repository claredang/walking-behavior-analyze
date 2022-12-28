# Analyze walking behavior to discover and prevent injuries

Calculates the walking asymmetry % in custom time with the exported csv files from the Physics Toolbox Sensor Suite app

## How to use

With 2 phones that have the Physics Toolbox Sensor Suite app ([iOS](https://apps.apple.com/us/app/physics-toolbox-sensor-suite/id1128914250)) ([Android](https://play.google.com/store/apps/details?id=com.chrystianvieyra.physicstoolboxsuite&hl=en_CA&gl=US)) installed, place a phone in each of your 2 front pockets and press record on the "Linear Accelerometer" portion of the app. Walk for at least 1 minute and press stop when you are finished. The 2 csv files will need to be moved to the computer with this python program installed, and can be run with the following commands:

Regular usage:

- python3 main.py \{path to left leg's csv file} \{path to right leg's csv file}

Compare with Apple Health result:

- python3 main.py \{path to left leg's csv file} \{path to right leg's csv file} \{apple health xml file}

Results will be displayed as output in the console, and a plot of the accelerations will be shown in a popup window

## Example usage

python3 main.py data/1-l.csv data/1-r.csv

python3 main.py data/2-l.csv data/2-r.csv data/export-1.xml

## To share your Apple Health data in XML format

https://support.apple.com/en-ca/guide/iphone/iph5ede58c3d/ios

## Required Python libraries

pandas

matplotlib
