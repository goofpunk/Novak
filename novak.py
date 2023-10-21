from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime as dt
import os, html, shutil

template_env = Environment(loader=FileSystemLoader(searchpath='src/layouts/'))

articles_dir = 'src/articles'
articles = os.listdir(articles_dir)
stories_dict = {}
essays_dict = {}
feed_dict = {}

# used for generating an RSS feed
homepageURL = ""

outputFolder = 'dist'

shutil.copytree('src/styles', 'dist/styles', dirs_exist_ok = True)
shutil.copytree('src/assets', 'dist/assets', dirs_exist_ok = True)


# ignore dotfiles
def article_filter(file):
    if file[0] == ".":
        return False
    else:
        return True
    
articles = list(filter(article_filter, articles))

for article in articles:
    filename = os.path.splitext(article)[0]
    
    markdownFile = open(articles_dir + '/' + article)
    formattedFile = markdown(markdownFile.read(), extras=['strike', 'tables', 'metadata'])

    template = template_env.get_template(formattedFile.metadata['layout'] + '.html')

    articleTitle = formattedFile.metadata['title']
    articlePubDate = dt.strptime(formattedFile.metadata['date'], '%Y%m%d').strftime('%B %-d, %Y')
    if formattedFile.metadata['author'] == '':
        articleAuthor = 'ARTICLE AUTHOR'
    else:
        articleAuthor = formattedFile.metadata['author']

    if 'style' not in formattedFile.metadata:
        articleStyle = 'default.css'
    else:
        articleStyle = formattedFile.metadata['style'] + '.css'
    
    outputFileLocation = filename.replace(" ", "-") + '.html'
    outputFile = open(outputFolder + '/' + outputFileLocation, 'w')
    outputFile.write(template.render(title = articleTitle, author = articleAuthor, pubDate=articlePubDate, body = formattedFile, style = 'styles/' + articleStyle))
    outputFile.close()

    
    if 'category' not in formattedFile.metadata:
        print('ERROR: ' + article + ': All files must contain \'category\' metadata')
        exit()
    elif formattedFile.metadata['category'] == 'fiction':
        stories_dict[formattedFile.metadata['date']] = {
            'title': formattedFile.metadata['title'],
            'relativeLocation':outputFileLocation,
            'permalink': homepageURL + outputFileLocation,
            'atomDate': dt.strptime(formattedFile.metadata['date'], '%Y%m%d').isoformat() + 'Z',
            'content': html.escape(formattedFile)}
    elif formattedFile.metadata['category'] == 'essay':
        essays_dict[formattedFile.metadata['date']] = {
            'title': formattedFile.metadata['title'],
            'relativeLocation':outputFileLocation,
            'permalink': homepageURL + outputFileLocation,
            'atomDate': dt.strptime(formattedFile.metadata['date'], '%Y%m%d').isoformat() + 'Z',
            'content': html.escape(formattedFile)}
    else:
        print('ERROR: ' + article + ': unrecognized category \'' + formattedFile.metadata['category'] + '\'.')

stories_dict = dict(sorted(stories_dict.items(), reverse=True))
essays_dict = dict(sorted(essays_dict.items(), reverse=True))

feed_dict = stories_dict | essays_dict
feed_dict = dict(sorted(feed_dict.items(), reverse=True))

template = template_env.get_template('index.html')
indexFile = open(outputFolder + '/index.html', 'w')
indexFile.write(template.render(essays_dict = essays_dict, stories_dict = stories_dict, style= 'styles/default.css'))
indexFile.close()

template = template_env.get_template('feed.xml')
feedFile = open(outputFolder + '/feed.xml', 'w')
feedFile.write(template.render(essays_dict = feed_dict, lastUpdated = dt.now().isoformat() + 'Z'))
feedFile.close()
