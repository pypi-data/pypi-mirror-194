This is a CLI tool for fetching and downloading weather data from two public AWS S3 buckets: noaa-goes18 and noaa-nexrad-level2. The tool allows users to sign up, sign in, and view their remaining API calls.

### Installation

'pip install aerodash-v1'

## Usage

### Sign Up
- To sign up, run the command below:

'aerodash-v1 create_user'

- This command prompts the user to enter their details such as username, password, mobile, subscription type, and credit card details. The subscription type options are:

- Platinum - (100$)
- Gold - (50$)
- Free - (0$)

- Depending on the subscription type chosen, users are assigned an API call limit.

### Sign In
- To sign in and get the remaining API calls limit, run the command below:

'aerodash-v1 api_calls_limit'

- This command prompts the user to enter their username and password. On successful login, the remaining API calls are displayed.

### fetch files
- To fetch files from the noaa-goes18 or noaa-nexrad-level2 bucket, run the command below:

'aerodash-v1 fetch DATATYPE YEAR [MONTH] DAY [HOUR] [STATION]'

- DATATYPE: The type of data to fetch. It can either be geos18 or nexrad.
- YEAR: The year to fetch files for.
- DAY: The day of the year to fetch files for.
- HOUR: The hour to fetch files for. This is only required when the DATATYPE is geos18.
- MONTH: The month to fetch files for. This is only required when the DATATYPE is nexrad.
- STATION: The station code to fetch files for. This is only required when the DATATYPE is nexrad.
- The command will prompt the user to enter their username and password. On successful login, the list of files found in the bucket for the given parameters is displayed.

### download files
- To download a file from the noaa-goes18 or noaa-nexrad-level2 bucket, run the command below:

'aerodash download FILE_NAME'

- FILE_NAME: The name of the file to download.
- The command will prompt the user to enter their username and password. On successful login, the file is downloaded from the public S3 bucket to a personal S3 bucket, and the download link is displayed.

### Upgrade Subscription
- To upgrade a user's subscription plan, run the command below:

'aerodash-v1 plan_upgrade'

- The command will prompt the user to enter their username and password. On successful login, the user's remaining API calls are displayed. 
- The user is then prompted to select a new subscription plan. The subscription plan options are:

- Platinum - (100$)
- Gold - (50$)
- Free - (0$)

- Depending on the subscription type chosen, the user's API call limit is updated.

### Forgot Password
- To update a user's password, run the command below:

'aerodash-v1 forgot_password'

- The command prompts the user to enter their username and new password. If the user is found, their password is updated.

## Limitations

- The tool only supports fetching and downloading files from the noaa-goes18 and noaa-nexrad-level2 public AWS S3 buckets.
- The user's subscription plan and API call limits may restrict the amount of data that can be accessed and downloaded using the tool.
- The tool may require a certain level of technical expertise and knowledge in order to effectively use and interpret the data it provides.
- The tool may not be compatible with all operating systems or devices, and may require specific hardware or software configurations in order to function properly.