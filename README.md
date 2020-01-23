# result-notifier
This script uses [api-football](https://www.api-football.com) to get the data about matches. And to send you notifications it's using [IFTTT webhooks and notifications](https://ifttt.com).

To use this script you will need to do a few things first!
1. Install [requests](https://pypi.org/project/requests/):

        pip install requests
        
2. Create an [rapidapi account](https://rapidapi.com) and add [api-football](https://rapidapi.com/api-sports/api/api-football) to your apps.
Don't worry they have a plan that is charge free.
3. Create an [IFTTT account](https://ifttt.com) and install their app on your phone.
4. Create an IFTTT applet 

    Follow these steps:
      * Click on the `this` button
      * Search for the `webhooks` service and select `Receive a web request`
      * Name your event
      * Click on the `that` button
      * Search for `notifications` service and select `Send a notification from the IFTTT app`
      * Change the message to your liking! Use `{{Value1}}` and `{{Value2}}`. `Value1` will the name of the competition and `Value2` will be `team1 score team2`
    * Click on the `Finish` button 

5. Edit the `configure.py` file. :
    * Fill in your `X-RapidAPI-Key`
    * Fill in your `team identifier`
    
    These two above will be found [here](https://rapidapi.com/api-sports/api/API-FOOTBALL)
    * Fill in the event name from your IFTTT app
    * Fill in your `IFTTT Key`. You can find it in `webhooks settings`

With all these steps you should be good to go!
As this script is running 24/7 it's best to use it on for example Raspberry pi or a python hosting service
