import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'plyavini'
    inst_pass = '#PWD_INSTAGRAM_BROWSER:10:1618314903:AXRQANKUfUukbA1QKswFReuc7jh+2' \
                '/3bAEX7l985NfHWJiI+vxaUU9ANU8DB38famn1YGL01tn2HAQ7hm5Wsvr9uIcqjxvv8TPc' \
                'PzZGQ2RwM79PBzVKh7y0CZK+8zYDTStEF..........'
    #parse_user = 'viktoriia_2752'
                # 'alexeyzharkoff'
    parse_user_list = ['viktoriia_2752', 'alexeyzharkoff']
    followers_hash = '5aefa9893005572d237da5068082d8d5'
    subscribers_hash = '3dec7e2c57367ef3da3d987d89f9dbc8'
    graphql_url = 'https://www.instagram.com/graphql/query/'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.inst_login, 'enc_password': self.inst_pass,
                                           'queryParams': {}, 'optIntoOneTap': 'false'},
                                 headers={'X-CSRFToken': csrf_token}
                                 )

    def user_login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body.get('authenticated'):
            for parse_user in self.parse_user_list:
                yield response.follow(
                    f'/{parse_user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': parse_user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id, 'include_reel': 'true', 'fetch_mutual': 'true', 'first': 24}
        url_followers = f'{self.graphql_url}?query_hash={self.followers_hash}&{urlencode(variables)}'
        url_subscribers = f'{self.graphql_url}?query_hash={self.subscribers_hash}&{urlencode(variables)}'

        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'variables': deepcopy(variables),
                       'username': username,
                       'user_id': user_id}
        )

        yield response.follow(
            url_subscribers,
            callback=self.user_subscribers_parse,
            cb_kwargs={'variables': deepcopy(variables),
                       'username': username,
                       'user_id': user_id}
        )

    def user_followers_parse(self, response: HtmlResponse, variables, username, user_id):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_followers = f'{self.graphql_url}?query_hash={self.followers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={'variables': deepcopy(variables),
                           'username': username,
                           'user_id': user_id}
            )
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for follower in followers:
            yield InstaparserItem(
                parse_user=username,
                status='followers',
                user_id=user_id,
                insta_id=follower.get('node').get('id'),
                insta_name=follower.get('node').get('username'),
                photo=follower.get('node').get('profile_pic_url')
                #user_data=follower.get('node')
            )

    def user_subscribers_parse(self, response: HtmlResponse, variables, username, user_id):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_subscribers = f'{self.graphql_url}?query_hash={self.subscribers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscribers,
                callback=self.user_subscribers_parse,
                cb_kwargs={'variables': deepcopy(variables),
                           'username': username,
                           'user_id': user_id}
            )
        subscribers = j_data.get('data').get('user').get('edge_follow').get('edges')
        for subscriber in subscribers:
            yield InstaparserItem(
                parse_user=username,
                status='subscriptions',
                user_id=user_id,
                insta_id=subscriber.get('node').get('id'),
                insta_name=subscriber.get('node').get('username'),
                photo=subscriber.get('node').get('profile_pic_url')
                #user_data=follower.get('node')
            )

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')
