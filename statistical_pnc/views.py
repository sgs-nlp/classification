from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from .dataset2database import add2database
import logging
from django.contrib import messages

titr_string = 'نخستين مركز آموزش عالي بين‌المللي دانشگاه موناش استراليا در كيش آغاز به كار كرد'

content_string = """به گزارش خبرنگار اعزامي خبرگزاري دانشجويان ايران (ايسنا)، دكتر حميد عباچي، با اشاره به اينكه اين 
مركز اسفند ماه سال گذشته در رشته مهندسي برق و سيستم‌هاي كامپيوتر با پذيرش 30 دانشجو اولين دوره آموزشي خود را در كيش 
آغاز كرده است، افزود: دانشجويان دوره چهار ساله اين رشته را در گرايشهاي برق نرم‌افزار و سخت افزار، كنترل، ‌كامپيوتر و 
مهندسي پزشكي به صورت دو دوره دو ساله در دانشگاه كيش و موناش استراليا سپري كرده و مدرك رسمي دانشگاه مذكور را دريافت 
مي‌كنند. وي سقف پذيرش دانشجو در اين رشته را 200 نفر اعلام و پيش بيني كرد كه تعداد دانشجويان اين دانشگاه از 30 نفر 
فراتر رفته و رشته‌هاي تحصيلي اين مركز نيز به مهندسي مواد، پتروشيمي، راه و ساختمان، مكانيك، صنايع افزايش يابد. دكتر 
عباچي افزود: دانشگاه موناش استراليا با 40 سال سابقه تحصيل داراي 50 هزار دانشجو در شش زير گروه بوده و داراي 3 زير 
مجموعه در مالزي، افريقاي جنوبي و كيش است. وي شرايط تحصيلي و آموزش اين دوره را كاملا همسان، همزمان و تحت نظر دانشگاه 
موناش استراليا خواند و اظهار كرد: دانشجويان به جاي پرداخت سالانه 12 هزار دلار شهريه تحصيل در دانشگاه موناش استراليا 
مي‌توانند دو سال تحصيل خود را با پرداخت سالانه شش هزاردلار امريكا در دانشگاه كيش سپري كنند. به علاوه هم اكنون اساتيد 
اين رشته از دانشگاه صنعتي شريف تامين شده و در اين زمينه تبادل با اساتيد ساير دانشگاه‌هاي كشور صورت گرفته است. استاد 
دانشگاه موناش استراليا با اعلام آغاز مرحله دوم پذيرش دانشجوي اين رشته در پايان تير ماه جاري، گفت: دانشجويان و كساني 
كه در كنكور سراسري پذيرفته نشده اند، پس از اعلام فراخوان دانشگاه كيش بعد از كنكور سراسري به شرط داشتن مدرك تحصيلي 
رشته رياضي، معدل 15 به بالا و نمره 12 به بالا نمره 6 از 9 در آزمون ieltf كه به طور رسمي توسط شوراي فرهنگي بريتانيا در 
تهران برگزار مي‌شود در اين رشته پذيرفته مي‌شوند. همچنين حسين زمان، مدير اجراي دوره بين المللي مشترك دانشگاه كيش و 
موناش استراليا با اعلام اينكه اولين مركز آموزش عالي فعاليت بين‌المللي رسمي خود را در كشور از اسفند ماه سال گذشته آغاز 
كرده است، گفت: ‌بيشتر دانشجويان علاقمند به تحصيل در خارج از كشور پس از ديپلم بلافاصله به ساير كشورها مراجعه كرده و 
معمولا با مشكلات بسياري نظير ناتواني و عدم تسلط به زبان انگليسي مواجه مي‌شوند، بر اين اساس برقراري دوره‌هاي مشترك و 
فني جهت تقويت پايه آموزش عالي در داخل كشور بوده و راه چند ساله روشهاي آموزشي را در مدتي كوتاه سپري خواهد كرد. نماينده 
دانشگاه موناش استراليا در كيش در پايان گفت: دور اول پذيرش دانشجو در اين رشته از بين 300 متقاضي صورت گرفته و از اين 
بين 30 نفر انتخاب شدند. """

category_title = 'آموزشي'


def prerequisites(request: HttpRequest):
    from pathlib import Path
    from datetime import datetime

    # logging.info('Started storing dataset in the database.')
    # file_name = Path('staticfiles', 'HamshahriData.xlsx')
    # add2database(file_name)
    # logging.info('Data storage in the database is complete.')
    # logging.info('Started classification analys.')
    # clss = classification()
    # logging.info('Classification analys complate.')
    # from statistical_pnc.models import news2db
    # file_name = Path('staticfiles', 'HamshahriData.xlsx')
    # add2database(file_name)
    # s = news2db(titr_string=titr_string, content_string=content_string, category_title=category_title)
    return render(
        request,
        'ai_index.html',
        context={'word2vec_word_embeding__svm__accuracy_score': 1},  # clss,
    )


def index(request: HttpRequest):
    return render(request, 'index.html', context={})


def classification(request: HttpRequest):
    response = {}
    text = request.POST['text_for_classify']
    if text is None or len(text) == 0:
        response['TEXT'] = False
        response['ERROR_MESSAGE'] = 'Please enter the news you want to categorize in this section.'
        return JsonResponse(response)
    response['TEXT'] = True
    response['CATEGORY_TITLE'] = 'Educational'
    return JsonResponse(response)
