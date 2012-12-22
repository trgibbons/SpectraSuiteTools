#!/usr/bin/env python

# Written by Ted Gibbons (tgibbons@umd.edu)
# Winter 2012

import sys
import os
import re





# This function initializes the table with row names from the first file
def initializeTable(directory, filename):

  # This "table" variable is different than the one I created within main(), and will soon replace it
  table = [["Filename", filename]]

  # I use this variable to track my position within the file
  segment = "pre"

  # Open the file for reading and iterate through each line
  for line in open(os.path.join(directory, filename), "r"):

    # The header section is prefixed by a line of '+'s
    if line[0] == "+":
      segment = "header"

    # There are lines on either side of the data containing a bunch of chevrons
    elif line[0] == ">":

      # The first time, we start storing data
      if segment == "header":
        segment = "data"

      # The second time, we're done with the file and can move on
      elif segment == "data":
        break

    # Store the next header line, creating an labeled row for that field
    elif segment == "header":
      temp = line.rstrip().split(": ")
      table.append([temp[0], temp[1]])

    # Store the next data line, creating a labeled row for that wavelength
    elif segment == "data":
      temp = line.rstrip().split()
      table.append([temp[0], temp[1]])

  # Send the new table back to the main() function
  return table





# This function adds new data to the table, and attempts to check for some basic consistency along the way
def growTable(table, directory, filename):

  # This "table" variable is different than the one I created within main(), and will soon replace it
  table[0].append(filename)

  # I use this variable to track my position within the file
  segment = "pre"
  i = 0

  # Open the file for reading and iterate through each line
  for line in open(os.path.join(directory, filename), "r"):

    # The header section is prefixed by a line of '+'s
    if line[0] == "+":
      segment = "header"

    # There are lines on either side of the data containing a bunch of chevrons
    elif line[0] == ">":

      # The first time, we start storing data
      if segment == "header":
        segment = "data"

      # The second time, we're done with the file and can move on
      elif segment == "data":
        break

    # Store the next header line, creating a labeled row for that field
    elif segment == "header":
      temp = line.rstrip().split(": ")
      i += 1
      table[i].append(temp[1])
      if temp[0] != table[i][0]:
        sys.stderr.write("Headers between files "+str(filename)+" and "+str(table[0][1])+" do not appear to match.\n"+ \
                         "You have been warned.\n")

    # Store the next data line, creating a labeled row for that wavelength
    elif segment == "data":
      temp = line.rstrip().split()
      i += 1
      table[i].append(temp[1])
      if temp[0] != table[i][0]:
        sys.stderr.write("Wavelengths between files "+str(filename)+" and "+str(table[0][1])+" do not appear to match.\n"+ \
                         "You have been warned.\n")

  # Send the updated table back to the main() function
  return table




# This prints the table to the output file
def printTable(table, outFile):

  # Open the output file
  outHandle = open(outFile, "w")

  # Print the table to the output file
  for i in range(len(table)):
    tempOut = str(table[i][0])
    for j in range(1,len(table[i])):
      tempOut += "\t"+str(table[i][j])
    outHandle.write(tempOut+"\n")

  # We opened this file explicitely, so it's only responsible to close it again
  outHandle.close()





# This is where all the magic happens
def main(argv=None):
  if argv == None:
    argv = sys.argv

  # Directory containing input files
  directory = argv[1]

  # Start a little progress message for the user
  sys.stdout.write("\nLooking for input files in:\n"+ \
                   "  "+str(directory)+"\n"+ \
                   "Importing files:\n")

  # Create a temporary dummy variable to catch the initial boundary condition
  table = ''

  # Iterate through each file in the specified directory, adding it to a growing table
  for filename in os.listdir(directory):

    # Skip any non-SpectraSuite output files
    if re.match('[A-Z][0-9]{3}\.txt', filename):

      # Continue progress message for the user
      sys.stdout.write("  "+str(os.path.join(directory, filename))+"\n")

      # Use the first file to initialize the row labels
      if table == '':
        table = initializeTable(directory, filename)
      else:
        table = growTable(table, directory, filename)

  # Select a file for output
  if len(argv) > 2:
    outFilename = argv[2]
  else:
    outFilename = os.path.join(str(directory), "combinatized.txt")

  # Continue progress message for the user
  sys.stdout.write("Writing output to:\n"+ \
                   "  "+str(outFilename)+"\n")

  # Print the table to the output file
  printTable(table, outFilename)

  # Alert user that the program has completed
  sys.stdout.write("Finished!\n\n")





# Executing the main function this way allows the script to be called repeatedly
# in an interactive shell without closing the session
if __name__ == "__main__":
  sys.exit(main())

