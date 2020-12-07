# Messenger Chatbot

**Chatbot** bases on Messenger conversations downloaded from Facebook. While you miss your friend, you can easily make a bot that talks like them.

The project is compatibile with Python 3.4+ and Tensorflow 2.



MEDIUM ARTICLE: https://medium.com/@zuzannadeutschman/replicate-your-friend-with-transformer-bc5efe3a1596

## Features

* Fast and reliable - similarly to google translator, it uses transformer model, implemented in tensorflow

* Each language compatibile - corpus is built based on sent messages. So, you input conversation may be in any language you want! For me, polish language works fantastic.

* Easy to run

## Demo

![](C:\Users\zuzan\Pictures\chatbot.gif)

## TODO

* Firstly, please download messenger conversation with any friend you want. [Here ]([https://www.zapptales.com/en/download-facebook-messenger-chat-history-how-to/](https://www.zapptales.com/en/download-facebook-messenger-chat-history-how-to/) you can find description how to do it. As a result you should have one or multiple files called `message_{n}.html` in certain folder.

* Clone this repository

* To build and run Chatbot, you need the following libraries preinstalled.
  
  * beautifulsoup4
  
  * colorama
  
  * lxml
  
  * pandas
  
  * re
  
  * requests
  
  * tensorflow
  
  * tensorflow_datasets
  
  * tqdm

* To run your Chatbot, only those 3 lines have to be written in Command Prompt (in repository path).
  
  * `python conversations_to_csv.py path_to_html_files` You will be asked to enter input and target persons fullname. The first person is probably you and the target person is the one you want to make chatbot based on. Please note, that names you enter should be exactly the same as provided on Facebook.
  
  * `python train.py` This script is responsible for building and training transformer model, so it will take some time  to complete. If you would like to change some parameters, for example batch size or number of epochs, you can easily do it  within the script.
  
  * `python talk.py` You will be asked to enter your and chatbot name or nick.  Then you can start your conversation. Enjoy! For closing, press `CTRL + C`
  
  * 

* I hope you like chatbot you built. If you are interested in details of how it works, please go to  the `transformer_chatbot.ipynb` notebook and to my **Medium artcile**.
  
    
