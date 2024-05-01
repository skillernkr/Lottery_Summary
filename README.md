Lottery_Summary.py

Purpose:
  Chart colormapped histograms of balls drawn for Powerball and Megamillions lottery games in selected date range or on specific dates.
  Read history from local file or from internet with option to save.

Instructions:
  Run python3 file.
  In console, program will prompt user which lottery game is to be used.
  Then it will ask for a data source, either a local file (such as 'Powerball\Powerball.csv') or internet data from www.texaslottery.com.
  If internet data is selected, it will ask if the data should be saved to a local file.
  Next, the program uses numpy and matplotlib to generate a chart of histograms.
  Sliders along the top allow the selection of either a date range (top left) or a specific date (top right) to be displayed.
  Color mapped bars correspond to the frequency of each ball.
  
Comments:
  I put this together as an open source project for fun.  
  Please feel free to suggest changes or fork into new branches to increase functionality.
