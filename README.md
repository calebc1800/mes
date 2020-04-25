# Master Enumeration Script (MES)

Master Enumeration Script (MES) is a python3 script which compiles various enumeration techniques in a single script and compiles reports on each host. MES currently employs the following techniques:
- Host discovery
- Nmap scanning
- Website scraping

## Installation
MES currently is installed through direct download through github. The HEAD can be downloaded by copying the repository locally or the latest stable release can be downloaded [here](https://github.com/calebc1800/mes/releases/latest).
The required repositories and packages can be viewed in [requirements.txt](https://github.com/calebc1800/mes/requirements.txt)

## Usage
MES uses cli arguments to function. MES requires that -d and -t are used. All available arguments are as follows:
```
arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Destination directory for enumeration report
  -t TARGET, --target TARGET
                        Target IP (192.168.0.1) or subnet (192.168.0.0/24)
  -s SCAN_TYPE, --scan-type SCAN_TYPE
                        nmap scan type (1-3). 1 being the fastest and briefest while 3 is more detailed and longer. Default: 2
```

MES is run through the following command:
```bash
sudo python3 ./mes/master_script.py -d /[report_location]/ -t [subnet]
```
Each of the scripts in the /mes/resources/ directory can also be run individually.

Currently has only been tested on Debian 5.5.13-2.
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)