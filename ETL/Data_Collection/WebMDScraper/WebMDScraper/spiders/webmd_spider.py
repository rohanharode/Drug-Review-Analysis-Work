# -*- coding: utf-8 -*-
from WebMDScraper.items import WebmdscraperItem
from scrapy import Spider, Request
from scrapy.selector import Selector
import urllib
import re
import html

headers = {'User-Agent': 'Chrome/60.0.3112.113',
           'enc_data': 'OXYIMo2UzzqFUzYszFv4lWP6aDP0r+h4AOC2fYVQIl8=',
           'timestamp': 'Mon, 04 Sept 2017 04:35:00 GMT',
           'client_id': '3454df96-c7a5-47bb-a74e-890fb3c30a0d'}


class WebmdSpider(Spider):
    name = 'webmd_spider'
    allowed_domains = ['http://www.webmd.com/']
    start_urls = ['https://www.webmd.com/drugs/2/index']
    drug_dict = {}

    def parse(self, response):
        print("Processing:" + response.url)
        drugs_a_to_z = response.xpath('//ul[@class="browse-letters squares"]')[0].xpath("li/a/@href").extract()
        for i in range(2):
            yield Request(response.urljoin(drugs_a_to_z[i]),
                          callback=self.parse_sub,
                          dont_filter=True)


    def parse_sub(self, response):
        print("Processing sub drug category:" + response.url)
        sub = response.xpath('//ul[@class="browse-subletters squares"]')[0].xpath("li/a/@href").extract()
        for i in range(2):
            yield Request(response.urljoin(sub[i]),
                          callback=self.parse_drug,
                          dont_filter=True)


    def parse_drug(self, response):
        drug_list = response.xpath('//ul[@class="drug-list"]')[0].xpath("li/a")
        for i in range(2):
            yield Request(response.urljoin(drug_list[i].xpath("@href")[0].extract()),
                          callback=self.parse_details,
                          meta={'Drug': drug_list[i].xpath("text()")[0].extract().lower()},
                          dont_filter=True)


    def parse_details(self, response):

        Use = ' '.join(response.xpath('//div[@id="tab-1"]').xpath("div/div/p").xpath("text()")[0].extract())
        Sides_fulltext = ' '.join(response.xpath('//div[@id="tab-2"]').xpath('div/div/p/descendant-or-self::*/text()').extract())
        Sides = ' '.join(re.split(r'(?<=[.:;])\s', Sides_fulltext)[:2])


        if Sides.startswith('See also'):
            Sides = ' '.join(re.split(r'(?<=[.:;])\s', Sides_fulltext)[1:2])

        if Sides.split('.')[1] and Sides.split('.')[1] != "":
            if 'If either of these' in Sides.split('.')[1]:
                Sides = ' '.join(re.split(r'(?<=[.:;])\s', Sides_fulltext)[0:1])
            
        if Sides.startswith(('Consult your','Remember that your')):
            Sides = ''

        a = re.split(r'(?<=\w[\.])\s', Sides)
        if a != []:
            Sides = a[0]

        review_url = ' '.join(
            response.xpath('//div[@class="drug-review-lowest"]').xpath("a").xpath("@href")[0].extract())

        if review_url:
            if not Use:
                Use = ' '

            if not Sides:
                Sides = ' '

            yield Request(response.urljoin(review_url.replace(" ", '')),
                          callback=self.parse_reviews,
                          meta={'Drug': response.meta['Drug'],
                                'Use': Use,
                                'Sides': Sides,
                                'Review_URL': review_url,
                                }, dont_filter=True)

    def parse_reviews(self, response):
        NumReviews = 0
        if re.search('Rate this treatment and share your opinion', response.body.decode('utf-8')) \
                or re.search('Be the first to share your experience with this treatment',
                             response.body.decode('utf-8')):
            WebmdSpider.drug_dict[response.meta['Drug']] = {'Use': response.meta['Use'],
                                                            'Sides': response.meta['Sides'],
                                                            'Reviews': [{}]}

        else:
            NumReviews = int(
                response.xpath('//span[@class="totalreviews"]/text()')[0].extract().replace(" Total User Reviews", ""))
            url = 'http://www.webmd.com/drugs/service/UserRatingService.asmx/GetUserReviewSummary?repositoryId=1&primaryId='
            DrugId = re.search('(drugid=)(\d+)', response.url).group(2)
            url2 = '&secondaryId=-1&secondaryIdValue='
            id2 = urllib.parse.quote(
                re.sub("\s+", " ", response.xpath('//option[@value = -1]//text()').extract()[0]).strip())

        if NumReviews != 0:
            yield Request(url + DrugId + url2 + id2,
                          callback=self.parse_ratings,
                          meta={'Drug': response.meta['Drug'],
                                'Use': response.meta['Use'],
                                'Sides': response.meta['Sides'],
                                'DrugId': DrugId,
                                'NumReviews': NumReviews},
                          dont_filter=True)

    def parse_ratings(self, response):
        if re.search('("xsd:string">)(\d+.\d+)', response.xpath('//*/*').extract()[3]):
            Effectiveness = re.search('("xsd:string">)(\d+.\d+)', response.xpath('//*/*').extract()[3]).group(2)
        else:
            Effectiveness = re.search('("xsd:string">)(\d+)', response.xpath('//*/*').extract()[3]).group(2)

        if re.search('("xsd:string">)(\d+.\d+)', response.xpath('//*/*').extract()[4]):
            EaseofUse = re.search('("xsd:string">)(\d+.\d+)', response.xpath('//*/*').extract()[4]).group(2)
        else:
            EaseofUse = re.search('("xsd:string">)(\d+)', response.xpath('//*/*').extract()[4]).group(2)

        if re.search('("xsd:string">)(\d+.\d+)', response.xpath('//*/*').extract()[5]):
            Satisfaction = re.search('("xsd:string">)(\d+.\d+)', response.xpath('//*/*').extract()[5]).group(2)
        else:
            Satisfaction = re.search('("xsd:string">)(\d+)', response.xpath('//*/*').extract()[5]).group(2)

        url = "http://www.webmd.com/drugs/service/UserRatingService.asmx/GetUserReviewsPagedXml?repositoryId=1&objectId="
        url2 = "&pageIndex=0&pageSize="
        url3 = "&sortBy=DatePosted"

        yield Request(url + response.meta['DrugId'] + url2 + str(response.meta['NumReviews']) + url3,
                      method='GET', headers=headers,
                      callback=self.parse_all_reviews,
                      meta={'Drug': response.meta['Drug'],
                            'Use': response.meta['Use'],
                            'Sides': response.meta['Sides'],
                            'DrugId': response.meta['DrugId'],
                            'NumReviews': response.meta['NumReviews'],
                            'Overall Effectiveness': Effectiveness,
                            'Overall EaseofUse': EaseofUse,
                            'Overall Satisfaction': Satisfaction},
                      dont_filter=True)

    def parse_all_reviews(self, response):
        n = response.meta['NumReviews']
        data = Selector(
            text=html.unescape(response.xpath("//*")[0].extract()).replace("<![CDATA[", "").replace("]]>", ""))
        Reviews = [{} for i in range(int(n))]
        for i in range(int(n)):
            # t_Id = data.xpath("//userreviewid")[i].xpath("text()")
            # Reviews[i]['Id'] = ' ' if len(t_Id) is 0 else t_Id[0].extract()
            t_Condition = data.xpath("//secondaryvalue")[i].xpath("text()")
            if len(t_Condition) == 0:
                Reviews[i]['Condition'] = ' '
            else:
                Reviews[i]['Condition'] = t_Condition[0].extract()
            # t_IsPatient = data.xpath("//boolean2")[i].xpath("text()")
            # Reviews[i]['IsPatient'] = ' ' if len(t_IsPatient) is 0 else t_IsPatient[0].extract()
            t_IsMale = data.xpath("//boolean1")[i].xpath("text()")
            if len(t_IsMale) == 0:
                Reviews[i]['IsMale'] = ' '
            else:
                if t_IsMale[0].extract() == 'True':
                    Reviews[i]['IsMale'] = 'Male'
                else:
                    Reviews[i]['IsMale'] = 'Female'


            t_Age = data.xpath("//lookuptext1")[i].xpath("text()")
            if len(t_Age) == 0:
                Reviews[i]['Age'] = ' '
            else:
                Reviews[i]['Age'] = t_Age[0].extract()

            # t_TimeUsingDrug = data.xpath("//lookuptext2")[i].xpath("text()")
            # Reviews[i]['TimeUsingDrug'] = ' ' if len(t_TimeUsingDrug) is 0 else t_TimeUsingDrug[0].extract()
            t_DatePosted = data.xpath("//dateposted")[i].xpath("text()")
            if len(t_DatePosted) == 0:
                Reviews[i]['DatePosted'] = ' '
            else:
                Reviews[i]['DatePosted'] = t_DatePosted[0].extract().split(" ")[0]

            t_Comment = data.xpath("//userexperience")[i].xpath("text()")
            if len(t_Comment) == 0:
                Reviews[i]['Comment'] = ' '
            else:
                Reviews[i]['Comment'] = t_Comment[0].extract()

            t_Effectiveness = data.xpath("//ratingcriteria1")[i].xpath("text()")
            if len(t_Effectiveness) == 0:
                Reviews[i]['Effectiveness'] = ' '
            else:
                Reviews[i]['Effectiveness'] = t_Effectiveness[0].extract()

            t_EaseOfUse = data.xpath("//ratingcriteria2")[i].xpath("text()")
            if len(t_EaseOfUse) == 0:
                Reviews[i]['EaseOfUse'] = ' '
            else:
                Reviews[i]['EaseOfUse'] = t_EaseOfUse[0].extract()

            t_Satisfaction = data.xpath("//ratingcriteria3")[i].xpath("text()")
            if len(t_Satisfaction) == 0:
                Reviews[i]['Satisfaction'] = ' '
            else:
                Reviews[i]['Satisfaction'] = t_Satisfaction[0].extract()

            t_NumFoundHelpful = data.xpath("//foundhelpfulcount")[i].xpath("text()")
            if len(t_NumFoundHelpful) == 0:
                Reviews[i]['NumFoundHelpful'] = 0
            else:
                Reviews[i]['NumFoundHelpful'] = t_NumFoundHelpful[0].extract()
            # t_NumVoted = data.xpath("//totalvotedcount")[i].xpath("text()")
            # Reviews[i]['NumVoted'] = ' ' if len(t_NumVoted) is 0 else t_NumVoted[0].extract()
            info = WebmdSpider.drug_dict = {'DrugId': response.meta['DrugId'],
                                            'Sides': response.meta['Sides'],
                                            'Effectiveness': Reviews[i]['Effectiveness'],
                                            'EaseofUse': Reviews[i]['EaseOfUse'],
                                            'Sex': Reviews[i]['IsMale'],
                                            'Age': Reviews[i]['Age'],
                                            'Satisfaction': Reviews[i]['Satisfaction'],
                                            'Reviews': Reviews[i]['Comment'],
                                            'Condition': Reviews[i]['Condition'],
                                            'UsefulCount':Reviews[i]['NumFoundHelpful'],
                                            'Date':Reviews[i]['DatePosted'],
                                            }
            item = WebmdscraperItem()
            item['Drug'] = response.meta['Drug']
            for key in info.keys():
                item[key] = info[key]
            yield item

    # def parse_conditions(self, response):
    #     atoz = response.xpath('//ul[@class="browse-letters squares"]')[0].xpath("li/a/@href").extract()
    #     for i in range(len(atoz)):
    #         yield Request(response.urljoin(atoz[i]),
    #                       callback=self.parse_condition,
    #                       dont_filter=True)
    #
    # def parse_condition(self, response):
    #     drug_list = response.xpath('//ul[@class="drug-list"]')[0].xpath("li/a")
    #     for i in range(len(drug_list)):
    #         yield Request(response.urljoin(drug_list[i].xpath("@href")[0].extract()),
    #                       callback=self.parse_condition_drug,
    #                       meta={'Condition': drug_list[i].xpath("text()")[0].extract()},
    #                       dont_filter=True)
    #
    # def parse_condition_drug(self, response):
    #     drugs = response.xpath("//table[@class='drugs-treatments-table']")[0].xpath("tbody/tr")
    #     for i in range(len(drugs)):
    #         Drug = drugs[i].xpath("td")[0].xpath("a/text()")[0].extract().lower()
    #         Indication = drugs[i].xpath("td")[1].xpath("text()")[0].extract()
    #         Type = drugs[i].xpath("td")[2].xpath("text()")[0].extract().replace('\r\n', '')
    #         if Drug not in WebmdSpider.drug_dict:
    #             print("ANOMALY: " + Drug)
    #         else:
    #             info = WebmdSpider.drug_dict[Drug]
    #             item = WebmdscraperItem()
    #             item['Condition'] = response.meta['Condition']
    #             item['Drug'] = Drug
    #             item['Indication'] = Indication
    #             item['Type'] = Type
    #             for key in info.keys():
    #                 item[key] = info[key]
    #             yield item
