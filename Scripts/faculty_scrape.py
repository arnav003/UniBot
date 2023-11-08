from bs4 import BeautifulSoup as BS
import lxml

with open('data.html', 'r') as file:
    content = file.read()
    soup = BS(content, 'lxml')
    faculty_list = soup.find_all('li', class_='col-sm-4')
    for faculty in faculty_list:
        name = faculty.find('a', class_='name').text
        dep = faculty.find('a', class_='institute').text
        post = faculty.find('p').text
        try:
            email = faculty.find_all('a')[2].text
            phone = faculty.find_all('a')[3].text
        except:
            email = None
            phone = None
        info_dict = {
            'Name': name,
            'Department': dep,
            'Post': post,
            'Email': email,
            'Phone': phone
        }
        print(info_dict)
        print('')
