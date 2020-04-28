# -*- coding: utf-8 -*-
import scrapy
import re
from watson_developer_cloud import PersonalityInsightsV3
class CelebSpider(scrapy.Spider):
    name = 'celeb'
    #Define domain for the website to be crawl
    allowed_domains = ['www.filmfare.com']
    start_urls = ['https://www.filmfare.com/features/10-most-popular-bollywood-stars-on-social-media-34664.html']
   
    def parse(self, response):
        
        #Define url, apikey for ibm watson service
        url = "https://api.eu-gb.personality-insights.watson.cloud.ibm.com/instances/dd0964cb-397f-4757-bd8f-f140d577a6ef"
        apikey = "azkccV6fEpGGa0f3eQpamfR5D4Hjjstkar_JYiMuk8_k"
        service = PersonalityInsightsV3(url=url,iam_apikey=apikey,version="2020-4-22")
        for number in range(2,12):
            #Get selector i.e div for each celeb'sinformation
            celebrityDivId = "photo_34664_"+str(number)
            celebrityID = "div[id='"+celebrityDivId+"']"
            for celebrity in response.css(celebrityID):
                #Get the text between html tags
                cleanr = re.compile('<.*?>')
                cleantext = re.sub(cleanr, '', celebrity.get())
                profile = service.profile(cleantext,content_type="text/plain").get_result()
                personality = profile['personality'] 
                #Collect the personality trait from the given array
                personalityTrait = ""
                for trait in personality:
                    for persontrait in trait['children']:
                        personalityTrait = personalityTrait+" "+persontrait['name']
                yield{
                     "Name": celebrity.css("strong::text").extract_first(),
                     "Image_url": celebrity.css("div span img::attr('data-original')").extract_first(),
                     "Personality Trait":personalityTrait
                     }
                        
