#!/usr/bin/python

from bs4 import BeautifulSoup
from csv import writer
import requests
import sys, getopt
import re
import time
import subprocess


networksdbURL="http://networksdb.io/"


class bcolors:
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   RED = '\033[31m'
   YELLOW = '\033[93m'
   FAIL = '\033[91m'
   ENDC = '\033[0m'
   BOLD = '\033[1m'
   BGRED = '\033[41m'
   WHITE = '\033[37m'
   CYAN = '\033[36m'


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         usage()
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   logo()
   print(bcolors.BGRED + bcolors.WHITE + timelog()+ "[INFO] Hunting IPs belonging to organisations with the name:  " + inputfile + bcolors.ENDC + "\n\n")
   orgsnatcher(inputfile, outputfile)
   print(bcolors.BGRED + bcolors.WHITE + timelog()+ "[INFO] Scrape has completed. Output CSV file can be found at " + outputfile + bcolors.ENDC)


def timelog():
	current_time = time.localtime()
	ctime = time.strftime('%H:%M:%S', current_time)
	return "["+ ctime + "]"

def logo():
	subprocess.call(["clear"])
	print(bcolors.CYAN + bcolors.BOLD)
	print("""

  ____            _____                             
 / __ \          |  __ \                            
| |  | |_ __ __ _| |__) |__ _ _ __   __ _  ___ _ __ 
| |  | | '__/ _` |  _  // _` | '_ \ / _` |/ _ \ '__|
| |__| | | | (_| | | \ \ (_| | | | | (_| |  __/ |   
 \____/|_|  \__, |_|  \_\__,_|_| |_|\__, |\___|_|   
             __/ |                   __/ |          
            |___/                   |___/           
       v0.1 - x-orginating-ip 


    """)
	print(bcolors.ENDC)

def usage():
	logo()
	print("""
	USAGE:
        OrgRanger.py -i <org name> -o <file name>
    """)
	sys.exit()



def orgsnatcher(inputfile, outputfile):
   orgurl = inputfile.replace(" ","-")
   print(timelog() + bcolors.BLUE + "[INFO] Scraping search page: " + networksdbURL + "search/org/" + orgurl + bcolors.ENDC)
   i = True
   t = 2
   resultspage = requests.get(networksdbURL+"search/org/"+ orgurl)
   soup = BeautifulSoup(resultspage.content, "html.parser")
   while i is True:
      pagebody = requests.get(networksdbURL+"search/org/" + orgurl + "/page/" + str(t)) 
      if "This search returned" in pagebody:
         print(timelog() + bcolors.BLUE + "[INFO] Scraping search page: " + networksdbURL + "search/org/" + orgurl + "/page/" + str(t) + bcolors.ENDC)
         soup2 = BeautifulSoup(pagebody.content, "html.parser")
         soup = soup.append(soup2)
         t = t + 1
      else:
         i = False
   orguris = soup.find_all("a", {'class': 'link', 'href': True})
   for orguri in orguris:
      print(timelog() + bcolors.BLUE +"[INFO] Org URI visiting: " + orguri.text + bcolors.ENDC)
      orgpageuri = orguri.text.replace(" ","-")
      indivOrgIPScrapeRaw = requests.get(networksdbURL+"ip-addresses-of/"+orgpageuri)
      soup = BeautifulSoup(indivOrgIPScrapeRaw.content, "html.parser")
      indivOrgIPScrape = soup.find_all("div", class_="row netblock")
      for ipentry in indivOrgIPScrape:
         country = ipentry.find("div", class_="col-md-7 col-sm-7").find("img").attrs["title"]
         print("\n" + bcolors.YELLOW + "Country: " + country + bcolors.ENDC)
         org = ipentry.find("div", class_="col-md-7 col-sm-7").find("b").text
         print(bcolors.YELLOW + "Org: " + org + bcolors.ENDC)
         netname = ipentry.find("div", class_="col-md-7 col-sm-7").find("a").text
         print(bcolors.YELLOW + "Netname: " + netname + bcolors.ENDC)
         cidr = ipentry.find("div", class_="col-md-5 col-sm-5").find("b", text=re.compile("CIDR:")).next_sibling.strip()
         print(bcolors.YELLOW + "CIDR: " + cidr + bcolors.ENDC)
         iprange = ipentry.find("div", class_="col-md-5 col-sm-5").find("b", text=re.compile("IP Range:")).next_sibling.strip()
         print(bcolors.YELLOW + "IP Range: " + iprange + bcolors.ENDC)
         blocksize = ipentry.find("div", class_="col-md-5 col-sm-5").find("b", text=re.compile("Block size:")).next_sibling.strip()
         print(bcolors.YELLOW + "Blocksize: " + blocksize + bcolors.ENDC + "\n")
         list = [org,netname,country,cidr,iprange,blocksize]
         fileWriter(list, outputfile)

def fileWriter(list, outputfile):
   with open(outputfile, 'a', newline='') as f_object:
      writer_object = writer(f_object)
      writer_object.writerow(list)
      f_object.close()


if __name__ == "__main__":
   main(sys.argv[1:])
