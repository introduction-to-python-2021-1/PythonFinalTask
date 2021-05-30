from jinja2 import Environment, FileSystemLoader
from utils import util


class RssConverter:

    def get_news_template(self, rss_news, img_files: dict, show_logs: bool = False):
        """
        Create html for saving into file

        :param img_files: dict of ig_link:src for inserting images into file
        :param rss_news: news to be inserted into template
        :param show_logs: show logs on console or not
        :return: str
        """
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('news_template.html')
        util.log(msg="Start rendering template...", flag="INFO", show_on_console=show_logs)
        generated_page = template.render(channels_news=rss_news, img_files=img_files)
        util.log(msg="Template was generated successfully", flag="INFO", show_on_console=show_logs)
        return generated_page
