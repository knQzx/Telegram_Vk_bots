# pip install pytelegrambotapi
# pip install requests
# pip install requests bs4

from telebot import types
import requests  # Модуль для обработки URL
from bs4 import BeautifulSoup  # Модуль для работы с HTML
import telebot

bot = telebot.TeleBot('1567662670:AAGw14kNEGBN8w6paN1njQ2TRusNxqh33so')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

# доллар
DOLLAR = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
# евро
EVRO = 'https://www.google.com/search?q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&sxsrf=ALeKk031mNuFnTE5vVraAqmAEIO_5ObjXw%3A1610550949504&ei=pQ7_X9ztHe6OwPAP8M6dwAk&oq=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjIGCAAQBxAeMgYIABAHEB4yCAgAEAgQBxAeMggIABAIEAcQHjIICAAQCBAHEB4yCAgAEAgQBxAeMggIABAIEAcQHjIICAAQCBAHEB4yCAgAEAgQBxAeOgQIABBHOgQIABANOggIABANEAUQHjoHCAAQFBCHAjoCCABQ6jxYkEdggEhoAXACeACAAVOIAekBkgEBM5gBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwic1PLpmZnuAhVuBxAIHXBnB5gQ4dUDCA0&uact=5'
# фунты стерлингов
GBP = 'https://www.google.com/search?q=gbp+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&sxsrf=ALeKk029rHLX2J0OMlPeGOvoU4RcWglt3g%3A1610550959754&ei=rw7_X83ALauMrwSPtrOABg&oq=GBP+&gs_lcp=CgZwc3ktYWIQARgAMgQIABBDMgQIABBDMggIABCxAxCDATIICAAQsQMQgwEyBQgAELEDMgcIABAUEIcCMgoIABCxAxCDARBDMgUIABCxAzIECAAQQzICCAA6BwgjEOoCECdQ4sdGWOLHRmC30EZoAXABeACAAVmIAVmSAQExmAEAoAEBoAECqgEHZ3dzLXdperABCsABAQ&sclient=psy-ab'
# швейцарские франки
CHF = 'https://www.google.com/search?q=chf+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&sxsrf=ALeKk01ojS_lAUzo5ivSodABmj4kxkVg-Q%3A1610552118302&ei=NhP_X4X-EaWxrgTj443gCA&oq=CHF+&gs_lcp=CgZwc3ktYWIQARgBMgcIABAUEIcCMgQIABBDMgUIABCxAzIECAAQQzICCAAyAggAMgIIADICCAAyAggAMgIIADoHCCMQ6gIQJ1CNnRBYjZ0QYK2mEGgBcAF4AIABbogBbpIBAzAuMZgBAKABAaABAqoBB2d3cy13aXqwAQrAAQE&sclient=psy-ab'
# японские иены
JPY = 'https://www.google.com/search?q=JPY++%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&sxsrf=ALeKk03fPJOAsv_bVNomodIWRQZsz7LqEA%3A1610552386709&ei=QhT_X8rdKrCwrgSE16_QAg&oq=JPY++%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&gs_lcp=CgZwc3ktYWIQAzICCAAyBggAEAcQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeOgQIABBDUM7VDFjs2Qxg4uYMaABwAXgAgAFbiAHqAZIBATOYAQCgAQGgAQKqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwjKhpuXn5nuAhUwmIsKHYTrCyoQ4dUDCA0&uact=5'
# австралийские доллары
AUD = 'https://www.google.com/search?q=AUD+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&sxsrf=ALeKk023xmot_hiR6UJD2BsyU0H7QxFA0w%3A1610552916110&ei=VBb_X4uFBqeSwPAP3PW1yAY&oq=AUD+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&gs_lcp=CgZwc3ktYWIQAzICCAAyBggAEAUQHjIGCAAQBRAeMgYIABAFEB46BAgAEEdQwAhYwAhgxg1oAHACeACAAUyIAUySAQExmAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwiL_9KToZnuAhUnCRAIHdx6DWkQ4dUDCA0&uact=5'
# юань
CNY = 'https://www.google.com/search?q=%D1%8E%D0%B0%D0%BD%D1%8C+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&sxsrf=ALeKk01TWMkYgCfsLkyisqTRYjKMLyqSyA%3A1610559527915&ei=JzD_X_uhN-XhrgTft7r4Cg&oq=%D1%8E%D0%B0%D0%BD%D1%8C+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&gs_lcp=CgZwc3ktYWIQAzICCAAyBAgAEEMyBggAEAcQHjICCAAyBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBAgAEB4yBggAEAUQHjIGCAAQBRAeOgQIABBHOggIABAHEAUQHlCyqAJYnbICYOWzAmgAcAN4AIABTYgB4AKSAQE1mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwi70bPkuZnuAhXlsIsKHd-bDq8Q4dUDCA0&uact=5'
# белорусский рубль
BYN = 'https://www.google.com/search?q=%D0%B1%D0%B5%D0%BB%D0%BE%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9+%D1%80%D1%83%D0%B1%D0%BB%D1%8C+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&sxsrf=ALeKk01u9qwnv8o-fBUbBAngA03y5GtWmg%3A1610559568995&ei=UDD_X-qcPOrLrgS2qoagAQ&oq=%D0%B1%D0%B5%D0%BB%D0%BE%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9+%D1%80%D1%83%D0%B1%D0%BB%D1%8C+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjIGCAAQBxAeMgYIABAHEB4yBAgAEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB46BAgAEEc6BAgAEA06CAgAEAcQBRAeOgcIABCxAxANOgIIADoJCAAQDRBGEIICUMquA1i3zgNg1dADaABwA3gAgAFciAGTC5IBAjE4mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjqhP_3uZnuAhXqpYsKHTaVARQQ4dUDCA0&uact=5'
# гривна
UAH = 'https://www.google.com/search?q=%D0%93%D0%A0%D0%98%D0%92%D0%9D%D0%90+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&sxsrf=ALeKk001eLMlZ4vZmlBPgoyjj_-pQXC9UA%3A1610559629265&ei=jTD_X5ivD4ewrgTy0YLYDg&oq=%D0%93%D0%A0%D0%98%D0%92%D0%9D%D0%90+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&gs_lcp=CgZwc3ktYWIQAzICCAAyAggAMgIIADIGCAAQBxAeMgIIADIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB46BAgAEEc6BAgAEENQlZ8CWNaoAmDfrAJoAHADeACAAcMBiAGfBJIBAzUuMZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwjYqd2UupnuAhUHmIsKHfKoAOsQ4dUDCA0&uact=5'
# польский злотый
PLN = 'https://www.google.com/search?sxsrf=ALeKk00-9IM218TC7TeLCum7f-xiSB0PrQ:1610559703691&q=%D0%B7%D0%BB%D0%BE%D1%82%D1%8B%D0%B9+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D0%B8&spell=1&sa=X&ved=2ahUKEwiooJy4upnuAhUqi8MKHVweBlsQBSgAegQIBBA1&biw=1366&bih=625'
# азербайджанский манат
MANAT = 'https://www.google.com/search?q=%D0%BC%D0%B0%D0%BD%D0%B0%D1%82+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BC%D0%B0%D0%BD%D0%B0%D0%BA+%D0%BA+&aqs=chrome.1.69i57j0i10i433j0i10j0i10i395l7.5783j1j7&sourceid=chrome&ie=UTF-8'
# Албанский лек
LEK = 'https://www.google.com/search?q=%D0%BB%D0%B5%D0%BA%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk02hmYL2710ktH9_o9taNCLvZaSoUA%3A1610641102431&ei=zm4AYPHTGeiIrwSTlILoDg&oq=%D0%BB%D0%B5%D0%BA%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIECAAQDTIICAAQCBAHEB4yCAgAEAcQBRAeMggIABAHEAUQHjIICAAQBxAFEB46BAgAEEc6BggAEAcQHlC-wwRYk8cEYMDIBGgAcAN4AIABWYgB7gGSAQEzmAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjx8pTW6ZvuAhVoxIsKHROKAO0Q4dUDCA0&uact=5'
# Алжирский динар
ALSHDINAR = 'https://www.google.com/search?q=%D0%B0%D0%BB%D0%B6%D0%B8%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk03rPjYuqDq7nrpF_Yb4rHY6YLm8VQ%3A1610641233415&ei=UW8AYLTwGKWQrgSKg5DgBA&oq=%D0%B0%D0%BB%D0%B6%D0%B4%D0%B8%D0%BD%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQARgAMgYIABAHEB4yCAgAEAgQBxAeMggIABAHEAUQHjIICAAQBxAFEB4yCAgAEAcQBRAeOgQIABBHOgcIIxCwAhAnOggIABAHEAoQHjoECAAQDToGCAAQDRAeOggIABANEAUQHlDfMVioNmDaRGgAcAJ4AIABf4gBnQKSAQMyLjGYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab'
# Аргентинское песо
ARGENTPESO = 'https://www.google.com/search?q=%D0%B0%D1%80%D0%B3%D0%B5%D0%BD%D1%82%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%BF%D0%B5%D1%81%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk02r8sa5SJcT0YltYE2dse0y6xcWUg%3A1610641243037&ei=W28AYMXnAfD6qwHZvLvQDA&oq=%D0%B0%D1%80%D0%B3%D0%B5%D0%BD%D1%82%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%BF%D0%B5%D1%81%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjIGCAAQBxAeMgQIABAeMgYIABAFEB4yBggAEAgQHjoICAAQBxAKEB46CAgAEAgQBxAeOggIABAHEAUQHjoECAAQDVCnlAJYna8CYKm3AmgAcAF4AIABdYgB_AqSAQQxNC4zmAEAoAEBqgEHZ3dzLXdpesABAQ&sclient=psy-ab&ved=0ahUKEwiFgZuZ6pvuAhVw_SoKHVneDsoQ4dUDCA0&uact=5'
# Армянский драм
ARMDRAM = 'https://www.google.com/search?q=%D0%B0%D1%80%D0%BC%D1%8F%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D1%80%D0%B0%D0%BC+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk01sCCMqWsYWsvis3TQ5PMrZJvhLWg%3A1610641283764&ei=g28AYLqGLtKgjgbm54DQAQ&oq=%D0%B0%D1%80%D0%BC%D1%8F%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D1%80%D0%B0%D0%BC+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAAyAggAMgIIADIGCAAQBxAeMgQIABAeMgQIABAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB46CAgAEAcQChAeOggIABAHEAUQHjoICAAQCBAHEB5QyfsBWPyLAmCTjgJoAHABeACAAVqIAb4IkgECMTSYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwj609Cs6pvuAhVSkMMKHeYzABoQ4dUDCA0&uact=5'
# Болгарский лев
BLGLEV = 'https://www.google.com/search?q=%D0%B1%D0%BE%D0%BB%D0%B3%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%BB%D0%B5%D0%B2+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk0000oeADSqQUvdTlYg6-ivetMGEdQ%3A1610641319218&ei=p28AYJveDO2yrgSagpTYDA&oq=%D0%B1%D0%BE%D0%BB%D0%B3%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D0%BB%D0%B5%D0%B2+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAAyAggAMgQIABAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB4yBggAEAgQHjIGCAAQCBAeOgYIABAHEB46CAgAEAcQChAeOgQIABANOggIABAHEAUQHjoICAAQCBAHEB5QvvcBWJyNAmC3kQJoAHABeACAAXOIAfIIkgEEMTMuMZgBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwjbzcS96pvuAhVtmYsKHRoBBcsQ4dUDCA0&uact=5'
# Боливийский боливиано
BOLIVBOLIV = 'https://www.google.com/search?q=%D0%B1%D0%BE%D0%BB%D0%B8%D0%B2%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9+%D0%B1%D0%BE%D0%BB%D0%B8%D0%B2%D0%B8%D0%B0%D0%BD%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk00D41pHOZABeOedVTrLNxEm0yPDXg%3A1610641355142&ei=y28AYM-eCOmqrgTIs574Dg&oq=%D0%B1%D0%BE%D0%BB%D0%B8%D0%B2%D0%B8%D0%B9+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQARgBMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgQIABBHOggIABAHEAUQHjoECAAQDToICAAQDRAFEB5QhcICWKLKAmCv2gJoAHACeACAAXGIAf8CkgEDMi4ymAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab'
# Бразильский реал
BRAZREAL = 'https://www.google.com/search?q=%D0%B1%D1%80%D0%B0%D0%B7%D0%B8%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9+%D1%80%D0%B5%D0%B0%D0%BB+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk001G-mAEcqPwJW58MZKITsuV-MzSw%3A1610641400470&ei=-G8AYNmWHOrMrgTTyJCICA&oq=%D0%B1%D1%80%D0%B0%D0%B7%D0%B8%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9+%D1%80%D0%B5%D0%B0%D0%BB+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAAyBggAEAcQHjIECAAQHjIECAAQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIICAAQBxAFEB4yBggAEAUQHjIGCAAQBRAeOggIABAIEAcQHjoECAAQDVCp4gJY2vkCYIT9AmgAcAB4AIABcogBtwmSAQQxNS4xmAEAoAEBqgEHZ3dzLXdpesABAQ&sclient=psy-ab&ved=0ahUKEwjZ8qPk6pvuAhVqposKHVMkBIEQ4dUDCA0&uact=5'
# Венгерский форинт
VENGFORINT = 'https://www.google.com/search?q=atyuthcrbq+ajhbyn+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk03sHzi-pLzTgOCUdSMe1MHj7fzoYw%3A1610641450231&ei=KnAAYMXNDan3qwH07ZuoCA&oq=atyuthcrbq+ajhbyn+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIECAAQDTIGCAAQDRAeMgYIABANEB4yCAgAEA0QBRAeMggIABAIEA0QHjoGCAAQBxAeOgUIABDNAlDg7QFYh4sCYLOOAmgAcAF4AIABlAGIAYMNkgEEMTIuNZgBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwjFioH86pvuAhWp-yoKHfT2BoUQ4dUDCA0&uact=5'
# Вьетнамский донг
VEATNDONG = 'https://www.google.com/search?q=%D0%B2%D1%8C%D0%B5%D1%82%D0%BD%D0%B0%D0%BC%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%BE%D0%BD%D0%B3+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk00EgpXmxiQ6TuiE2rOQ9TVTla-ZQA%3A1610641485672&ei=TXAAYJXKKJa43AO7uKxA&oq=%D0%B2%D1%8C%D0%B5%D1%82%D0%BD%D0%B0%D0%BC%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%BE%D0%BD%D0%B3+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAAyAggAMgYIABAHEB4yBAgAEB4yBAgAEB4yBAgAEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjoICAAQDRAFEB46CAgAEAcQBRAeOggIABAIEAcQHlCKlAVY36sFYKOvBWgAcAB4AIABfogBigqSAQQxNS4xmAEAoAEBqgEHZ3dzLXdpesABAQ&sclient=psy-ab&ved=0ahUKEwjVpPSM65vuAhUWHHcKHTscCwgQ4dUDCA0&uact=5'
# Гватемальский кетсаль
GVATKETS = 'https://www.google.com/search?q=%D0%B3%D0%B2%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9+%D0%BA%D0%B5%D1%82%D1%81%D0%B0%D0%BB%D1%8C+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk00MZ9k7Xt849Nx_kSpCN0Es53VXHQ%3A1610641575113&ei=p3AAYKOUBsT4qwGg84KICw&oq=%D0%B3%D0%B2%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9+%D0%BA%D0%B5%D1%82%D1%81%D0%B0%D0%BB%D1%8C+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAA6BggAEAcQHjoICAAQBxAFEB46CggAEAcQBRAKEB5QkNkCWPT5AmCs_AJoAHABeACAAWSIAf4MkgEEMjAuMZgBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwjjg8e365vuAhVE_CoKHaC5ALEQ4dUDCA0&uact=5'
# Гонконгский доллар
GONGDLR = 'https://www.google.com/search?q=%D0%B3%D0%BE%D0%BD%D0%BA%D0%BE%D0%BD%D0%B3%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk006QbnLplsOLIQ_viTrfnOKQbDFPw%3A1610641624579&ei=2HAAYPbcIsWr3AOSpqPQCA&oq=%D0%B3%D0%BE%D0%BD+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQARgBMgQIABANMgYIABAHEB4yBAgAEA0yBAgAEA0yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB46CAgAEAcQChAeULeEAli-iAJgx6ACaABwAXgAgAFIiAHLAZIBATOYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab'
# Грузинский лари
GRUZLARI = 'https://www.google.com/search?q=%D0%B3%D1%80%D1%83%D0%B7%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%BB%D0%B0%D1%80%D1%80%D0%B8+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk01V2xUh0zt0w1Tc4mcXdsy8W_bD4Q%3A1610641662376&ei=_nAAYISRFomnrgSll7nwDg&oq=%D0%B3%D1%80%D1%83%D0%B7%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%BB%D0%B0%D1%80%D1%80%D0%B8+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIECAAQDTIGCAAQDRAeMgYIABANEB4yBggAEA0QHjIGCAAQDRAeMggIABANEAUQHjIICAAQDRAFEB4yCAgAEA0QBRAeMggIABANEAUQHjIICAAQDRAFEB46BggAEAcQHjoCCAA6CAgAEAcQChAeOggIABAHEAUQHjoICAAQCBAHEB5Qqr0BWMvQAWCM1AFoAHABeACAAWuIAYQJkgEEMTUuMZgBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwiEiJXh65vuAhWJk4sKHaVLDu4Q4dUDCA0&uact=5'
# Датская крона
DATSKRONA = 'https://www.google.com/search?q=%D0%B4%D0%B0%D1%82%D1%81%D0%BA%D0%B0%D1%8F+%D0%BA%D1%80%D0%BE%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk02I4r7jt6Y8QHGqTcDwXx5_pkLsjA%3A1610641690601&ei=GnEAYKqIJNLnrgTKka2YDA&oq=%D0%B4%D0%B0%D1%82%D1%81%D0%BA%D0%B0%D1%8F+%D0%BA%D1%80%D0%BE%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAAyBggAEAcQHjIECAAQHjIECAAQHjIECAAQHjIECAAQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeOgYIABAIEB46CAgAEAcQChAeOgQIABANOggIABAIEAcQHjoICAAQBxAFEB5Q9JACWLmvAmC0sgJoAHAAeACAAbIBiAH0CZIBBDEzLjKYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwiq_c_u65vuAhXSs4sKHcpIC8MQ4dUDCA0&uact=5'
# Дирхам ОАЭ
DIRXAMOAE = 'https://www.google.com/search?q=%D0%B4%D0%B8%D1%80%D1%85%D0%B0%D0%BC+%D0%BE%D0%B0%D1%8D+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk03s5qQEOau-hcCjlFKo5eLHJRFtsg%3A1610641730793&ei=QnEAYKDmL8vrrgTQrLWgAg&oq=%D0%B4%D0%B8%D1%80%D1%85%D0%B0%D0%BC+%D0%BE%D0%B0%D1%8D+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjIGCAAQBxAeOggIABAHEAoQHjoECAAQDToCCAA6BQgAELEDOgQIABAeOggIABAIEAcQHlC9tAFYptMBYJvVAWgBcAF4AIAB5wGIAeUIkgEFOS4xLjGYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwigj-WB7JvuAhXLtYsKHVBWDSQQ4dUDCA0&uact=5'
# Доминиканское песо
DOMINPESO = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BC%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%BF%D0%B5%D1%81%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk02tHQc9ObyC7hnj3rk-r1s6IjeNhg%3A1610641758935&ei=XnEAYILEOMPcrgT-j6KgBw&oq=%D0%B4%D0%BE%D0%BC%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%BF%D0%B5%D1%81%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAAyBggAEAUQHjIGCAAQBRAeOgYIABAHEB46CAgAEAgQBxAeOggIABAHEAUQHjoICAAQDRAFEB46BAgAEA1QnsUDWNnfA2Cb4gNoAHABeACAAccBiAHAC5IBBDE2LjKYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwiC65qP7JvuAhVDrosKHf6HCHQQ4dUDCA0&uact=5'
# Египетский фунт
EGIPETFUNT = 'https://www.google.com/search?q=%D0%B5%D0%B3%D0%B8%D0%BF%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B9+%D1%84%D1%83%D0%BD%D1%82+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk00mpZHWTc1kab1JP1pFtFdtckdHbg%3A1610641821503&ei=nXEAYJWUHsfrrgTHnJngDg&oq=%D0%B5%D0%B3%D0%B8%D0%BF%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B9+%D1%84%D1%83%D0%BD%D1%82+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjIGCAAQBxAeMgYIABAHEB4yAggAMgIIADIECAAQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeOggIABAHEAoQHjoECAAQDToGCAAQDRAeOggIABAHEAUQHjoICAAQDRAFEB46CAgAEAgQDRAeOggIABAIEAcQHlDMkQJY-KcCYJ2rAmgAcAF4AIABYIgB5wiSAQIxNZgBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwjV1oWt7JvuAhXHtYsKHUdOBuwQ4dUDCA0&uact=5'
# Индийская рупия
INDIRUPIA = 'https://www.google.com/search?q=%D0%B8%D0%BD%D0%B4%D0%B8%D0%B9%D1%81%D0%BA%D0%B0%D1%8F+%D1%80%D1%83%D0%BF%D0%B8%D1%8F+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk02Twil-YMZczRMLgXODEqJPlbbpmQ%3A1610641860730&ei=xHEAYIfwK4SorgShh5uABg&oq=%D0%B8%D0%BD%D0%B4%D0%B8%D0%B9%D1%81%D0%BA%D0%B0%D1%8F+%D1%80%D1%83%D0%BF%D0%B8%D1%8F+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAAyBggAEAcQHjICCAAyBAgAEB4yBAgAEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeOggIABAIEAcQHjoICAAQBxAFEB46BggAEAgQHjoECAAQDVCozgFYoOUBYI3nAWgAcAF4AIABb4gB_wiSAQQxNC4xmAEAoAEBqgEHZ3dzLXdpesABAQ&sclient=psy-ab&ved=0ahUKEwiH4t-_7JvuAhUElIsKHaHDBmAQ4dUDCA0&uact=5'
# Иорданский динар
IORDDINAR = 'https://www.google.com/search?q=%D0%B8%D0%BE%D1%80%D0%B4%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk01bFan91sAPNAGwClH64cDUfSUzFw%3A1610641891202&ei=43EAYK7CC7OWjgb-6rzQAg&oq=%D0%B8%D0%BE%D1%80%D0%B4%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAAyBggAEAcQHjIECAAQHjIECAAQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB46CAgAEAcQBRAeOgoIABAHEAUQChAeOgQIABANUL6NAljfqQJguq0CaABwAXgAgAFwiAHVCZIBBDEzLjOYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwjuv6PO7JvuAhUzi8MKHX41DyoQ4dUDCA0&uact=5'
# Иранский риал
IRANRIAL = 'https://www.google.com/search?q=%D0%B8%D1%80%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D1%80%D0%B5%D0%B0%D0%BB+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk00EvX8Qc1AH5rRYnvGaA04s_s8sCg%3A1610641930546&ei=CnIAYJTcII-vrgSRq4SYAg&oq=%D0%B8%D1%80%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D1%80%D0%B5%D0%B0%D0%BB+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIJCAAQChBGEIICOgYIABAHEB46BAgAEA06BggAEA0QHjoICAAQBxAFEB46CAgAEA0QBRAeOggIABAIEA0QHjoKCAAQCBANEAoQHjoICAAQBxAKEB5Qw5MDWKClA2DUpwNoAHABeACAAVSIAdUHkgECMTOYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwiUiYXh7JvuAhWPl4sKHZEVASMQ4dUDCA0&uact=5'
# Исландская крона
ISLANDKRONA = 'https://www.google.com/search?q=%D0%B8%D1%81%D0%BB%D0%B0%D0%BD%D0%B4%D1%81%D0%BA%D0%B0%D1%8F+%D0%BA%D1%80%D0%BE%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=ALeKk03PbDmCzAA3woW2R2wxPZpUePCRKw%3A1610641985580&ei=QXIAYK7zIoqOrwTzx4OgBg&oq=%D0%B8%D1%81%D0%BB%D0%B0%D0%BD%D0%B4%D1%81%D0%BA%D0%B0%D1%8F+%D0%BA%D1%80%D0%BE%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzICCAAyBggAEAcQHjIECAAQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeMgYIABAIEB46CAgAEAgQBxAeOggIABAHEAUQHjoECAAQDVDn6wFY0ocCYOSbAmgAcAB4AIABbIgBxAmSAQQxNS4xmAEAoAEBqgEHZ3dzLXdpesABAQ&sclient=psy-ab&ved=0ahUKEwjul6T77JvuAhUKx4sKHfPjAGQQ4dUDCA0&uact=5'




# доллар
full_page = requests.get(DOLLAR, headers=headers)
soup = BeautifulSoup(full_page.content, 'html.parser')
convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
dlr12 = '1 USD(доллар) равен ' + convert[0].text + ' руб'
dlr_te = float(convert[0].text.replace(',', '.'))

# евро
full_page1 = requests.get(EVRO, headers=headers)
soup1 = BeautifulSoup(full_page1.content, 'html.parser')
convert1 = soup1.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
eur12 = '1 EUR(евро) равно ' + convert1[0].text + ' руб'
eur_te = float(convert1[0].text.replace(',', '.'))

# фунты стерлингов
full_page2 = requests.get(GBP, headers=headers)
soup2 = BeautifulSoup(full_page2.content, 'html.parser')
convert1 = soup2.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
gbp12 = '1 GBP(Фунт стерлингов) равен ' + convert1[0].text + ' руб'
gbp_te = float(convert1[0].text.replace(',', '.'))

# швейцарские франки
full_page3 = requests.get(CHF, headers=headers)
soup3 = BeautifulSoup(full_page3.content, 'html.parser')
convert2 = soup3.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
chf12 = '1 CHF(Швейцарский франк) равен ' + convert2[0].text + ' руб'
chf_te = float(convert2[0].text.replace(',', '.'))

# японские иены
full_page4 = requests.get(JPY, headers=headers)
soup4 = BeautifulSoup(full_page4.content, 'html.parser')
convert3 = soup4.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
jpy12 = '1 JPY(Японская иена) равна ' + convert3[0].text + ' руб'
jpy_te = float(convert3[0].text.replace(',', '.'))

# австралийские доллары
full_page5 = requests.get(AUD, headers=headers)
soup5 = BeautifulSoup(full_page5.content, 'html.parser')
convert4 = soup5.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
aud12 = '1 AUD(Австралийский доллар) равен ' + convert4[0].text + ' руб'
aud_te = float(convert4[0].text.replace(',', '.'))

# юань
full_page6 = requests.get(CNY, headers=headers)
soup6 = BeautifulSoup(full_page6.content, 'html.parser')
convert5 = soup6.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
cny12 = '1 CNY(юань) равен ' + convert5[0].text + ' руб'
cny_te = float(convert5[0].text.replace(',', '.'))

# белорусские рубли
full_page7 = requests.get(BYN, headers=headers)
soup7 = BeautifulSoup(full_page7.content, 'html.parser')
convert6 = soup7.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
byn12 = '1 BYN(белорусский рубль) равен ' + convert6[0].text + ' руб'
byn_te = float(convert6[0].text.replace(',', '.'))

# гривна
full_page8 = requests.get(UAH, headers=headers)
soup8 = BeautifulSoup(full_page8.content, 'html.parser')
convert7 = soup8.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
uah12 = '1 UAH(гривна) равна ' + convert7[0].text + ' руб'
uah_te = float(convert7[0].text.replace(',', '.'))

# польский злотый PLN
full_page9 = requests.get(PLN, headers=headers)
soup9 = BeautifulSoup(full_page9.content, 'html.parser')
convert8 = soup9.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
pln12 = '1 PLN(польский злотый) равен ' + convert8[0].text + ' руб'
pln_te = float(convert8[0].text.replace(',', '.'))

# азербайджанский манат
full_page10 = requests.get(MANAT, headers=headers)
soup10 = BeautifulSoup(full_page10.content, 'html.parser')
convert9 = soup10.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
manat12 = '1 MANAT(азербайджанский манат) равен ' + convert9[0].text + ' руб'
manat_te = float(convert9[0].text.replace(',', '.'))

# Албанский лек
full_page11 = requests.get(LEK, headers=headers)
soup11 = BeautifulSoup(full_page11.content, 'html.parser')
convert10 = soup11.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
lek12 = '1 LEK(Албанский лек) равен ' + convert10[0].text + ' руб'
lek_te = float(convert10[0].text.replace(',', '.'))

# Алжирский динар
full_page12 = requests.get(ALSHDINAR, headers=headers)
soup12 = BeautifulSoup(full_page12.content, 'html.parser')
convert11 = soup12.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
alshidinar12 = '1 ALSHIDINAR(Алжирский динар) равен ' + convert11[0].text + ' руб'
alshidinar_te = float(convert11[0].text.replace(',', '.'))

# Аргентинское песо
full_page13 = requests.get(ARGENTPESO, headers=headers)
soup13 = BeautifulSoup(full_page13.content, 'html.parser')
convert12 = soup13.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
argentpeso12 = '1 ARGENTPESO(Аргентинское песо) равно ' + convert12[0].text + ' руб'
argentpeso_te = float(convert12[0].text.replace(',', '.'))

# Армянский драм
full_page14 = requests.get(ARMDRAM, headers=headers)
soup14 = BeautifulSoup(full_page14.content, 'html.parser')
convert13 = soup14.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
armdram12 = '1 ARMDRAM(Армянский драм) равен ' + convert13[0].text + ' руб'
armdram_te = float(convert13[0].text.replace(',', '.'))

# Болгарский лев
full_page15 = requests.get(BLGLEV, headers=headers)
soup15 = BeautifulSoup(full_page15.content, 'html.parser')
convert14 = soup15.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
blglev12 = '1 BLGLEV(Болгарский лев) равен ' + convert14[0].text + ' руб'
blglev_te = float(convert14[0].text.replace(',', '.'))

# Боливийский боливиано
full_page16 = requests.get(BOLIVBOLIV, headers=headers)
soup16 = BeautifulSoup(full_page16.content, 'html.parser')
convert15 = soup16.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
bolivboliv12 = '1 BOLIVBOLIV(Боливийский боливиано) равен ' + convert15[0].text + ' руб'
bolivboliv_te = float(convert15[0].text.replace(',', '.'))

# Бразильский реал
full_page17 = requests.get(BRAZREAL, headers=headers)
soup17 = BeautifulSoup(full_page17.content, 'html.parser')
convert16 = soup17.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
brazreal12 = '1 BRAZREAL(Бразильский реал) равен ' + convert16[0].text + ' руб'
brazreal_te = float(convert16[0].text.replace(',', '.'))

# Венгерский форинт
full_page18 = requests.get(VENGFORINT, headers=headers)
soup18 = BeautifulSoup(full_page18.content, 'html.parser')
convert17 = soup18.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
vengforint12 = '1 VENGFORINT(Венгерский форинт) равен ' + convert17[0].text + ' руб'
vengforint_te = float(convert17[0].text.replace(',', '.'))


# Гватемальский кетсаль
full_page20 = requests.get(GVATKETS, headers=headers)
soup20 = BeautifulSoup(full_page20.content, 'html.parser')
convert19 = soup20.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
gvatkets12 = '1 GVATKETS(АГватемальский кетсальм) равна ' + convert19[0].text + ' руб'
gvatkets_te = float(convert19[0].text.replace(',', '.'))

# Гонконгский доллар
full_page21 = requests.get(GONGDLR, headers=headers)
soup21 = BeautifulSoup(full_page21.content, 'html.parser')
convert20 = soup21.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
gongdlr12 = '1 GONGDLR(Гонконгский доллар) равен ' + convert20[0].text + ' руб'
gongdlr_te = float(convert20[0].text.replace(',', '.'))

# Грузинский лари
full_page22 = requests.get(GRUZLARI, headers=headers)
soup22 = BeautifulSoup(full_page22.content, 'html.parser')
convert21 = soup22.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
gruzlari12 = '1 GRUZLARI(Грузинский лари) равен ' + convert21[0].text + ' руб'
gruzlari_te = float(convert21[0].text.replace(',', '.'))

# Датская крона
full_page23 = requests.get(DATSKRONA, headers=headers)
soup23 = BeautifulSoup(full_page23.content, 'html.parser')
convert22 = soup23.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
datskrona12 = '1 DATSKRONA(Датская крона) равна ' + convert22[0].text + ' руб'
datskrona_te = float(convert22[0].text.replace(',', '.'))

# Дирхам ОАЭ
full_page24 = requests.get(DIRXAMOAE, headers=headers)
soup24 = BeautifulSoup(full_page24.content, 'html.parser')
convert23 = soup24.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
dirxamoae12 = '1 DIRXAMOAE(Дирхам ОАЭ) равен ' + convert23[0].text + ' руб'
dirxamoae_te = float(convert23[0].text.replace(',', '.'))

# Доминиканское песо
full_page25 = requests.get(DOMINPESO, headers=headers)
soup25 = BeautifulSoup(full_page25.content, 'html.parser')
convert24 = soup25.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
dominpeso12 = '1 DOMINPESO(Доминиканское песо) равно ' + convert24[0].text + ' руб'
dominpeso_te = float(convert24[0].text.replace(',', '.'))

# Египетский фунт
full_page26 = requests.get(EGIPETFUNT, headers=headers)
soup26 = BeautifulSoup(full_page26.content, 'html.parser')
convert25 = soup26.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
egipetfunt12 = '1 EGIPETFUNT(Египетский фунт) равен ' + convert25[0].text + ' руб'
egipetfunt_te = float(convert25[0].text.replace(',', '.'))

# Индийская рупия
full_page27 = requests.get(INDIRUPIA, headers=headers)
soup27 = BeautifulSoup(full_page27.content, 'html.parser')
convert26 = soup27.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
indirupia12 = '1 INDIRUPIA(Индийская рупия) равна ' + convert26[0].text + ' руб'
indirupia_te = float(convert26[0].text.replace(',', '.'))

# Иорданский динар
full_page28 = requests.get(IORDDINAR, headers=headers)
soup28 = BeautifulSoup(full_page28.content, 'html.parser')
convert27 = soup28.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
iorddinar12 = '1 IORDDINAR(Иорданский динар) равен ' + convert27[0].text + ' руб'
iorddinar_te = float(convert27[0].text.replace(',', '.'))

# Исландская крона
full_page30 = requests.get(ISLANDKRONA, headers=headers)
soup30 = BeautifulSoup(full_page30.content, 'html.parser')
convert29 = soup30.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
islandkrona12 = '1 ISLANDKRONA(Исландская крона) равна ' + convert29[0].text + ' руб'
islandkrona_te = float(convert29[0].text.replace(',', '.'))




chislo_nach = 0
age = 0


@bot.message_handler(commands=['count'])
def start_handler1(message):
    bot.send_message(message.from_user.id, "Сколько у тебя рублей")
    bot.register_next_step_handler(message, get_age)
    print(message)


# бот реагирует на сообщения
@bot.message_handler(commands=['kyrs'])
def start_handler(message):
    keyboard = types.InlineKeyboardMarkup()
    key_dollar = types.InlineKeyboardButton(text='Доллар', callback_data='dlr')
    keyboard.add(key_dollar)
    key_euro = types.InlineKeyboardButton(text='Евро', callback_data='eur')
    keyboard.add(key_euro)
    key_gbp = types.InlineKeyboardButton(text='Фунт стерлинг', callback_data='gbp')
    keyboard.add(key_gbp)
    key_chf = types.InlineKeyboardButton(text='Швейцарский франк', callback_data='chf')
    keyboard.add(key_chf)
    key_jpy = types.InlineKeyboardButton(text='Японская иена', callback_data='jpy')
    keyboard.add(key_jpy)
    key_aud = types.InlineKeyboardButton(text='Австралийский доллар', callback_data='aud')
    keyboard.add(key_aud)
    key_cny = types.InlineKeyboardButton(text='Юань', callback_data='cny')
    keyboard.add(key_cny)
    key_byn = types.InlineKeyboardButton(text='Белорусские рубли', callback_data='byn')
    keyboard.add(key_byn)
    key_uah = types.InlineKeyboardButton(text='Гривна', callback_data='uah')
    keyboard.add(key_uah)
    key_pln = types.InlineKeyboardButton(text='Польский злотый', callback_data='pln')
    keyboard.add(key_pln)
    key_manat = types.InlineKeyboardButton(text='Азербайджанский минат', callback_data='manat')
    keyboard.add(key_manat)
    key_lek = types.InlineKeyboardButton(text='Албанский лек', callback_data='lekalb')
    keyboard.add(key_lek)
    key_alshdinar = types.InlineKeyboardButton(text='Алжирский динар', callback_data='aldshidinar')
    keyboard.add(key_alshdinar)
    key_argentpeso = types.InlineKeyboardButton(text='Аргентинское песо', callback_data='argentpeso')
    keyboard.add(key_argentpeso)
    key_armdram = types.InlineKeyboardButton(text='Армянский драм', callback_data='armdram')
    keyboard.add(key_armdram)
    key_bglev = types.InlineKeyboardButton(text='Болгарский лев', callback_data='bglev')
    keyboard.add(key_bglev)
    key_bolivboliv = types.InlineKeyboardButton(text='Боливийский боливиано', callback_data='bolivboliv')
    keyboard.add(key_bolivboliv)
    key_brazreal = types.InlineKeyboardButton(text='Бразильский реал', callback_data='brazreal')
    keyboard.add(key_brazreal)
    key_vengforint = types.InlineKeyboardButton(text='Венгерский форинт', callback_data='vengforint')
    keyboard.add(key_vengforint)
    key_gvatemalkets = types.InlineKeyboardButton(text='Гватемальский кетсаль', callback_data='gvatemalkets')
    keyboard.add(key_gvatemalkets)
    key_gongdola = types.InlineKeyboardButton(text='Гонконгский доллар', callback_data='gongdola')
    keyboard.add(key_gongdola)
    key_gruzlari = types.InlineKeyboardButton(text='Грузинский лари', callback_data='gruzlari')
    keyboard.add(key_gruzlari)
    key_datskrona = types.InlineKeyboardButton(text='Датская крона', callback_data='datskrona')
    keyboard.add(key_datskrona)
    key_dirxamoae = types.InlineKeyboardButton(text='Дирхам ОАЭ', callback_data='dirxamoae')
    keyboard.add(key_dirxamoae)
    key_dominpeso = types.InlineKeyboardButton(text='Доминиканское песо', callback_data='dominpeso')
    keyboard.add(key_dominpeso)
    key_egipetfunt = types.InlineKeyboardButton(text='Египетский фунт', callback_data='egipetfunt')
    keyboard.add(key_egipetfunt)
    key_indirupia = types.InlineKeyboardButton(text='Индийская рупия', callback_data='indirupia')
    keyboard.add(key_indirupia)
    key_iorddinar = types.InlineKeyboardButton(text='Иорданский динар', callback_data='iorddinar')
    keyboard.add(key_iorddinar)
    key_islandkrona = types.InlineKeyboardButton(text='Исландская крона', callback_data='islandkrona')
    keyboard.add(key_islandkrona)

    bot.send_message(message.from_user.id, text='Выбери какая тебе нужна валюта', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши /kyrs или /count")
        print("Напиши /kyrs или /count")
    elif message.text == "Посчитать" or message.text == "посчитать":
        bot.send_message(message.from_user.id, "Сколько у тебя рублей")
        bot.register_next_step_handler(message, get_age)
        print("Сколько у тебя рублей")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        print('Я тебя не понимаю. Напиши /help.')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # доллары
    if call.data == "dlr":
        bot.send_message(call.message.chat.id, dlr12)
        print(dlr12)
    # евро
    elif call.data == "eur":
        bot.send_message(call.message.chat.id, eur12)
        print(eur12)
    # фунты стерлинги
    elif call.data == "gbp":
        bot.send_message(call.message.chat.id, gbp12)
        print(gbp12)
    # швейцарские франки
    elif call.data == "chf":
        bot.send_message(call.message.chat.id, chf12)
        print(chf12)
    # японские иены
    elif call.data == "jpy":
        bot.send_message(call.message.chat.id, jpy12)
        print(jpy12)
    # австралийский доллар
    elif call.data == "aud":
        bot.send_message(call.message.chat.id, aud12)
        print(aud12)
    # юань
    elif call.data == "cny":
        bot.send_message(call.message.chat.id, cny12)
        print(cny12)
    # белорусские рубли
    elif call.data == "byn":
        bot.send_message(call.message.chat.id, byn12)
        print(byn12)
    # гривна
    elif call.data == "uah":
        bot.send_message(call.message.chat.id, uah12)
        print(uah12)
    # польский злотый
    elif call.data == "pln":
        bot.send_message(call.message.chat.id, pln12)
        print(pln12)
    # Азербайджанский минат
    elif call.data == "manat":
        bot.send_message(call.message.chat.id, manat12)
        print(manat12)
    # Албанский лек
    elif call.data == "lekalb":
        bot.send_message(call.message.chat.id, lek12)
        print(lek12)
    # Алжирский динар
    elif call.data == "aldshidinar":
        bot.send_message(call.message.chat.id, alshidinar12)
        print(alshidinar12)
    # Аргентинское песо
    elif call.data == "argentpeso":
        bot.send_message(call.message.chat.id, argentpeso12)
        print(argentpeso12)
    # Армянский драм
    elif call.data == "armdram":
        bot.send_message(call.message.chat.id, armdram12)
        print(armdram12)
    # Болгарский лев
    elif call.data == "bglev":
        bot.send_message(call.message.chat.id, blglev12)
        print(blglev12)
    # Боливийский боливиано
    elif call.data == "bolivboliv":
        bot.send_message(call.message.chat.id, bolivboliv12)
        print(bolivboliv12)
    # Бразильский реал
    elif call.data == "brazreal":
        bot.send_message(call.message.chat.id, brazreal12)
        print(brazreal12)
    # Венгерский форинт
    elif call.data == "vengforint":
        bot.send_message(call.message.chat.id, vengforint12)
        print(vengforint12)
    # Гватемальский кетсаль
    elif call.data == "gvatemalkets":
        bot.send_message(call.message.chat.id, gvatkets12)
        print(gvatkets12)
    # Гонконгский доллар
    elif call.data == "gongdola":
        bot.send_message(call.message.chat.id, gongdlr12)
        print(gongdlr12)
    # Грузинский лари
    elif call.data == "gruzlari":
        bot.send_message(call.message.chat.id, gruzlari12)
        print(gruzlari12)
    # Датская крона
    elif call.data == "datskrona":
        bot.send_message(call.message.chat.id, datskrona12)
        print(datskrona12)
    # Дирхам ОАЭ
    elif call.data == "dirxamoae":
        bot.send_message(call.message.chat.id, dirxamoae12)
        print(dirxamoae12)
    # Доминиканское песо
    elif call.data == "dominpeso":
        bot.send_message(call.message.chat.id, dominpeso12)
        print(dominpeso12)
    # Египетский фунт
    elif call.data == "egipetfunt":
        bot.send_message(call.message.chat.id, egipetfunt12)
        print(egipetfunt12)
    # Индийская рупия
    elif call.data == "indirupia":
        bot.send_message(call.message.chat.id, indirupia12)
        print(indirupia12)
    # Иорданский динар
    elif call.data == "iorddinar":
        bot.send_message(call.message.chat.id, iorddinar12)
        print(iorddinar12)
    # Исландская крона
    elif call.data == "islandkrona":
        bot.send_message(call.message.chat.id, islandkrona12)
        print(islandkrona12)



def get_age(message):
    global age
    while age == 0:
        try:
            age = int(message.text)
            print(age)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        ageall = age + 0
        bot.send_message(message.from_user.id, 'В какую валюту хотим перевести?')
        bot.send_message(message.from_user.id, 'P.S. Доступны те что и во вложениях /kyrs ')
        bot.register_next_step_handler(message, get_name)
        print(message)


def get_name(message):
    global name
    name = message.text
    if name == "Доллары":
        bot.send_message(message.from_user.id, f'В долларах это {age / dlr_te}')
        print(f'В долларах это {age / dlr_te}')
    elif name == "Евро":
        bot.send_message(message.from_user.id, f'В евро это {age / eur_te}')
        print(f'В евро это {age / eur_te}')
    elif name == "Фунты стерлинги":
        bot.send_message(message.from_user.id, f'В фунтах стерлингах это {age / gbp_te}')
        print(f'В фунтах стерлингах это {age / gbp_te}')
    elif name == "Швейцарские франки":
        bot.send_message(message.from_user.id, f'В швейцарских франках это {age / chf_te}')
        print(f'В швейцарских франках это {age / chf_te}')
    elif name == "Японские иены":
        bot.send_message(message.from_user.id, f'В японских иенах это {age / jpy_te}')
        print(f'В японских иенах это {age / jpy_te}')
    elif name == "Австралийский доллар":
        bot.send_message(message.from_user.id, f'В австралийских долларах это {age / aud_te}')
        print(f'В австралийских долларах это {age / aud_te}')
    elif name == "Юани":
        bot.send_message(message.from_user.id, f'В юанях это {age / cny_te}')
        print(f'В юанях это {age / cny_te}')
    elif name == "Белорусские рубли":
        bot.send_message(message.from_user.id, f'В белорусских рублях это {age / byn_te}')
        print(f'В белорусских рублях это {age / byn_te}')
    elif name == "Гривны":
        bot.send_message(message.from_user.id, f'В гривнах это {age / uah_te}')
        print(f'В гривнах это {age / uah_te}')
    elif name == "Польский злотый":
        bot.send_message(message.from_user.id, f'В польских злотых это {age / pln_te}')
        print(f'В польских злотых это {age / pln_te}')


bot.polling(none_stop=True, interval=0)
