def parse_html(html):
    """
    Takes HTML and does some basic parsing
    :param html: html text
    :return: ???
    """
    pass


def url_to_dictionary(url):
    """
    FOR TESTING PURPOSES ONLY, takes a url and runs the various parsing functions to return a dictionary in the JSON
    representation that Miriam's autograder accepts
    :param url: url of requested recipe
    :return: dictionary in autograder-acceptable format
    """
    from app.app import get_html
    html = get_html(url)
    # etc
    pass