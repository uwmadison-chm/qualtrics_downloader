# qualtrics_downloader
A little script to download CSV data from Qualtrics

Requires Python 3 and the `requests` library.

## Usage

```
usage: download_survey.py [-h] [-o OUT_DIR] [-v]
                          qualtrics_domain api_token survey_id

 Download a survey from Qualtrics, as CSV.

Getting your IDs are documented here:
https://api.qualtrics.com/docs/finding-your-qualtrics-ids

And your Qualtrics domain will be every domain before qualtrics.com; something
like:

yourorg
or
yourorg.co1

positional arguments:
  qualtrics_domain      Qualtrics domain (everything before qualtrics.com)
  api_token             API token for your user
  survey_id             ID for the survey to download

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DIR, --out-dir OUT_DIR
                        Directory to save downloaded CSV to
  -v, --verbose         print debugging output
  ```

## Credits

Written by Nate Vack at the Center for Healthy Minds at the University of Wisconsin-Madison. Adapted from [Qualtrics demo API code](https://api.qualtrics.com/docs/getting-survey-responses-new).