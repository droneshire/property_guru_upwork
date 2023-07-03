# PropertyGuru Web Alert System
[![Python application](https://github.com/droneshire/property_guru_upwork/actions/workflows/python-app.yml/badge.svg)](https://github.com/droneshire/property_guru_upwork/actions/workflows/python-app.yml)


Web Scraping and Telegram/Email Alert System

## Requirements from Customer

Looking for an alert bot that will prompt me through telegram (if not email) that a specific listing matching the parameters set on the scraper has popped up.
The prompt should include the link to that specific listing for me to do my own further assessment.

Example:

https://www.propertyguru.com.sg/listing/for-sale-the-woodleigh-residences-24395172 (see attachment too)
This listing popped up an hour ago.
If the parameters were set for 'Woodleigh Residences', I would have been alerted as soon as the scraper picked up on it.
Ideally I would like to be able to search for multiple terms at one time, instead of just 'Woodleigh Residences' only for example

If the parameters can be even more specific such as including a price range that would be fantastic.
So in the event I had it set for '$900,000 to $1,200,000', the bot would not bother to alert me as this listing is above that range, even though 'Woodleigh Residences' matches

For more specific parameter examples:

https://www.propertyguru.com.sg/property-for-sale

Please follow the link above and click on 'Filter'.

Under 'Buy' you will see all the different parameters available on the website

If possible please also include a way to mute/pause the alert bot, in such event that my partner and I are not actively searching for any specific listings


