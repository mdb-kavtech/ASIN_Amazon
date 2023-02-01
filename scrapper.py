import traceback
import pandas as pd
import requests
import xlsxwriter

from main import amazon_product_review_scraper
import threading
from datetime import *
import time

# from utils import highlight_diff, ASIN_email

start_time = time.time()
today = datetime.today()
t_day = today.strftime("%m-%d-%Y")
review_sheets = [[] for _ in range(4)]
price_sheets = [[] for _ in range(4)]
question_sheets = [[] for _ in range(4)]
threads = [None] * 4
df = [pd.read_excel('ASIN SKU LIST.xlsx', nrows=211),
      pd.read_excel('ASIN SKU LIST.xlsx', skiprows=range(1, 212), nrows=211),
      pd.read_excel('ASIN SKU LIST.xlsx', skiprows=range(1, 423), nrows=211),
      pd.read_excel('ASIN SKU LIST.xlsx', skiprows=range(1, 634))]


# df = pd.read_excel('price_1.xlsx')
# df = df[df['scrape_price'].isnull()]


def get_data_from_amazon_1(asin_nums1, review_sheet1, price_sheet1, question_sheet1, thread_id1):
    for asin in asin_nums1:
        try1 = 0
        print('scraping for asin = {}, thread {}'.format(asin, thread_id1))
        while True:
            try:
                base_scraper1 = amazon_product_review_scraper(amazon_site="amazon.com", product_asin=asin)
                reviews, prices, questions = base_scraper1.scrape()

                review_sheet1.append(reviews)
                price_sheet1.append(prices)
                question_sheet1.append(questions)
                break
            except requests.exceptions.ConnectionError as e:
                print(e)
                time.sleep(5)
                continue
            except Exception as e:
                if try1 > 1:
                    print("main exc\n", e)
                    traceback.print_exc()
                    break
                try1 += 1


def get_data_from_amazon_2(asin_nums2, review_sheet2, price_sheet2, question_sheet2, thread_id2):
    for asin in asin_nums2:
        try2 = 0
        print('scraping for asin = {}, thread {}'.format(asin, thread_id2))
        while True:
            try:
                base_scraper2 = amazon_product_review_scraper(amazon_site="amazon.com", product_asin=asin)
                reviews, prices, questions = base_scraper2.scrape()

                review_sheet2.append(reviews)
                price_sheet2.append(prices)
                question_sheet2.append(questions)
                break
            except requests.exceptions.ConnectionError as e:
                print(e)
                time.sleep(5)
                continue
            except Exception as e:
                if try2 > 1:
                    print("main exc\n", e)
                    traceback.print_exc()
                    break
                try2 += 1


def get_data_from_amazon_3(asin_nums3, review_sheet3, price_sheet3, question_sheet3, thread_id3):
    for asin in asin_nums3:
        try3 = 0
        print('scraping for asin = {}, thread {}'.format(asin, thread_id3))
        while True:
            try:
                base_scraper3 = amazon_product_review_scraper(amazon_site="amazon.com", product_asin=asin)
                reviews, prices, questions = base_scraper3.scrape()

                review_sheet3.append(reviews)
                price_sheet3.append(prices)
                question_sheet3.append(questions)
                break
            except requests.exceptions.ConnectionError as e:
                print(e)
                time.sleep(5)
                continue
            except Exception as e:
                if try3 > 1:
                    print("main exc\n", e)
                    traceback.print_exc()
                    break
                try3 += 1


def get_data_from_amazon_4(asin_nums4, review_sheet4, price_sheet4, question_sheet4, thread_id4):
    for asin in asin_nums4:
        try4 = 0
        print('scraping for asin = {}, thread {}'.format(asin, thread_id4))
        while True:
            try:
                base_scraper4 = amazon_product_review_scraper(amazon_site="amazon.com", product_asin=asin)
                reviews, prices, questions = base_scraper4.scrape()

                review_sheet4.append(reviews)
                price_sheet4.append(prices)
                question_sheet4.append(questions)
                break
            except requests.exceptions.ConnectionError as e:
                print(e)
                time.sleep(5)
                continue
            except Exception as e:
                if try4 > 1:
                    print("main exc\n", e)
                    traceback.print_exc()
                    break
                try4 += 1


# def create_asin_file():
#     qdf = pd.read_excel('price.xlsx')
#     qdf2 = pd.read_excel('question.xlsx')
#     qdf3 = pd.read_excel('review.xlsx')
#
#     qdf['Descritption'] = qdf['Descritption'].fillna('')
#     qdf['Description 2'] = qdf['Description 2'].fillna('')
#     qdf['Life Cycle Status Code'] = qdf['Life Cycle Status Code'].fillna('')
#     qdf['MAP-Expected Price'] = qdf['MAP-Expected Price'].fillna(0)
#     qdf['original_price'] = qdf['original_price'].fillna('0')
#     qdf['scrape_price'] = qdf['scrape_price'].fillna('0')
#     qdf['total_rating'] = qdf['total_rating'].fillna('')
#     qdf['average_rating'] = qdf['average_rating'].fillna('')
#     qdf['free_delivery_date'] = qdf['free_delivery_date'].fillna('')
#     qdf['stock_status'] = qdf['stock_status'].fillna('')
#     qdf['ship_from'] = qdf['ship_from'].fillna('')
#     qdf['sold_by'] = qdf['sold_by'].fillna('')
#     qdf['amazon_badge'] = qdf['amazon_badge'].fillna('')
#     qdf['average_rating'] = qdf['average_rating'].astype('str')
#
#     qdf2['Item No_'] = qdf2['Item No_'].fillna('')
#     qdf2['asin_number'] = qdf2['asin_number'].fillna('')
#     qdf2['Descritption'] = qdf2['Descritption'].fillna('')
#     qdf2['Description 2'] = qdf2['Description 2'].fillna('')
#     qdf2['Life Cycle Status Code'] = qdf2['Life Cycle Status Code'].fillna('')
#     qdf2['MAP-Expected Price'] = qdf2['MAP-Expected Price'].fillna(0)
#     qdf2['question'] = qdf2['question'].fillna('')
#
#     qdf3['Descritption'] = qdf3['Descritption'].fillna('')
#     qdf3['Description 2'] = qdf3['Description 2'].fillna('')
#     qdf3['Life Cycle Status Code'] = qdf3['Life Cycle Status Code'].fillna('')
#     qdf3['MAP-Expected Price'] = qdf3['MAP-Expected Price'].fillna(0)
#     qdf3['date_info'] = qdf3['date_info'].fillna('')
#     qdf3['reviewer_name'] = qdf3['reviewer_name'].fillna('')
#     qdf3['review_title'] = qdf3['review_title'].fillna('')
#     qdf3['review_content'] = qdf3['review_content'].fillna('')
#     qdf3['reviewer_rating'] = qdf3['reviewer_rating'].fillna('')
#     qdf3['total_reviews'] = qdf3['total_reviews'].fillna(0)
#
#     qdf['Scrape Date'] = str(date.today() - timedelta(days=0))
#     qdf2['Scrape Date'] = str(date.today() - timedelta(days=0))
#     qdf3['Scrape Date'] = str(date.today() - timedelta(days=0))
#
#     workbook = xlsxwriter.Workbook('Amazon MDB Report.xlsx'.format(date.today()))
#     worksheet = workbook.add_worksheet('price')
#     worksheet2 = workbook.add_worksheet('question')
#     worksheet3 = workbook.add_worksheet('review')
#     c_code = {
#         "l_green": "#d8e4bc",
#         "l_red": "#da9694",
#         "d_green": "#76933c",
#         "yellow": "#ffff00",
#         "orange": "#e26b0a",
#         "grey": "#e4dfec",
#         "blue_h": "#4f81bd"
#     }
#     colors = {}
#     for color_name in c_code.keys():
#         xlsx_format = workbook.add_format()
#         xlsx_format.set_bg_color(c_code[color_name])
#         colors[color_name] = xlsx_format
#     worksheet.write_row(0, 0, list(qdf.columns), colors['blue_h'])
#     worksheet2.write_row(0, 0, list(qdf2.columns), colors['blue_h'])
#     worksheet3.write_row(0, 0, list(qdf3.columns), colors['blue_h'])
#
#     row_id = 1
#     for row in qdf.itertuples(index=False):
#         th_price_p = int(row[5] * 0.20) + row[5]
#         th_price_n = row[5] - int(row[5] * 0.20)
#         if type(row[7]) != float:
#             if th_price_p > int(row[7].replace(',', '')) > th_price_n or row[7] == '0':
#                 # print('ok')
#                 # print(row[7], type(row[7]))
#                 for i, val in enumerate(row):
#                     if type(val) == float:
#                         worksheet.write(row_id, i, "")
#                     elif val != 'nan':
#                         worksheet.write(row_id, i, val)
#                     else:
#                         worksheet.write(row_id, i, "")
#             else:
#                 # print('not ok')
#                 # print(row[7], type(row[7]))
#                 for i, val in enumerate(row):
#                     if type(val) == float:
#                         worksheet.write(row_id, i, "")
#                     elif val != 'nan':
#                         worksheet.write(row_id, i, val, colors["l_red"])
#                     else:
#                         worksheet.write(row_id, i, "")
#         else:
#             # print('main else')
#             for i, val in enumerate(row):
#                 if i == 7:
#                     worksheet.write(row_id, i, "")
#                 # print(val, type(val))
#                 if type(val) == float:
#                     worksheet.write(row_id, i, "")
#                 elif val != 'nan':
#                     worksheet.write(row_id, i, val)
#                 else:
#                     worksheet.write(row_id, i, "")
#         print('**********************************************************************************')
#         row_id += 1
#
#         row_id = 1
#         for row in qdf2.itertuples(index=False):
#             #     print(row)
#             for i, val in enumerate(row):
#                 if type(val) == float:
#                     worksheet2.write(row_id, i, "")
#                 elif val != 'nan':
#                     worksheet2.write(row_id, i, val)
#                 else:
#                     worksheet2.write(row_id, i, "")
#             #     print('********************************************************************************')
#             row_id += 1
#
#         row_id = 1
#         for row in qdf3.itertuples(index=False):
#             #     print(row)
#             for i, val in enumerate(row):
#                 if type(val) == float:
#                     worksheet3.write(row_id, i, "")
#                 #             print(row_id, i, "")
#                 elif val != 'nan':
#                     worksheet3.write(row_id, i, val)
#                 #             print(row_id, i, val)
#                 else:
#                     worksheet3.write(row_id, i, "")
#             #             print(row_id, i, "")
#             #     print('********************************************************************************************')
#             row_id += 1
#         workbook.close()

scraper = [get_data_from_amazon_1, get_data_from_amazon_2, get_data_from_amazon_3, get_data_from_amazon_4]

# get_data_from_amazon_1(df[0]['asin_number'], review_sheets[0], price_sheets[0], question_sheets[0], 0)
for i in range(len(threads)):
    threads[i] = threading.Thread(target=scraper[i], args=(df[i]['asin_number'], review_sheets[i],
                                                           price_sheets[i], question_sheets[i], i))
    threads[i].start()
    print('thread {} started'.format(i))

for i in range(len(threads)):
    threads[i].join()

print("--- %s seconds ---" % (time.time() - start_time))

df = pd.read_excel('ASIN SKU LIST.xlsx')

fps = [item for sublist in price_sheets for item in sublist]
fqs = [item for sublist in question_sheets for item in sublist]
frs = [item for sublist in review_sheets for item in sublist]
for ps in fqs:
    try:
        ps['asin_number'] = [ps['asin_number']] * len(ps['question'])
    except:
        pass
for ps in frs:
    try:
        ps['asin_number'] = [ps['asin_number']] * len(ps['reviewer_name'])
        ps['total_reviews'] = [ps['total_reviews']] * len(ps['reviewer_name'])
    except:
        pass

print('fps: {}, fqs: {}, frs: {}'.format(len(fps), len(fqs), len(frs)))

fqs_df = pd.DataFrame()
for d in fqs:
    temp_df = pd.DataFrame.from_dict(d, orient='index').transpose()
    fqs_df = pd.concat([fqs_df, temp_df])
print(fqs_df.shape)

frs_df = pd.DataFrame()
for d in frs:
    temp_df = pd.DataFrame.from_dict(d, orient='index').transpose()
    frs_df = pd.concat([frs_df, temp_df])
print(frs_df.shape)

fps_df = pd.DataFrame(fps)
print(fps_df.shape)

price_df = fps_df[['original_price', 'scrape_price', 'total_rating', 'average_rating', 'free_delivery_date',
                   'stock_status', 'ship_from', 'sold_by', 'amazon_badge', 'asin_number']]
# rank_df = fps_df[['Ranking 1', 'Category 1', 'Ranking 2', 'Category 2', 'asin_number']]

price_df = pd.merge(df, price_df, on='asin_number', how='outer')
print(price_df.shape)
price_df.to_excel('price.xlsx', index=False)

# rank_df = pd.merge(df, rank_df, on='asin_number', how='outer')
# print(rank_df.shape)
# rank_df.rename(columns={'ranking 1': 'Ranking 1', 'ranking 2': 'Ranking 2', 'category 1': 'Category 1',
#                         'category 2': 'Category 2', 'asin_number': 'ASIN', 'Item No_': 'SKU',
#                         'Descritption': 'Description'}, inplace=True)
# rank_df['Scrape Date'] = str(date.today() - timedelta(days=0))
# out = rank_df.reindex(
#     columns=['Scrape Date', 'SKU', 'ASIN', 'Description', 'Ranking 1', 'Category 1', 'Ranking 2', 'Category 2'])
# out['Ranking 1'] = out['Ranking 1'].str.split('#', expand=True)[1].astype(str)
# out['Ranking 2'] = out['Ranking 2'].str.split('#', expand=True)[1].astype(str)
# out['Scrape Date'] = out['Scrape Date'].replace(['2023-1-3'], '2023-1-4')
# out.to_excel('RankSheet2.xlsx', index=False)

question_df = pd.merge(df, fqs_df, on='asin_number', how='outer')
print(question_df.shape)
question_df.to_excel('question.xlsx', index=False)

review_df = pd.merge(df, frs_df, on='asin_number', how='outer')
print(review_df.shape)
review_df.to_excel('review.xlsx', index=False)


# create_asin_file()
