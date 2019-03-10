from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes_model import NaiveBayesClassifier
from sqlalchemy import exists


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    news = s.query(News).get(request.query.id)
    label = request.query.label
    news.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    url = "https://news.ycombinator.com/newest"
    all_news = get_news(url)

    s = session()
    for news in all_news:
        ret = s.query(exists().where((News.title == news['title'] and News.author == news['author']))).scalar()
        if not ret:
            news = News(title=news['title'],
                        author=news['author'],
                        url=news['url'],
                        comments=news['comments'],
                        points=news['points'])
            s.add(news)
            s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    recently_marked_news = s.query(News).filter(News.title not in x_train and News.label != None).all()
    x_extra_train = [row.title for row in recently_marked_news]
    y_extra_train = [row.label for row in recently_marked_news]
    classifier.fit(x_extra_train, y_extra_train)

    blank_rows = s.query(News).filter(News.label == None).all()
    x = [row.title for row in blank_rows]
    labels = classifier.predict(x)
    good = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == 'good']
    maybe = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == 'maybe']
    never = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == 'never']

    return template('recommended', {'good': good, 'never': never, 'maybe': maybe})


if __name__ == "__main__":
    s = session()
    classifier = NaiveBayesClassifier(1)
    marked_news = s.query(News).filter(News.label != None).all()
    x_train = [row.title for row in marked_news]
    y_train = [row.label for row in marked_news]
    classifier.fit(x_train, y_train)
    run(host="localhost", port=8080)
