from bs4 import BeautifulSoup
import requests
import ucto
from pynlpl.formats import folia




# Reading URL's from the txt file.
def read_urls(filename):
	with open(filename) as f:
		lines = f.read().splitlines()
	return lines

# Simple page request to an URL, returns the content of the request.
def get_request(url):
	r = requests.get(url)
	return r.content

# It's returning the urls of the news in a day
def find_new_urls(url):
	content = get_request(url)
	soup = BeautifulSoup(content, 'html5lib')
	links = []
	for link in soup.select('table.cnt tbody tr td div table tbody tr td span a[href]'):
		links.append(link['href'])
	return links

# Making the actual call for a new and returning a cleaned string.
def get_and_clean_data(url):
	content = get_request(url)
	soup = BeautifulSoup(content, 'html5lib')
	data = soup.select('div.Normal')
	if len(data)>0:
		splitted = BeautifulSoup(str(data[0]), 'lxml').text.split('\n')
		clean_data = clear_string(splitted)
		return clean_data
	return None

def clear_string(array):
	data = ''
	for i in array:
		if i != '':
			if i[0].isdigit() != True:
				data = data + ' ' + i
	return data


def get_tokenized_data(data):
	settingsfile = "./tokconfig-eng"
	tokenizer = ucto.Tokenizer(settingsfile)
	tokenizer.process(data)
	tokenized_array = []
	for sentence in tokenizer.sentences():
		tokenized_array.append(sentence)
	return tokenized_array

def folia_creator(id, data, docname):
	doc = folia.Document(id=id)
	for i in range(0, len(data)):
		text = doc.add(folia.Text)
		text.add(folia.Word, data[str(i)]['value'])
		text.add(folia.Sentence, data[str(i)]['text'])
	doc.save('./files/'+docname)
	return True

def get_datas():
	url = read_urls('news.urls.txt')[0]
	news = find_new_urls(url)[0:3]
	counter = 0
	json_data = {}
	for i in news:
		cleaned_data = get_and_clean_data(i)
		if cleaned_data != None:
			json_data[counter] = get_tokenized_data(cleaned_data)
			counter = counter + 1
	return json_data

#folia_creator('username', {0:{'text': 'haha', 'value': "1"}}, 'user_selections.xml')
#get_tokenized_data(" It's that time again, where we're all excited about the new beginnings, new hopes and the whole new year, new you charm. Like every year, you need to make a few promises to yourself and stick around to your resolutions. And we know that most of us hardly stick to the resolutions. So this time we have come with a list of attainable goal that we can focus on. Excited for the New Year 2018? Read through! We know that imagining life without the internet is tough. But, don't we all waste our time way too much on social media. From dinner dates to family outings, we must learn to prioritise things. Being realistic, let's spend time on social media when we're free and not every time.  Do you know that 2017 was one year that focused a lot on health and fitness? From clean eating to a fitness regime, there are a lot of things you can introduce in your life now. Better now, then never! When was the last time you met your grandmother or your uncle? Give your family the gift of time and trust us there is no better gift than time for them! Don't we all fall into the trap of office politics every now and then? Whenever you get in that zone, always think of your actions. Always think if your words or actions are worth ruining someone's mood. Be it your wife or your mother, learn to thank the people around you. A little thank you won't hurt anyone. So, the next time your mother packs a wholesome meal, just appreciate her work and let her know how you feel!  Be it season sales or the easy EMIs, we hardly think of saving money. But this year, you must change that. If you're really bad at saving, start small with saving a particular amount every month.  With the busy work schedule, we hardly get to spend the time of new things. When was the last time you did something new? Can't think, right? This year make sure you try new things and have a whole lot of stories to share the entire year!  This year challenge yourself and break your shell. Talk to more people from your office to your gym class. We know that nothing beats meeting your old friends, but that doesn't mean you should not make new friends at all. ")
#find_new_urls(get_request("https://timesofindia.indiatimes.com/2018/1/1/archivelist/year-2018,month-1,starttime-43101.cms"))
#read_urls('news.urls.txt')
#print(get_and_clean_data('https://timesofindia.indiatimes.com/life-style/events/new-year-resolutions-2018-lets-aim-for-these-serious-new-year-resolutions/articleshow/62296606.cms?'))
