"# twitter-coronavirus-bot"

## A bot for your daily Coronavirus statistics update

This project creates a Twitter bot that replies to users' tweets with latest Coronavirus statistics.
To try the bot that I developed, please follow @YourCoronaBot on Twitter!

## Technologies used

*Language: Python
*Packages: TweepyAPI
\*External APIs: Coronavirus monitor from RapidAPI

## How to use this project?

1. Clone this repository to your local device.
2. Register and get approved for a Twitter Developer Account at www.developer.twitter.com. \*Decide whether to use a personal account or create a separate Twitter account.
3. Create an App on your Twitter Dev Acc.
4. Get the app's Consumer key and Security key. Then, update the variables to the right keys. \*Variables are defined in the project
5. Run the project :

E.g.
`python3 reply.py`

OPTIONAL

1. Use Amazon EC2/Heroku to deploy the project in the background.

## Programs

1. posting.py : Post a standard tweet.
2. reply.py : Reply user's tweet with latest coronavirus stats of certain country when mentioned certain keywords such as "coronavirus usa".
3. progress.py : Reply user's tweet with a country's Coronavirus progress. (Percentage between yesterday and today's active cases.)

## License & Copyright

© Riza Hassan
\*This is a personal Open Source project. Feel free to clone and use the project. Contact Riza Hassan at ruhulruzbihan@gmail.com for more information.
