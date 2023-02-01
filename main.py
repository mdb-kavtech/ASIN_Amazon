# Importing packages
from import_file import *

# to ignore SSL certificate errors
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# random user-agent
from fake_useragent import UserAgent

ua = UserAgent()


class amazon_product_review_scraper:
    def __init__(self, amazon_site, product_asin, sleep_time=1, start_page=1, end_page=None):
        self.end_page = None
        self.question_page = None
        self.max_try = 10
        self.ua = ua.random
        self.main_page = "https://www." + amazon_site + "/dp/" + product_asin + "?th=1"
        self.sleep_time = sleep_time
        self.reviews_dict = {}
        self.question_dict = {}
        self.reviews_page = "https://www." + amazon_site + "/dp/product-reviews/" + product_asin + \
                            "/ref=cm_cr_arp_d_viewopt_rvwer?sortBy=recent&pageNumber=1&reviewerType=avp_only_reviews"
        self.product_asin = product_asin
        self.start_page = start_page
        self.amazon_site = amazon_site
        self.end_page = end_page

    def total_pages(self):
        response = self.request_wrapper(self.reviews_page.format(1))
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find("div", class_="a-row a-spacing-base a-size-base").get_text()
        total_reviews = content.strip().split()[3]
        total_reviews = int(''.join(total_reviews[0:].split(',')))
        self.reviews_dict['total_reviews'] = total_reviews
        if total_reviews == 0:
            total_pages = 0
        else:
            total_pages = 1
        return total_pages

    # MAIN FUNCTION
    def scrape(self):
        data = self.request_wrapper(self.main_page)
        soup = BeautifulSoup(data.text, 'html.parser')

        # Rotal customer gives rating
        total_rating = soup.find('span', id="acrCustomerReviewText")
        if total_rating is None:
            total_rating = None
        else:
            total_rating = total_rating.get_text().strip().split()[0]

        # Amazon badge
        amazon_badge = soup.find('span', class_='ac-for-text')
        if amazon_badge is None:
            badge = None
        else:
            badge = amazon_badge.find('span').get_text()

        # Discount Price of the product
        main_scrape_price = []
        price_span = soup.find("span", class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay")
        if price_span is None:
            pass
        else:
            price = price_span.find("span", class_="a-price-whole").get_text().split('.')[0]
            main_scrape_price.append(price)
        if len(main_scrape_price) == 0:
            price_li = soup.find('li', {"data-defaultasin": self.product_asin})
            if price_li is None:
                pass
            else:
                price = price_li.find("span", class_="a-size-mini olpMessageWrapper")
                if price is None:
                    pass
                else:
                    price = price.get_text()
                    if "from" in price:
                        price = price.split('$')[1].split('.')[0]
                        main_scrape_price.append(price)
            if len(main_scrape_price) == 0:
                main_scrape_price.append(None)

        # Original Price of the product
        full_price = soup.find("div", class_="a-section a-spacing-small aok-align-center")
        original_price_list = []
        if full_price is None:
            original_price_list.append(None)
        else:
            original_price = full_price.find("span", class_="a-offscreen")
            if original_price is None:
                original_price_list.append(None)
            else:
                original_price = original_price.get_text()
                original_price = original_price.split()[0]
                original_price_list.append(original_price)

        # Average rating of the product
        average_review = soup.find('span', class_="a-icon-alt")
        if average_review is None:
            average_review = None
        else:
            average_review = average_review.get_text().strip().split()[0]
            if 'Previous' in average_review:
                average_review = None

        # free delivery date
        free_delivery_date = []
        free_delivery = soup.find_all('span', class_='a-text-bold')
        for i in free_delivery[0:5]:
            if ',' in i.text:
                free_delivery_date.append(i.text)
                break
            if '-' in i.text:
                text = i.text.split('-')[1]
                if len(text.split(' ')) == 3 or len(text.split(' ')) == 2:
                    free_delivery_date.append(i.text)
                    break
        if len(free_delivery_date) == 0:
            free_delivery_date.append(None)

        # Ship and Sold by
        all_data = soup.find('div', class_="tabular-buybox-container")
        selected_divs = []
        if all_data is None:
            selected_divs.append(all_data)
            selected_divs.append(None)
            selected_divs.append(None)
        else:
            selected_data = all_data.find_all('span', class_='a-size-small')
            for div in selected_data[1:4]:
                selected_divs.append(div.text)
        ship_from = selected_divs[0]
        sold_by = selected_divs[2]

        # Check availability of product
        required_data = []
        availability_data = soup.find('div', id="availability")
        if availability_data is None:
            required_data.append('out of stock')
        else:
            available_data = availability_data.find('span',
                                                    class_="a-size-medium a-color-success") or availability_data.find(
                'span', class_="a-size-medium a-color-price") or availability_data.find(
                'span', class_="a-size-medium a-color-state")
            if available_data is None:
                required_data.append("out of stock")
            else:
                # if available_data == None
                for check_availability in available_data:
                    if check_availability is None:
                        required_data.append("out of stock")
                    else:
                        check_availability = check_availability.get_text()
                        if check_availability == ' ':
                            required_data.append("out of stock")
                        else:
                            required_data.append(check_availability)
        stock_status = required_data

        # Rank
        # description = []
        # rank = []
        # try:
        #     driver = self.get_driver()
        #     driver.get(self.main_page)
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        #     soup = BeautifulSoup(driver.page_source, 'html.parser')
        #     table_ = soup.find('table', id="productDetails_detailBullets_sections1")
        #     table_row = table_.find_all('td')
        #     for i in table_row:
        #         if '#' in i.text:
        #             split_rank = i.text.split('(')
        #             rank1 = split_rank[0].split('in')[0]
        #             if rank1 is None:
        #                 rank1 = None
        #             rank.append(rank1)
        #             des1 = split_rank[0].split('in')[1]
        #             if des1 is None:
        #                 des1 = None
        #             description.append(des1)
        #             split_rank1 = split_rank[1].split(')')[1]
        #             if split_rank1 is None:
        #                 rank.append(None)
        #                 description.append(None)
        #             else:
        #                 if '#' in split_rank1:
        #                     rank_2nd = split_rank1.split('in')[0]
        #                     if rank_2nd is None:
        #                         rank_2nd = None
        #                     rank.append(rank_2nd)
        #                     dic = split_rank1.split('in')[1]
        #                     if '#' in dic:
        #                         dic = dic.split('#')[0]
        #                         if dic is None:
        #                             dic = None
        #                         description.append(dic)
        #                     else:
        #                         description.append(dic)
        #             if len(rank) == 0 and len(description) == 0:
        #                 rank.append(None)
        #                 description.append(None)
        #                 rank.append(None)
        #                 description.append(None)
        #                 break
        #     try:
        #         driver.close()
        #     except Exception as rank_e:
        #         rank_e = str(rank_e)
        # except Exception as e:
        #     print('Scrape Rank', e)
        #
        # while len(rank) < 2: rank.append('')
        # while len(description) < 2: description.append('')
        if type(main_scrape_price) is list:
            try:
                main_scrape_price = main_scrape_price[0].strip()
            except:
                main_scrape_price = main_scrape_price[0]
        if type(original_price_list) is list:
            try:
                original_price_list = original_price_list[0].strip()
            except:
                original_price_list = original_price_list[0]
        if type(free_delivery_date) is list:
            try:
                free_delivery_date = free_delivery_date[0].strip()
            except:
                free_delivery_date = free_delivery_date[0]
        if type(stock_status) is list:
            try:
                stock_status = stock_status[0].strip()
            except:
                stock_status = stock_status[0]

        price_dict = {'scrape_price': main_scrape_price, 'original_price': original_price_list,
                      'average_rating': average_review, 'total_rating': total_rating, 'ship_from': ship_from,
                      'sold_by': sold_by, 'free_delivery_date': free_delivery_date, 'stock_status': stock_status,
                      'amazon_badge': badge}
            # , 'Ranking 1': rank[0], 'Category 1': description[0], 'Ranking 2': rank[1],
            #           'Category 2': description[1]}
        try:
            self.question_page = "https://www." + self.amazon_site + "/ask/questions/asin/" + self.product_asin + "/1"
            data = self.request_wrapper(self.question_page)
            soup = BeautifulSoup(data.text, 'html.parser')
            req_question = []
            question_div = soup.find("div", class_="a-section askTeaserQuestions")
            if question_div is None:
                req_question.append('Have no question')
            else:
                question = question_div.find_all('span', class_="a-declarative")
                question_lst = []
                for i in question:
                    if str(i.text).strip() != '':
                        question_lst.append(str(i.text).strip())

                for que in question_lst:
                    if 'See all' not in que:
                        req_question.append(que)
            self.question_dict['question'] = req_question
        except Exception as e:
            print('Scrape Questions', e)

        if self.end_page is None:
            self.end_page = self.total_pages()
        else:
            self.end_page = min(self.end_page, self.total_pages())

        print("Total pages: {}".format(self.end_page - self.start_page + 1), flush=True)
        print("Start page: {}; End page: {}".format(self.start_page, self.end_page))
        print("Started!", flush=True)

        for page in tqdm(range(self.start_page, self.end_page + 1)):
            self.page_scraper(page)
        print("Completed!")
        self.reviews_dict['asin_number'] = self.product_asin
        price_dict['asin_number'] = self.product_asin
        self.question_dict['asin_number'] = self.product_asin
        return self.reviews_dict, price_dict, self.question_dict

    # page scrapper
    @staticmethod
    def helper(content, tag, parameter_key, parameter_value):
        attribute_lst = []
        attributes = content.find_all(tag, {parameter_key: parameter_value})
        for attribute in attributes:
            attribute_lst.append(attribute.contents[0])
        return attribute_lst

    def page_scraper(self, page):
        try:
            response = self.request_wrapper(self.reviews_page.format(page))
            # parsing content
            soup = BeautifulSoup(response.text, 'html.parser')
            reviews = soup.findAll("div", {"class": "a-section review aok-relative"})
            # parsing reviews section
            reviews = BeautifulSoup('<br/>'.join([str(tag) for tag in reviews]), 'html.parser')

            # 1. name of customer
            name_lst = self.helper(reviews, "span", "class", "a-profile-name")

            # 2. review_title
            titles = reviews.find_all("a", {"data-hook": "review-title"})
            title_lst = []
            for title in titles:
                title_lst.append(title.find_all("span")[0].contents[0])
            while len(title_lst) != len(name_lst):
                title_lst.append(None)

            # 3. rating
            ratings = reviews.find_all("i", {"data-hook": "review-star-rating"})
            rating_lst = []
            for rating in ratings:
                rating_lst.append(rating.find_all("span")[0].contents[0])
            while len(rating_lst) != len(name_lst):
                rating_lst.append(None)

            # 4. date
            date_lst = self.helper(reviews, "span", "data-hook", "review-date")

            # 5. content
            contents = reviews.find_all("span", {"data-hook": "review-body"})
            content_lst = []
            for content in contents:
                if content is not None:
                    try:
                        text_ = content.find_all("span")[0].get_text("\n").strip()
                        text_ = ". ".join(text_.splitlines())
                        content_lst.append(text_)
                    except:
                        content_lst.append(None)

            # adding to the main list
            self.reviews_dict['date_info'] = date_lst
            self.reviews_dict['reviewer_name'] = name_lst
            self.reviews_dict['review_title'] = title_lst
            self.reviews_dict['review_content'] = content_lst
            self.reviews_dict['reviewer_rating'] = rating_lst

        except Exception as e:
            print("Not able to scrape page {} (CAPTCHA is not bypassed)".format(page), flush=True)

    # wrapper around request package to make it resilient
    def request_wrapper(self, reviews_page):
        while True:
            # amazon blocks requests that do not come from browser, therefore need to mention user-agent
            # response = requests.get(url, verify=False, headers={'User-Agent': self.ua}, proxies=self.proxy)
            response = requests.get(reviews_page, verify=False, headers={'User-Agent': self.ua})

            # checking the response code
            if response.status_code != 200:
                raise Exception(response.raise_for_status())

            # checking whether captcha is bypassed or not (status code is 200 in case it displays the captcha image)
            if "api-services-support@amazon.com" in response.text:

                if self.max_try == 0:
                    continue
                    # raise Exception("CAPTCHA is not bypassed")
                else:
                    time.sleep(self.sleep_time)
                    self.max_try -= 1
                    self.ua = ua.random
                    # self.proxy = choice(self.proxies)
                    continue

            self.max_try = 5
            break

        return response

    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument("start-maximized")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
