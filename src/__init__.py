from .scraper import create_image as create_news_image


def display_news(inky_display, display_color):
    print("Displaying news")
    return create_news_image(inky_display, display_color)

