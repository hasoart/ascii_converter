@ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ * , . , ! @ @ @ @ @ 
@ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ $ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ # : . . : $ @ @ @ @ @ @ 
@ @ @ @ @ @ @ $ @ @ @ @ @ @ @ @ # - . . ~ # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ $ = ~ . . . : @ @ @ @ @ @ @ @ 
@ @ @ @ @ @ @ : $ @ @ @ @ @ @ @ ~ , = ~ . , $ @ @ @ @ # = # $ @ @ @ @ @ @ @ @ @ $ * ; * @ ; . . , ~ . : @ @ @ @ @ @ @ @ 
@ @ @ @ @ @ @ ~ * @ @ @ @ @ @ # . = @ @ ; . * @ @ @ ! . . . - $ @ @ $ # * ! ; ~ . . : # @ # * # @ $ , : @ @ @ @ @ @ @ @ 
@ @ @ @ @ @ @ - * @ @ @ @ @ @ = ~ @ @ @ * . $ @ @ = . = @ = . ; @ @ = . . . . , ; * @ @ @ @ @ @ @ @ - : @ @ @ @ @ @ @ @ 
@ @ @ @ @ @ $ , = @ @ @ @ @ @ = : @ @ @ ! . @ @ $ , - @ @ @ - : @ @ $ * * ! . # @ @ @ @ @ @ @ @ @ @ ~ : @ @ @ @ @ @ @ @ 
@ @ @ @ @ @ * , , $ @ @ @ @ @ ! , $ @ @ # = @ @ ; . # @ @ @ : : @ @ @ @ @ * . # @ @ @ @ @ @ @ @ @ @ : : @ @ @ @ @ @ @ @ 
@ @ @ @ @ @ : * , # @ @ @ @ @ @ - ~ @ @ @ @ @ @ , - @ @ @ @ # * @ @ @ @ @ - . @ @ @ @ @ @ @ @ @ @ @ : : @ @ @ @ @ @ @ @ 
@ @ @ @ @ $ , @ - = @ @ @ @ @ @ # . : $ @ @ @ ! . ; @ @ @ @ @ @ @ @ @ @ @ , . @ @ @ @ @ @ @ @ @ @ @ : : @ @ @ @ @ @ @ @ 
@ @ @ @ @ ! ~ @ ~ : $ : ! @ $ @ @ ; . = @ @ @ : . = @ @ @ @ @ @ @ @ @ @ @ . . @ @ @ @ @ @ @ @ @ @ @ - ; @ $ = # @ @ @ @ 
@ @ @ @ $ ~ : * : . . : $ @ @ $ @ $ , , $ @ @ - . = @ @ @ @ @ @ @ @ @ @ # . ~ @ @ @ @ @ @ @ @ @ @ $ . - $ - , $ @ @ @ @ 
@ @ @ $ ; . . . . . = $ @ @ @ @ @ @ * . = @ @ - . = @ @ @ @ @ @ @ @ @ @ ; . = @ @ @ @ @ @ @ @ @ @ = . , , . * @ @ @ @ @ 
@ = : . . . : # $ , = @ @ @ $ @ @ @ @ ~ ; @ @ - . = @ @ @ $ * @ @ @ @ @ - . # @ @ @ @ @ @ @ # = - . . . - $ @ @ @ @ @ @ 
@ @ @ * , * @ @ @ : ~ @ @ @ - ! $ @ @ ; : @ @ - . = @ @ $ ; = @ @ @ @ # . - @ @ @ @ @ @ $ ~ . . . . . ; $ @ @ @ @ @ @ @ 
@ @ * , # @ @ @ @ ; . * @ @ = . , : : . = @ @ - . - = = ~ . # @ @ @ @ * . ! @ @ @ @ @ @ * : : : ; = # @ @ @ @ @ @ @ @ @ 
$ ; , * @ @ @ @ @ $ - - @ @ @ * : , . . * @ @ ~ . . . . . ! @ @ @ @ @ ; . : : : ! @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 
$ : $ @ @ @ @ @ @ @ @ $ @ @ @ @ @ @ @ @ @ @ @ ! . . . . : @ @ * ; ~ - . . . . - * @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 
@ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ * - - ; $ @ @ = - - : ; = ! $ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 
@ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @

ASCII video converter by hasoart

Make sure you have all the necessary packages installed
Necessary packages are listed in the requirements.txt
(If you want to install the packages you can use 'pip install -r requirements.txt' in your terminal)

To use the program run the main.py.
After running it you'll see 4 options.
  1. Real time printer
     This program will convert and play the video you want at real time.
     In the settings you can specify conversion parameters, playback framerate, the color scheme you want,
     video volume and timeout, which will tell the program how long to wait before starting the program.
     NOTE. audio can be played only at it's original speed, thus if you want to have audio I recommend you setting
           the framerate option to 'auto'
     NOTE. if you feel that audio/video starts playing earlier and there is desync between them, I recommend to
           increase timeout, which will give time for the program to read the video and audio from your system.
     WARNING. if the converted width/height and/or framerate are above some threshold(depends on your setup) you will
              start seeing that video isn't played at proper framerate. In this case you will see repeating messages in
              your terminal that significant delay is registered(1 or 2 messages aren't critical, as long as there
              is no rain of messages avery frame). In this case you need to lower framerate and/or converted
              width/height.
  2. Convert video to frames
     This program will convert the video you choose to frames.
     In the settings you can specify conversion parameters(especially use them if you want to save space on your disk).
     WARNING. converted frames take several times(even orders of magnitude) more space than the original video, thus
              make sure that you have enough space on your disk.
  3. Convert frames to ascii file
     This program will convert the frames you give to it into ascii art and store it in a txt file. Store location is
     '/Result_Files/'. Frames are separated by | symbol.
     In the settings you can specify conversion parameters.
     NOTE. if you want to convert regular pictures(not video frames) just put them in a folder and run the program
           on that folder. As a result you will have your pictures in a txt file, which you can as however you want.
     WARNING. as the results are stored in a txt file, there is no image compression, thus if your scale factor is
              close to 1 you may end up with massive file sizes. Make sure that you have enough space on your disk
              before doing it.
  4. Print from file
     This program will print the converted txt files which were generated by 'Convert frames to ascii file' program.
     In the settings you can specify playback framerate, the color scheme you want and timeout, which will tell the
     program how long to wait before starting the program.
     WARNING. if the converted width/height and/or framerate are above some threshold(depends on your setup) you will
         start seeing that video isn't played at proper framerate. In this case you will see repeating messages in
         your terminal that significant delay is registered(1 or 2 messages aren't critical, as long as there
         is no rain of messages avery frame). In this case you need to lower framerate and/or converted
         width/height.

Frequent error causes.
1. non-unicode file/directory paths will cause an error. Make sure that your file/directory paths contain only ascii
   characters.
2. outdated 'numba' version may be a cause of error in 'functions.py'