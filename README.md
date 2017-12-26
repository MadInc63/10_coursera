# Coursera Dump

The script collects information about the courses from the site www.coursera.org and stores the result in a excel format file.

# How to use

The script requires the installed Python interpreter version 3.5 To call the help, run the script with the -h or --help option.

```Bash
python coursera.py -h
usage: coursera.py [-h] filepath number_of_course

positional arguments:
  filepath          path to file for load course from www.coursera.org
  number_of_course  number of random course from www.coursera.org

optional arguments:
  -h, --help        show this help message and exit

```

To start downloading course information on the website www.coursera.org, you must specify the path to save the file and the number of imported courses through a space after specifying the name of the script.

```Bash
python coursera.py cours.xlsx 15
Courses information saved to cours.xlsx
```

The resulting list of courses will be in the file `cours.xlsx`

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
