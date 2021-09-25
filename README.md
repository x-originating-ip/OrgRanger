# OrgRanger
## BETA v0.1
A quick Python3 script to scrape the IPv4/IPv6 address database on networksdb.io for a given company name, and output a CSV containing the data.

## Notice:
This is a very hastily written/quick win script. If anyone else happens to have utility for this outside of me, then let me know and I can spend some time cleaning it up.

## To Run:

```sh


  ____            _____                             
 / __ \          |  __ \                            
| |  | |_ __ __ _| |__) |__ _ _ __   __ _  ___ _ __ 
| |  | | '__/ _` |  _  // _` | '_ \ / _` |/ _ \ '__|
| |__| | | | (_| | | \ \ (_| | | | | (_| |  __/ |   
 \____/|_|  \__, |_|  \_\__,_|_| |_|\__, |\___|_|   
             __/ |                   __/ |          
            |___/                   |___/           

	USAGE:
        python3 OrgRanger.py -i <ORG NAME> -o <FILENAME.CSV>
```
### Note: If org name is comprised of more than one word, be sure to include the org name within double quotes (eg. -i "Miggins Pie Shop"). If your org name is an acronym, run both the acronym and the expanded version over two searches and diff the results. 
