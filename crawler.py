import MySQLdb
from BeautifulSoup import BeautifulSoup
import urllib2
import re

domain = "http://vimeo.com"
home_page = urllib2.urlopen(domain)
soup = BeautifulSoup( home_page )

video_url = "http://vimeo.com/%s" % soup.find({'ol':'featured_videos'}).find('a').get('href')
video_page = urllib2.urlopen(video_url)
soup = BeautifulSoup( video_page )
user_list = [ soup.find('a',{'rel':'author'}).get('href') ]




def get_user_info( user , user_list , count) :
	"""
	takes the user_url and total_count , return dict of user information and
	followers list if count is less that 5000 .
	"""

	user_url = "http://vimeo.com%s" % user
	html_page = urllib2.urlopen(user_url)
	soup = BeautifulSoup(html_page)

	profile_div = soup.find('div', {'id':'profile'})

	#user information
	data = {}
	data['url'] = user_url
	data['name'] = profile_div.find('span', {'itemprop':'name'}).text
	data['paying'] = bool( profile_div.find('span', {'class':'badge_plus'}) )
	data['staff_pick'] = bool( soup.find('ul' , {'id':'featured_videos'}) )
	data['video'] =  bool( soup.find('ul',{'id':'recent_videos'}) )

	following = soup.find('ul' ,{'class':'profile_following'})
        left_user_count = 5000 - count
	if following and  left_user_count :
		profile_following  = following.findAll('a')
		for each_user in profile_following:
			user = each_user.get('href')
			if (user not in user_list) and left_user_count :
				user_list.append(user)
				count += 1
                                left_user_count -= 1

	return data , user_list , count



count = 1
i = 1
db = MySQLdb.connect(host="localhost",user="root",passwd="rosh",db="vimeo")
cursor = db.cursor()

for each_user in user_list :
        try :
	    user , user_list , count  = get_user_info( each_user, user_list , count )
            query = "INSERT INTO search_vimeouser (name,url,paying,staff_pick,video)  VALUES ('%s','%s',%i,%i,%i)" % \
                    ( user['name'], user['url'] ,user['paying'] ,user['staff_pick'],user['video'] )

	    cursor.execute(query)
            db.commit()
            print "data inserted for user %s  ,  count : %s" % (user['name'], i)
	    i += 1
        except :
            count -= 1

db.close()
print "Executed"
