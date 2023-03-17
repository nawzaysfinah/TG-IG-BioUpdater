# Telegram to Instagram Bio Auto-Updater

> Based of Instagram Bio Auto-Updater by [Langston Howley](https://github.com/langstonhowley)

Using the [Selenium Web Driver](https://selenium-python.readthedocs.io/) and [Requests](https://requests.readthedocs.io/en/master/) modules this program updates a user's Instagram bio to whatever is sent to a telegram bot.

```
Writing some code
When: 2020-10-27 @ 13:35:35
```

## Installation and Running

If you'd like, first set up a [virtual enviroment](https://realpython.com/python-virtual-environments-a-primer/#using-virtual-environments) for storing the dependencies locally rather than on your machine.

```bash
# clone the repository into your current directory
git clone https://github.com/langstonhowley/Instagram-Bio-Auto-Updater.git

# go into the project directory
cd Instagram-Bio-Auto-Updater

# install all of the required packages
pip3 install -r requirements.txt

# create a .env folder and insert your credentials
touch .env
echo "INSTAGRAM_USERNAME = {YOUR_INSTA_USERNAME}" >> .env
echo "INSTAGRAM_PASSWORD = {YOUR_INSTA_PASSWORD}" >> .env

# run the updater 😁
python3 main.py
```
