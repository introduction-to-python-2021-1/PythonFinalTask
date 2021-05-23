import dateparser


class Article:
    def __init__(self, title, link, date, source, description, image):
        self.title = title
        self.link = link
        self.date = dateparser.parse(date)
        self.source = source
        self.description = description
        self.image = image

    def date_str(self, format):
        """Function to convert a date to a string"""
        return self.date.strftime(format)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Article):
            return self.link == other.link
        return False

    def __str__(self):
        """Overrides the default implementation"""
        return 'Title: ' + self.title + '\n' \
               + 'Link: ' + self.link + '\n' \
               + 'Date: ' + self.date_str("%a, %d %B, %Y") + '\n' \
               + 'Source: ' + self.source + '\n' \
               + 'Description: ' + self.description + '\n' \
               + 'Image: ' + self.image + '\n'

    def to_dict(self):
        """Function to convert an instance of a class to a dictionary"""
        fields = {
            'Title': self.title,
            'Link': self.link,
            'Date': self.date_str("%a, %d %B, %Y"),
            'Source': self.source,
            'Description': self.description,
            'Image': self.image, }
        return fields
